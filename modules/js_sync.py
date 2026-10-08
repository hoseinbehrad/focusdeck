# JavaScript Cloud Sync Module
JS_SYNC = r"""
// ==========================================
// 13. CLOUD SYNC (Cloudflare Pages Functions + D1)
// ==========================================
// Every local change is saved on the device first and queued in the IndexedDB 'outbox'.
// syncNow() sends queued records, receives everything other devices sent since our cursor,
// and keeps whichever version of each record is newest.
// The app works fully offline; sync simply waits until the server is reachable.

const SYNC_CONFIG_KEY = 'focusdeck.sync.v1';
const DEFAULT_SYNC_SERVER = 'https://focusdeck-6pj.pages.dev';
const SYNC_BATCH = 200;
const SYNC_TIMEOUT_MS = 20000;

let syncConfig = { server: '', token: '', cursor: 0, lastSyncAt: null, lastError: null };
let syncState = 'off'; // off | idle | syncing | offline | error | unauthorized
let _syncRunning = false;
let _syncAgain = false;
let _syncTimer = null;
let _renderDeferred = false;

function loadSyncConfig() {
  try {
    const raw = localStorage.getItem(SYNC_CONFIG_KEY);
    if (raw) syncConfig = { ...syncConfig, ...JSON.parse(raw) };
  } catch (e) { /* ignore */ }
}

function saveSyncConfig() {
  try { localStorage.setItem(SYNC_CONFIG_KEY, JSON.stringify(syncConfig)); } catch (e) { /* ignore */ }
}

// Same server as the page when the app is served from the web; the default server otherwise
// (file:// copy on the PC, Android wrapper).
function defaultSyncServer() {
  const isWeb = (location.protocol === 'https:' || location.protocol === 'http:') && location.hostname !== 'localhost';
  return isWeb ? location.origin : DEFAULT_SYNC_SERVER;
}

function getSyncServer() {
  if (syncConfig.server) return syncConfig.server.replace(/\/+$/, '');
  return defaultSyncServer();
}

function isSyncConfigured() {
  return !!(syncConfig.token && syncConfig.token.length >= 24);
}

// ---------- IndexedDB helpers used only by sync ----------
function idbGetMany(storeName, ids) {
  return new Promise((resolve, reject) => {
    const tx = _db.transaction(storeName, 'readonly');
    const st = tx.objectStore(storeName);
    const out = new Array(ids.length);
    ids.forEach((id, i) => {
      const req = st.get(id);
      req.onsuccess = () => { out[i] = req.result; };
    });
    tx.oncomplete = () => resolve(out);
    tx.onerror = () => reject(tx.error);
  });
}

// Removes sent outbox entries, unless the record changed again while the request was in flight.
function idbClearSentOutbox(sentEntries) {
  return new Promise((resolve, reject) => {
    const tx = _db.transaction('outbox', 'readwrite');
    const st = tx.objectStore('outbox');
    sentEntries.forEach(e => {
      const req = st.get(e.id);
      req.onsuccess = () => {
        if (req.result && req.result.updatedAt === e.updatedAt) st.delete(e.id);
      };
    });
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

function fetchWithTimeout(url, options, ms) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), ms);
  return fetch(url, { ...options, signal: ctrl.signal }).finally(() => clearTimeout(t));
}

// ---------- the sync loop ----------
function scheduleSync(delayMs) {
  if (!isSyncConfigured()) return;
  if (_syncTimer) clearTimeout(_syncTimer);
  _syncTimer = setTimeout(() => { _syncTimer = null; syncNow(); }, delayMs);
}

// Called by the storage engine after every successful local write
function onLocalRecordsWritten() {
  scheduleSync(3000);
}

async function syncNow() {
  if (!isSyncConfigured() || !_storageReady || !_db) { setSyncState('off'); return; }
  if (_syncRunning) { _syncAgain = true; return; }
  if (navigator.onLine === false) { setSyncState('offline'); return; }

  _syncRunning = true;
  setSyncState('syncing');
  let appliedTotal = 0;

  try {
    for (let round = 0; round < 100; round++) {
      await flushSaves();
      const outbox = (await idbGetAll('outbox')).slice(0, SYNC_BATCH);
      const recs = await idbGetMany('records', outbox.map(o => o.id));
      const changes = [];
      recs.forEach(r => {
        if (!r) return;
        changes.push({ id: r.id, type: r.type, data: r.deleted ? null : r.data, updatedAt: r.updatedAt || 0, deleted: !!r.deleted });
      });

      const res = await fetchWithTimeout(getSyncServer() + '/api/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + syncConfig.token },
        body: JSON.stringify({ since: syncConfig.cursor || 0, changes })
      }, SYNC_TIMEOUT_MS);

      if (res.status === 401) {
        syncConfig.lastError = 'The server rejected the sync key';
        saveSyncConfig();
        setSyncState('unauthorized');
        return;
      }
      if (!res.ok) {
        let msg = 'Server error ' + res.status;
        try { const j = await res.json(); if (j && j.error) msg += ': ' + j.error; } catch (e) { /* ignore */ }
        throw Object.assign(new Error(msg), { serverError: true });
      }

      const body = await res.json();
      await idbClearSentOutbox(outbox);
      if (Array.isArray(body.rejected) && body.rejected.length) {
        console.warn('[FocusDeck sync] server rejected records:', body.rejected);
      }
      if (Array.isArray(body.changes) && body.changes.length) {
        appliedTotal += await applyRemoteRecords(body.changes);
      }
      syncConfig.cursor = body.cursor || syncConfig.cursor || 0;
      saveSyncConfig();

      if (!body.hasMore && outbox.length < SYNC_BATCH) break;
    }

    syncConfig.lastSyncAt = Date.now();
    syncConfig.lastError = null;
    saveSyncConfig();
    setSyncState('idle');
    if (appliedTotal > 0) refreshAfterRemoteChanges();
  } catch (err) {
    syncConfig.lastError = (err && err.message) ? err.message : String(err);
    saveSyncConfig();
    // Network failures (blocked, no VPN, offline) are not errors: data is safe locally and will sync later.
    setSyncState(err && err.serverError ? 'error' : 'offline');
    if (appliedTotal > 0) refreshAfterRemoteChanges();
  } finally {
    _syncRunning = false;
    if (_syncAgain) { _syncAgain = false; scheduleSync(500); }
  }
}

// Replace in-memory data with the merged result and redraw.
// If the person is typing in a field, redraw after they leave it so the cursor isn't lost.
function refreshAfterRemoteChanges() {
  // appData was already rebuilt inside applyRemoteRecords; only redraw here.
  if (isTypingInField()) {
    _renderDeferred = true;
    return;
  }
  safeRenderAll();
}

function isTypingInField() {
  const el = document.activeElement;
  if (!el) return false;
  const tag = el.tagName;
  return (tag === 'TEXTAREA' || tag === 'SELECT' || (tag === 'INPUT' && !['button', 'checkbox', 'radio', 'submit', 'file'].includes(el.type)) || el.isContentEditable);
}

function safeRenderAll() {
  _renderDeferred = false;
  try {
    renderAllViews();
    if (typeof updateBackupTimestampsUI === 'function') updateBackupTimestampsUI();
  } catch (e) {
    console.warn('[FocusDeck sync] render after sync failed:', e);
  }
}

// ---------- status display ----------
function formatAgo(ts) {
  if (!ts) return 'never';
  const s = Math.round((Date.now() - ts) / 1000);
  if (s < 45) return 'just now';
  const m = Math.round(s / 60);
  if (m < 60) return m + 'm ago';
  const h = Math.round(m / 60);
  if (h < 24) return h + 'h ago';
  return formatDateString(ts);
}

function setSyncState(state) {
  syncState = state;
  renderSyncStatus();
}

function renderSyncStatus() {
  const labels = {
    off: 'Sync off',
    idle: 'Synced ' + formatAgo(syncConfig.lastSyncAt),
    syncing: 'Syncing...',
    offline: 'Offline · will sync later',
    error: 'Sync error',
    unauthorized: 'Sync key rejected'
  };
  const text = labels[syncState] || 'Sync off';

  const box = document.getElementById('sync-status');
  if (box) {
    box.dataset.state = syncState;
    box.title = syncConfig.lastError ? syncConfig.lastError : text;
    const t = document.getElementById('sync-status-text');
    if (t) t.textContent = text;
  }

  const s = document.getElementById('sync-settings-status');
  if (s) {
    let detail = text;
    if (syncConfig.lastSyncAt) detail += ' · last success ' + formatDateString(syncConfig.lastSyncAt) + ' ' + formatTimeString(syncConfig.lastSyncAt);
    if (syncConfig.lastError && syncState !== 'idle' && syncState !== 'syncing') detail += ' · ' + syncConfig.lastError;
    s.textContent = detail;
    s.dataset.state = syncState;
  }

  const connected = isSyncConfigured();
  const show = (id, on) => { const el = document.getElementById(id); if (el) el.style.display = on ? '' : 'none'; };
  show('sync-connect-form', !connected);
  show('sync-connected-actions', connected);
  const srv = document.getElementById('sync-server-label');
  if (srv) srv.textContent = getSyncServer();
}

// ---------- settings: connect / disconnect ----------
async function connectSync() {
  const tokenEl = document.getElementById('sync-token-input');
  const serverEl = document.getElementById('sync-server-input');
  const token = (tokenEl.value || '').trim();
  const server = (serverEl.value || '').trim().replace(/\/+$/, '');

  if (token.length < 24) {
    showToast('The sync key must be at least 24 characters', 'var(--coral)');
    return;
  }
  if (server && !/^https?:\/\//.test(server)) {
    showToast('Server must start with https://', 'var(--coral)');
    return;
  }

  const base = server || defaultSyncServer();
  const statusEl = document.getElementById('sync-settings-status');
  if (statusEl) statusEl.textContent = 'Checking key with ' + base + ' ...';

  try {
    const res = await fetchWithTimeout(base + '/api/status', { headers: { 'Authorization': 'Bearer ' + token } }, SYNC_TIMEOUT_MS);
    if (res.status === 401) {
      if (statusEl) statusEl.textContent = 'Key rejected by the server. Check for typos.';
      return;
    }
    if (!res.ok) {
      let msg = 'Server error ' + res.status;
      try { const j = await res.json(); if (j && j.error) msg += ': ' + j.error; } catch (e) { /* ignore */ }
      if (statusEl) statusEl.textContent = msg;
      return;
    }
  } catch (err) {
    if (statusEl) statusEl.textContent = 'Could not reach ' + base + '. If you are in Iran, turn your VPN on and try again.';
    return;
  }

  syncConfig.token = token;
  syncConfig.server = server;
  syncConfig.cursor = 0; // full catch-up on first connect
  syncConfig.lastError = null;
  saveSyncConfig();
  tokenEl.value = '';
  showToast('Cloud sync connected', 'var(--teal)');
  renderSyncStatus();
  syncNow();
}

function disconnectSync() {
  if (!confirm('Stop syncing this device? Your data stays on this device and in the cloud.')) return;
  syncConfig.token = '';
  syncConfig.lastError = null;
  saveSyncConfig();
  setSyncState('off');
}

function initSyncView() {
  loadSyncConfig();

  const connectBtn = document.getElementById('btn-sync-connect');
  if (connectBtn) connectBtn.addEventListener('click', connectSync);
  const tokenEl = document.getElementById('sync-token-input');
  if (tokenEl) tokenEl.addEventListener('keydown', e => { if (e.key === 'Enter') connectSync(); });
  const nowBtn = document.getElementById('btn-sync-now');
  if (nowBtn) nowBtn.addEventListener('click', () => syncNow());
  const discBtn = document.getElementById('btn-sync-disconnect');
  if (discBtn) discBtn.addEventListener('click', disconnectSync);
  const sb = document.getElementById('sync-status');
  if (sb) sb.addEventListener('click', () => {
    if (isSyncConfigured()) syncNow();
    else switchView('settings');
  });

  // Redraw postponed by sync once the person leaves the field they were typing in
  document.addEventListener('focusout', () => {
    setTimeout(() => { if (_renderDeferred && !isTypingInField()) safeRenderAll(); }, 50);
  });

  window.addEventListener('online', () => syncNow());
  document.addEventListener('visibilitychange', () => { if (!document.hidden) syncNow(); });
  setInterval(() => { if (!document.hidden) syncNow(); }, 60000);
  setInterval(renderSyncStatus, 30000);

  setSyncState(isSyncConfigured() ? 'idle' : 'off');
  if (isSyncConfigured()) syncNow();
}
"""
