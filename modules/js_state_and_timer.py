# JavaScript State and Timer Engine Module
JS_STATE_AND_TIMER = """
// ==========================================
// 1. DATA STATE, STORAGE & MIGRATION
// ==========================================
const SCHEMA_VERSION = "3";

const DEFAULT_SETTINGS = {
  focusDur: 25,
  shortBreakDur: 5,
  longBreakDur: 15,
  sessionsUntilLongBreak: 4,
  enableBreaks: true,
  enableCounting: true,
  autoStart: false,
  soundAlert: true,
  desktopNotif: false,
  showCountdownTab: true,
  dailyGoalMin: 240,
  customPreset: null
};

const DEFAULT_TAGS = [
  { id: 'tag-1', name: 'Deep Work', color: '#4F5BF0' },
  { id: 'tag-2', name: 'Coding', color: '#2DD4A7' },
  { id: 'tag-3', name: 'Research', color: '#7C5CFF' },
  { id: 'tag-4', name: 'Writing', color: '#FFB648' },
  { id: 'tag-5', name: 'Review', color: '#FF5C6C' }
];

const PALETTE = ['#4F5BF0', '#7C5CFF', '#2DD4A7', '#FF5C6C', '#FFB648', '#FF4FA3'];

function defaultTimerState() {
  return {
    status: 'idle', // 'idle' | 'running' | 'paused'
    mode: 'focus',   // 'focus' | 'shortBreak' | 'longBreak'
    cycleIndex: 0,
    endsAt: null,
    remainingMs: 25 * 60 * 1000,
    plannedMs: 25 * 60 * 1000,
    label: '',
    selectedTagIds: [],
    startedAt: null,
    interruptions: 0,
    linkedBlock: null // { date: 'YYYY-MM-DD', blockId: 'id' }
  };
}

// In-memory app state. Filled by loadAppData() (see storage engine).
let appData = null;

// Upgrades an older exported/legacy object by filling in missing fields.
// Never wipes existing sessions or settings.
function migrate(data) {
  if (!data || typeof data !== 'object') return null;

  data.schemaVersion = SCHEMA_VERSION;

  if (!data.settings || typeof data.settings !== 'object') data.settings = { ...DEFAULT_SETTINGS };
  else data.settings = { ...DEFAULT_SETTINGS, ...data.settings };
  if (!Array.isArray(data.tags) || data.tags.length === 0) data.tags = DEFAULT_TAGS.map(t => ({ ...t }));
  if (!Array.isArray(data.sessions)) data.sessions = [];
  if (!Array.isArray(data.parkedThoughts)) data.parkedThoughts = [];
  if (!Array.isArray(data.dismissedRecentSessionIds)) data.dismissedRecentSessionIds = [];
  if (!data.timer || typeof data.timer !== 'object') data.timer = defaultTimerState();

  if (!data.dayWindow || typeof data.dayWindow !== 'object') data.dayWindow = { startMin: 480, endMin: 1320 };
  if (!data.timeblockPlans || typeof data.timeblockPlans !== 'object') data.timeblockPlans = {};
  if (!Array.isArray(data.timeblockTemplates)) data.timeblockTemplates = [];
  if (!Array.isArray(data.skills)) data.skills = [];
  if (!Array.isArray(data.manualBacklogEntries)) data.manualBacklogEntries = [];
  if (!data.meta || typeof data.meta !== 'object') data.meta = { lastExport: null, lastImport: null };

  // Snapshots are device-only now and must never travel inside data (they used to nest and grow).
  delete data.snapshots;

  removeDemoLeftovers(data);

  return data;
}

// Older versions injected demo items. Remove only items that are provably demo AND untouched.
const DEMO_BLOCK_LABELS = ['Core Engine Architecture', 'Security Audit & Auth', 'Technical Documentation', 'API Schema Review'];
const DEMO_SKILL_IDS = ['skill-swe', 'skill-writing'];

function removeDemoLeftovers(data) {
  let removed = 0;

  const before = data.sessions.length;
  data.sessions = data.sessions.filter(s => !(s && typeof s.id === 'string' && s.id.indexOf('seed-') === 0));
  removed += before - data.sessions.length;

  Object.keys(data.timeblockPlans).forEach(date => {
    const plan = data.timeblockPlans[date];
    if (!plan || !Array.isArray(plan.blocks)) return;
    const n = plan.blocks.length;
    plan.blocks = plan.blocks.filter(b => !(
      b && typeof b.id === 'string' && b.id.indexOf('tb-seed-') === 0 &&
      DEMO_BLOCK_LABELS.includes(b.label) &&
      (b.status || 'planned') === 'planned' &&
      !b.actualMs &&
      !(b.linkedSessionIds && b.linkedSessionIds.length)
    ));
    removed += n - plan.blocks.length;
  });

  // Demo backlog hours, only when their demo skill no longer exists
  const skillIds = new Set(data.skills.map(k => k && k.id));
  const nb = data.manualBacklogEntries.length;
  data.manualBacklogEntries = data.manualBacklogEntries.filter(e => !(
    e && (e.id === 'bk-1' || e.id === 'bk-2') && DEMO_SKILL_IDS.includes(e.skillId) && !skillIds.has(e.skillId)
  ));
  removed += nb - data.manualBacklogEntries.length;

  return removed;
}

// Helpers
function getTodayDateString() {
  const d = new Date();
  return formatDateString(d.getTime());
}

function formatDateString(timestamp) {
  if (!timestamp) return '-';
  const d = new Date(timestamp);
  const m = padZero(d.getMonth() + 1);
  const day = padZero(d.getDate());
  return d.getFullYear() + '-' + m + '-' + day;
}

function padZero(n) {
  return n < 10 ? '0' + n : '' + n;
}

function formatMinutesToHours(min) {
  const h = Math.floor(min / 60);
  const m = Math.round(min % 60);
  if (h === 0) return m + 'm';
  return h + 'h ' + m + 'm';
}

function formatTimeString(timestamp) {
  if (!timestamp) return '-';
  const d = new Date(timestamp);
  return padZero(d.getHours()) + ':' + padZero(d.getMinutes());
}

function minToTimeOfDay(min) {
  const h = Math.floor(min / 60);
  const m = Math.floor(min % 60);
  return padZero(h) + ':' + padZero(m);
}

function timeOfDayToMin(timeStr) {
  if (!timeStr) return 0;
  const parts = timeStr.split(':');
  return (parseInt(parts[0], 10) || 0) * 60 + (parseInt(parts[1], 10) || 0);
}

function getLabelColor(label) {
  if (!label || !label.trim()) return PALETTE[0];
  let hash = 0;
  for (let i = 0; i < label.length; i++) {
    hash = (hash << 5) - hash + label.charCodeAt(i);
    hash |= 0;
  }
  return PALETTE[Math.abs(hash) % PALETTE.length];
}

// ==========================================
// 2. AUDIO & NOTIFICATIONS
// ==========================================
let audioCtx = null;

function playChime() {
  if (!appData.settings.soundAlert) return;
  try {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return;
    if (!audioCtx) audioCtx = new AudioContextClass();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    const now = audioCtx.currentTime;

    const osc1 = audioCtx.createOscillator();
    const gain1 = audioCtx.createGain();
    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(587.33, now);
    gain1.gain.setValueAtTime(0.001, now);
    gain1.gain.exponentialRampToValueAtTime(0.25, now + 0.04);
    gain1.gain.exponentialRampToValueAtTime(0.0001, now + 0.7);
    osc1.connect(gain1);
    gain1.connect(audioCtx.destination);
    osc1.start(now);
    osc1.stop(now + 0.75);

    const osc2 = audioCtx.createOscillator();
    const gain2 = audioCtx.createGain();
    osc2.type = 'sine';
    osc2.frequency.setValueAtTime(880.00, now + 0.18);
    gain2.gain.setValueAtTime(0.001, now + 0.18);
    gain2.gain.exponentialRampToValueAtTime(0.28, now + 0.22);
    gain2.gain.exponentialRampToValueAtTime(0.0001, now + 1.2);
    osc2.connect(gain2);
    gain2.connect(audioCtx.destination);
    osc2.start(now + 0.18);
    osc2.stop(now + 1.25);
  } catch (err) {
    console.warn('Web Audio error:', err);
  }
}

function triggerNotification(title, body) {
  if (!appData.settings.desktopNotif) return;
  if ('Notification' in window && Notification.permission === 'granted') {
    try {
      new Notification(title, { body });
    } catch (e) {
      console.warn('Notification error:', e);
    }
  }
}

// Toast notification system
function showToast(message, color) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  if (color) toast.style.borderColor = color;

  toast.innerHTML = `
    <svg viewBox="0 0 24 24" width="18" height="18" stroke="${color || 'var(--amber)'}" stroke-width="2.2" fill="none">
      <circle cx="12" cy="12" r="10"/>
      <path d="M12 6v6l4 2"/>
    </svg>
    <span>${escapeHTML(message)}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 300ms ease, transform 300ms ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// ==========================================
// 3. TIMER ENGINE (ABSOLUTE TIMESTAMP BASED)
// ==========================================
let timerIntervalId = null;

function getModeDurationMs(mode) {
  if (mode === 'shortBreak') return (appData.settings.shortBreakDur || 5) * 60 * 1000;
  if (mode === 'longBreak') return (appData.settings.longBreakDur || 15) * 60 * 1000;
  return (appData.settings.focusDur || 25) * 60 * 1000;
}

function initTimerEngine() {
  const t = appData.timer;
  const now = Date.now();

  if (t.status === 'running') {
    if (t.endsAt && now >= t.endsAt) {
      finalizeCompletedSession(t.endsAt, true);
      showAwayBanner('Focus session ended while you were away. Saved to log.');
    } else {
      startTicker();
    }
  } else if (t.status === 'paused') {
    renderTimerUI();
  } else {
    t.status = 'idle';
    t.remainingMs = getModeDurationMs(t.mode);
    t.plannedMs = t.remainingMs;
    renderTimerUI();
  }
}

function startTicker() {
  if (timerIntervalId) clearInterval(timerIntervalId);
  timerIntervalId = setInterval(onTimerTick, 250);
  onTimerTick();
}

function stopTicker() {
  if (timerIntervalId) {
    clearInterval(timerIntervalId);
    timerIntervalId = null;
  }
}

function onTimerTick() {
  const t = appData.timer;
  if (t.status !== 'running') {
    stopTicker();
    return;
  }

  const now = Date.now();
  const rem = Math.max(0, t.endsAt - now);
  t.remainingMs = rem;

  if (rem <= 0) {
    stopTicker();
    finalizeCompletedSession(t.endsAt, false);
    return;
  }

  renderTimerUI();
}

function startOrResumeTimer() {
  const t = appData.timer;
  const now = Date.now();

  if (t.status === 'idle') {
    t.status = 'running';
    t.startedAt = now;
    t.interruptions = 0;
    // If not already set by a timeblock launch override
    if (!t.plannedMs || t.remainingMs <= 0) {
      const dur = t.customDurationMs || getModeDurationMs(t.mode);
      t.plannedMs = dur;
      t.remainingMs = dur;
    }
    t.endsAt = now + t.remainingMs;
  } else if (t.status === 'paused') {
    t.status = 'running';
    t.endsAt = now + t.remainingMs;
  }

  saveAppData();
  startTicker();
  renderTimerUI();
}

function pauseTimer() {
  const t = appData.timer;
  if (t.status !== 'running') return;

  const now = Date.now();
  t.remainingMs = Math.max(0, t.endsAt - now);
  t.status = 'paused';
  if (t.mode === 'focus') {
    t.interruptions = (t.interruptions || 0) + 1;
  }

  stopTicker();
  saveAppData();
  renderTimerUI();
}

function resetTimer() {
  stopTicker();
  const t = appData.timer;
  t.status = 'idle';
  const baseDur = t.customDurationMs || getModeDurationMs(t.mode);
  t.remainingMs = baseDur;
  t.plannedMs = baseDur;
  t.endsAt = null;
  t.startedAt = null;
  t.interruptions = 0;
  t.linkedBlock = null;

  saveAppData();
  renderTimerUI();
}

function setTimerDuration(durationMin) {
  const min = parseInt(durationMin, 10);
  if (isNaN(min) || min < 1) return;
  const ms = min * 60 * 1000;
  const t = appData.timer;

  t.customDurationMs = ms;
  t.plannedMs = ms;

  if (t.status === 'idle') {
    t.remainingMs = ms;
  } else if (t.status === 'running') {
    const elapsed = Math.max(0, (t.plannedMs || ms) - (t.remainingMs || 0));
    t.remainingMs = Math.max(1000, ms - elapsed);
    t.endsAt = Date.now() + t.remainingMs;
  } else if (t.status === 'paused') {
    const elapsed = Math.max(0, (t.plannedMs || ms) - (t.remainingMs || 0));
    t.remainingMs = Math.max(1000, ms - elapsed);
  }

  saveAppData();
  renderTimerUI();
  showToast(`Timer duration set to ${min}m`, 'var(--accent)');
}
window.setTimerDuration = setTimerDuration;

function skipTimer() {
  stopTicker();
  advanceToNextSession(false);
}

function endEarlyAndSave() {
  const t = appData.timer;
  if (t.status === 'idle') return;

  const now = Date.now();
  const actualMs = Math.max(1000, now - (t.startedAt || now));
  const sessId = uid('sess');

  const record = {
    id: sessId,
    mode: t.mode,
    label: (t.label && t.label.trim()) ? t.label.trim() : (t.mode === 'focus' ? 'Focus Session' : 'Break'),
    tags: [ ...(t.selectedTagIds || []) ],
    plannedMs: t.plannedMs || getModeDurationMs(t.mode),
    actualMs: actualMs,
    startedAt: t.startedAt || (now - actualMs),
    endedAt: now,
    completed: true,
    interruptions: t.interruptions || 0,
    note: 'Ended early'
  };

  saveSessionRecord(record);
  syncLinkedTimeBlock(record, false);
  checkSkillMilestones(record);

  resetTimer();
  renderAllViews();
}

function finalizeCompletedSession(endedTimestamp, wasAway) {
  const t = appData.timer;
  const now = endedTimestamp || Date.now();
  const planned = t.plannedMs || getModeDurationMs(t.mode);
  const sessId = uid('sess');

  const record = {
    id: sessId,
    mode: t.mode,
    label: (t.label && t.label.trim()) ? t.label.trim() : (t.mode === 'focus' ? 'Focus Session' : 'Break'),
    tags: [ ...(t.selectedTagIds || []) ],
    plannedMs: planned,
    actualMs: planned,
    startedAt: t.startedAt || (now - planned),
    endedAt: now,
    completed: true,
    interruptions: t.interruptions || 0,
    note: ''
  };

  saveSessionRecord(record);
  syncLinkedTimeBlock(record, true);
  checkSkillMilestones(record);

  if (!wasAway) {
    playChime();
    const notifTitle = t.mode === 'focus' ? 'Focus Completed!' : 'Break Over!';
    const notifBody = t.mode === 'focus' ? 'Great focus! Time to take a mindful rest.' : 'Ready to resume focus?';
    triggerNotification(notifTitle, notifBody);
  }

  advanceToNextSession(true);
}

// Sync back to time block if session was started from a block
function syncLinkedTimeBlock(sessionRecord, completed) {
  const linked = appData.timer.linkedBlock;
  if (!linked || !linked.date || !linked.blockId) return;

  const plan = appData.timeblockPlans[linked.date];
  if (!plan || !Array.isArray(plan.blocks)) return;

  const block = plan.blocks.find(b => b.id === linked.blockId);
  if (block) {
    block.actualMs = (block.actualMs || 0) + sessionRecord.actualMs;
    if (!Array.isArray(block.linkedSessionIds)) block.linkedSessionIds = [];
    if (!block.linkedSessionIds.includes(sessionRecord.id)) {
      block.linkedSessionIds.push(sessionRecord.id);
    }
    if (completed || block.actualMs >= (block.durationMin * 60000)) {
      block.status = 'done';
    }
    saveAppData();
  }
  appData.timer.linkedBlock = null;
}

// Check if a completed session pushed any matching skill past a milestone
function checkSkillMilestones(sessionRecord) {
  if (sessionRecord.mode !== 'focus' || !appData.skills || appData.skills.length === 0) return;

  const MILESTONES = [10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 7500, 10000];

  appData.skills.forEach(skill => {
    // Check match
    const matchesLabel = skill.linkedLabels && skill.linkedLabels.includes(sessionRecord.label);
    const matchesTag = skill.linkedTags && skill.linkedTags.some(t => (sessionRecord.tags || []).includes(t));

    if (matchesLabel || matchesTag) {
      // Calculate hours before session
      const totalHoursNow = getSkillTotalHours(skill);
      const totalHoursBefore = Math.max(0, totalHoursNow - (sessionRecord.actualMs / 3600000));

      MILESTONES.forEach(m => {
        if (totalHoursBefore < m && totalHoursNow >= m) {
          showToast(`${skill.name}: ${m} hours milestone reached!`, skill.color);
          triggerJarCelebration(skill.id);
        }
      });
    }
  });
}

function advanceToNextSession(autoTrigger) {
  const t = appData.timer;
  const s = appData.settings;

  if (t.mode === 'focus') {
    if (s.enableBreaks) {
      if (s.enableCounting) {
        t.cycleIndex = ((t.cycleIndex || 0) + 1) % (s.sessionsUntilLongBreak || 4);
        t.mode = (t.cycleIndex === 0) ? 'longBreak' : 'shortBreak';
      } else {
        t.mode = 'shortBreak';
      }
    } else {
      t.mode = 'focus';
    }
  } else {
    t.mode = 'focus';
  }

  t.status = 'idle';
  t.remainingMs = getModeDurationMs(t.mode);
  t.plannedMs = t.remainingMs;
  t.endsAt = null;
  t.startedAt = null;
  t.interruptions = 0;
  t.linkedBlock = null;

  saveAppData();
  renderAllViews();

  if (autoTrigger && s.autoStart) {
    setTimeout(() => {
      startOrResumeTimer();
    }, 400);
  }
}

function saveSessionRecord(record) {
  appData.sessions.unshift(record);
  saveAppData();
}

function showAwayBanner(msg) {
  const b = document.getElementById('away-banner');
  const txt = document.getElementById('away-banner-text');
  if (b && txt) {
    txt.textContent = msg;
    b.classList.add('show');
  }
}
"""
