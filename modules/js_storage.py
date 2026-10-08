# JavaScript Storage Engine Module (IndexedDB, per-record, sync-ready)
JS_STORAGE = r"""
// ==========================================
// 0. STORAGE ENGINE (IndexedDB, one record per item)
// ==========================================
// The UI keeps working on the in-memory `appData` object.
// This layer splits appData into records ({id, type, data, updatedAt, deleted})
// and only writes the records that actually changed.
// - Deleted items become tombstones (deleted: true), never vanish, so sync can propagate deletes.
// - Every write is also queued in the 'outbox' store for the future cloud sync.
// - Device-only state (running timer, export/import times) lives in localStorage.
// - Safety snapshots live in IndexedDB 'local' store and are never synced or exported.

const DB_NAME = 'focusdeck';
const DB_VERSION = 1;
const LEGACY_STORAGE_KEY = 'focusdeck.v1';      // old single-blob storage (read once, never deleted)
const LOCAL_STATE_KEY = 'focusdeck.device.v1';  // device-only state

let _db = null;
let _storageReady = false;
let _persisted = new Map();   // recordId -> { type, json, deleted }
let _saveScheduled = false;
let _saveChain = Promise.resolve();
let _baselineSave = false;    // when true, writes get updatedAt = 0 (defaults that must never beat real data)
let deviceSnapshots = [];     // [{ timestamp, reason, data }]

// ---------- ids ----------
function uid(prefix) {
  let r;
  try {
    r = crypto.randomUUID();
  } catch (e) {
    r = Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10) + Math.random().toString(36).slice(2, 10);
  }
  return (prefix ? prefix + '-' : '') + r;
}

// ---------- stable JSON for change detection ----------
function stableStringify(v) {
  if (v === null || typeof v !== 'object') return JSON.stringify(v === undefined ? null : v);
  if (Array.isArray(v)) return '[' + v.map(stableStringify).join(',') + ']';
  const keys = Object.keys(v).filter(k => v[k] !== undefined).sort();
  return '{' + keys.map(k => JSON.stringify(k) + ':' + stableStringify(v[k])).join(',') + '}';
}

// ---------- IndexedDB helpers ----------
function openDB() {
  return new Promise((resolve, reject) => {
    if (!('indexedDB' in window)) { reject(new Error('IndexedDB is not available in this browser')); return; }
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains('records')) {
        const s = db.createObjectStore('records', { keyPath: 'id' });
        s.createIndex('type', 'type', { unique: false });
      }
      if (!db.objectStoreNames.contains('outbox')) db.createObjectStore('outbox', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('local')) db.createObjectStore('local');
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error || new Error('Could not open database'));
    req.onblocked = () => reject(new Error('Database is blocked by another open FocusDeck tab'));
  });
}

function idbGetAll(storeName) {
  return new Promise((resolve, reject) => {
    const tx = _db.transaction(storeName, 'readonly');
    const req = tx.objectStore(storeName).getAll();
    req.onsuccess = () => resolve(req.result || []);
    req.onerror = () => reject(req.error);
  });
}

function idbGetLocal(key) {
  return new Promise((resolve, reject) => {
    const tx = _db.transaction('local', 'readonly');
    const req = tx.objectStore('local').get(key);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

function idbPutLocal(key, value) {
  return new Promise((resolve, reject) => {
    const tx = _db.transaction('local', 'readwrite');
    tx.objectStore('local').put(value, key);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
    tx.onabort = () => reject(tx.error || new Error('Transaction aborted'));
  });
}

function idbWriteRecords(puts) {
  return new Promise((resolve, reject) => {
    const tx = _db.transaction(['records', 'outbox'], 'readwrite');
    const rs = tx.objectStore('records');
    const ob = tx.objectStore('outbox');
    puts.forEach(rec => {
      rs.put(rec);
      ob.put({ id: rec.id, updatedAt: rec.updatedAt });
    });
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
    tx.onabort = () => reject(tx.error || new Error('Transaction aborted (storage may be full)'));
  });
}

// ---------- appData <-> records ----------
// Simple list types: appData key -> record type
const LIST_TYPES = [
  { key: 'sessions', type: 'session', ordered: false },
  { key: 'tags', type: 'tag', ordered: true },
  { key: 'skills', type: 'skill', ordered: true },
  { key: 'manualBacklogEntries', type: 'backlog', ordered: true },
  { key: 'timeblockTemplates', type: 'template', ordered: true },
  { key: 'parkedThoughts', type: 'thought', ordered: false }
];
const CONFIG_KEYS = ['dayWindow', 'dismissedRecentSessionIds'];

function freshAppData() {
  return {
    schemaVersion: SCHEMA_VERSION,
    settings: { ...DEFAULT_SETTINGS },
    tags: DEFAULT_TAGS.map(t => ({ ...t })),
    timer: defaultTimerState(),
    sessions: [],
    parkedThoughts: [],
    dismissedRecentSessionIds: [],
    dayWindow: { startMin: 480, endMin: 1320 },
    timeblockPlans: {},
    timeblockTemplates: [],
    skills: [],
    manualBacklogEntries: [],
    meta: { lastExport: null, lastImport: null }
  };
}

// Splits appData into a Map(recordId -> {type, data}).
// Also repairs missing or duplicate ids in place, so memory and storage stay consistent.
function decompose(data) {
  const out = new Map();

  LIST_TYPES.forEach(({ key, type, ordered }) => {
    const arr = Array.isArray(data[key]) ? data[key] : [];
    arr.forEach((item, i) => {
      if (!item || typeof item !== 'object') return;
      if (!item.id || out.has(type + ':' + item.id)) item.id = uid(type);
      const rec = ordered ? { ...item, _order: i } : { ...item };
      out.set(type + ':' + item.id, { type, data: rec });
    });
  });

  // Time block plans: each block is a record; other plan fields (notes) form a 'dayplan' record
  const plans = data.timeblockPlans || {};
  Object.keys(plans).forEach(date => {
    const plan = plans[date];
    if (!plan || typeof plan !== 'object') return;
    (Array.isArray(plan.blocks) ? plan.blocks : []).forEach((b, i) => {
      if (!b || typeof b !== 'object') return;
      if (!b.id || out.has('block:' + b.id)) b.id = uid('tb');
      out.set('block:' + b.id, { type: 'block', data: { ...b, _date: date, _order: i } });
    });
    const extra = {};
    let hasContent = false;
    Object.keys(plan).forEach(k => {
      if (k === 'blocks') return;
      extra[k] = plan[k];
      if (plan[k] !== '' && plan[k] !== null && plan[k] !== undefined) hasContent = true;
    });
    if (hasContent) out.set('dayplan:' + date, { type: 'dayplan', data: { ...extra, _date: date } });
  });

  // Settings: one record per key, so editing two different settings on two devices never conflicts
  const s = data.settings || {};
  Object.keys(s).forEach(k => {
    if (s[k] === undefined) return;
    out.set('setting:' + k, { type: 'setting', data: { key: k, value: s[k] } });
  });

  CONFIG_KEYS.forEach(k => {
    if (data[k] !== undefined) out.set('config:' + k, { type: 'config', data: { key: k, value: data[k] } });
  });

  return out;
}

function stripInternal(obj) {
  const o = { ...obj };
  delete o._order;
  delete o._date;
  return o;
}

// Builds appData from stored records (tombstones are skipped).
function compose(records) {
  const data = freshAppData();
  data.tags = [];
  const lists = {};
  LIST_TYPES.forEach(lt => { lists[lt.type] = []; });
  const blocksByDate = {};
  let sawTag = false;

  records.forEach(r => {
    if (r.deleted || !r.data) return;
    const d = r.data;
    if (lists[r.type]) {
      lists[r.type].push(d);
      if (r.type === 'tag') sawTag = true;
    } else if (r.type === 'block') {
      (blocksByDate[d._date] = blocksByDate[d._date] || []).push(d);
    } else if (r.type === 'dayplan') {
      const plan = data.timeblockPlans[d._date] = data.timeblockPlans[d._date] || { blocks: [], notes: '' };
      Object.assign(plan, stripInternal(d));
    } else if (r.type === 'setting') {
      data.settings[d.key] = d.value;
    } else if (r.type === 'config') {
      data[d.key] = d.value;
    }
  });

  LIST_TYPES.forEach(({ key, type, ordered }) => {
    let arr = lists[type];
    if (ordered) arr.sort((a, b) => (a._order || 0) - (b._order || 0));
    else if (type === 'session') arr.sort((a, b) => (b.startedAt || 0) - (a.startedAt || 0));
    else arr.sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0));
    data[key] = arr.map(stripInternal);
  });
  if (!sawTag) data.tags = [];

  Object.keys(blocksByDate).forEach(date => {
    const plan = data.timeblockPlans[date] = data.timeblockPlans[date] || { blocks: [], notes: '' };
    plan.blocks = blocksByDate[date].sort((a, b) => (a._order || 0) - (b._order || 0)).map(stripInternal);
  });

  return data;
}

// ---------- device-only state ----------
function readLocalState() {
  try {
    const raw = localStorage.getItem(LOCAL_STATE_KEY);
    return raw ? (JSON.parse(raw) || {}) : {};
  } catch (e) {
    return {};
  }
}

let _localFlags = {};
function writeLocalState() {
  try {
    localStorage.setItem(LOCAL_STATE_KEY, JSON.stringify({
      timer: appData.timer,
      meta: appData.meta,
      flags: _localFlags
    }));
  } catch (e) {
    showStorageError('Could not save the timer state on this device: ' + e.message);
  }
}

// ---------- visible errors ----------
function showStorageError(msg) {
  console.error('[FocusDeck storage]', msg);
  let bar = document.getElementById('storage-error-bar');
  if (!bar) {
    bar = document.createElement('div');
    bar.id = 'storage-error-bar';
    bar.setAttribute('role', 'alert');
    bar.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:99999;background:#B4232F;color:#fff;' +
      'font:600 13px/1.4 system-ui,sans-serif;padding:10px 16px;display:flex;gap:12px;align-items:center;' +
      'justify-content:space-between;box-shadow:0 2px 12px rgba(0,0,0,.4);';
    bar.innerHTML = '<span id="storage-error-text"></span>' +
      '<button type="button" id="storage-error-export" style="background:#fff;color:#B4232F;border:0;border-radius:6px;' +
      'padding:6px 10px;font-weight:700;cursor:pointer;white-space:nowrap;">Export backup now</button>';
    document.body.appendChild(bar);
    document.getElementById('storage-error-export').addEventListener('click', () => {
      try { handleExportAllData(); } catch (e) { alert('Export failed: ' + e.message); }
    });
  }
  document.getElementById('storage-error-text').textContent = 'NOT SAVED. ' + msg;
  bar.style.display = 'flex';
}

function clearStorageError() {
  const bar = document.getElementById('storage-error-bar');
  if (bar) bar.style.display = 'none';
}

// ---------- save ----------
// Called from everywhere in the UI. Device state is written immediately;
// record changes are coalesced and written at the end of the current task.
function saveAppData() {
  writeLocalState();
  if (!_storageReady || _saveScheduled) return;
  _saveScheduled = true;
  Promise.resolve().then(() => {
    _saveScheduled = false;
    persistRecords();
  });
}

// Computes changed records and writes them. Returns a promise that resolves when written.
function persistRecords() {
  if (!_storageReady) return Promise.resolve();
  const current = decompose(appData);
  const now = _baselineSave ? 0 : Date.now();
  const puts = [];
  const previous = new Map();

  current.forEach((rec, id) => {
    const json = stableStringify(rec.data);
    const prev = _persisted.get(id);
    if (!prev || prev.deleted || prev.json !== json) {
      puts.push({ id, type: rec.type, data: rec.data, updatedAt: now, deleted: false });
      previous.set(id, prev);
      _persisted.set(id, { type: rec.type, json, deleted: false });
    }
  });

  _persisted.forEach((prev, id) => {
    if (!prev.deleted && !current.has(id)) {
      puts.push({ id, type: prev.type, data: null, updatedAt: Date.now(), deleted: true });
      previous.set(id, prev);
      _persisted.set(id, { type: prev.type, json: null, deleted: true });
    }
  });

  if (puts.length === 0) return _saveChain;

  _saveChain = _saveChain.then(() => idbWriteRecords(puts)).then(() => {
    clearStorageError();
  }).catch(err => {
    // Roll back our bookkeeping so the next save retries these records
    previous.forEach((prev, id) => {
      if (prev === undefined) _persisted.delete(id);
      else _persisted.set(id, prev);
    });
    showStorageError((err && err.message) ? err.message : String(err));
  });
  return _saveChain;
}

// ---------- load ----------
async function loadAppData() {
  const local = readLocalState();
  _localFlags = local.flags || {};

  try {
    _db = await openDB();
  } catch (err) {
    appData = freshAppData();
    showStorageError('Storage unavailable (' + err.message + '). Changes will be lost on reload.');
    return;
  }

  let records = [];
  try {
    records = await idbGetAll('records');
  } catch (err) {
    showStorageError('Could not read saved data: ' + err.message);
  }

  if (records.length > 0) {
    appData = compose(records);
    records.forEach(r => {
      _persisted.set(r.id, { type: r.type, json: r.deleted ? null : stableStringify(r.data), deleted: !!r.deleted });
    });
    _storageReady = true;
  } else if (!_localFlags.legacyMigrated && localStorage.getItem(LEGACY_STORAGE_KEY)) {
    // One-time move from the old single-blob localStorage format. The old key is kept as a fallback copy.
    let legacy = null;
    try { legacy = migrate(JSON.parse(localStorage.getItem(LEGACY_STORAGE_KEY))); } catch (e) { legacy = null; }
    appData = legacy || freshAppData();
    _storageReady = true;
    await persistRecords();
    _localFlags.legacyMigrated = Date.now();
  } else {
    // Brand-new device: defaults are written with updatedAt = 0 so they never overwrite real data during sync.
    appData = freshAppData();
    _storageReady = true;
    _baselineSave = true;
    await persistRecords();
    _baselineSave = false;
  }

  // Device-only state
  if (local.timer && typeof local.timer === 'object') appData.timer = { ...defaultTimerState(), ...local.timer };
  else if (!appData.timer) appData.timer = defaultTimerState();
  if (local.meta && typeof local.meta === 'object') appData.meta = { lastExport: null, lastImport: null, ...local.meta };
  writeLocalState();

  try {
    deviceSnapshots = (await idbGetLocal('snapshots')) || [];
  } catch (e) {
    deviceSnapshots = [];
  }

  // Ask the browser not to evict our data under storage pressure (silently ignored if refused)
  try {
    if (navigator.storage && navigator.storage.persist) navigator.storage.persist();
  } catch (e) { /* ignore */ }
}

// Waits for all pending writes (used before reloads)
function flushSaves() {
  persistRecords();
  return _saveChain;
}

// ---------- device-only safety snapshots (kept: last 3) ----------
function exportableAppData() {
  const copy = JSON.parse(JSON.stringify(appData));
  delete copy.snapshots;
  return copy;
}

function createSafetySnapshot(reason) {
  try {
    deviceSnapshots.unshift({
      timestamp: Date.now(),
      reason: reason || 'Manual snapshot',
      data: JSON.stringify(exportableAppData())
    });
    deviceSnapshots = deviceSnapshots.slice(0, 3);
    if (_db) {
      return idbPutLocal('snapshots', deviceSnapshots).catch(err => {
        showStorageError('Could not store safety snapshot: ' + err.message);
      });
    }
  } catch (e) {
    console.warn('Snapshot error:', e);
  }
  return Promise.resolve();
}

function saveDeviceSnapshots() {
  if (!_db) return Promise.resolve();
  return idbPutLocal('snapshots', deviceSnapshots).catch(err => {
    showStorageError('Could not update safety snapshots: ' + err.message);
  });
}

// Wipes all synced data (creates tombstones so the wipe can propagate), keeps snapshots.
async function wipeAllData() {
  await createSafetySnapshot('Pre-wipe snapshot');
  const keepTimer = defaultTimerState();
  appData = freshAppData();
  appData.timer = keepTimer;
  writeLocalState();
  await flushSaves();
}
"""
