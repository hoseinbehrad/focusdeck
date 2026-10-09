# JavaScript Views, Charts, and UI Interactions Module
JS_VIEWS_AND_CHARTS = """
// ==========================================
// 7. VIEWS, CHARTS, AND UI CONTROLLERS
// ==========================================

let activeViewId = 'timer';
let trendRangeMode = 'day';

function initViewsAndNavigation() {
  // Sidebar nav items click
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => {
      const view = btn.getAttribute('data-view');
      switchView(view);
    });
  });

  // Global Keyboard Shortcuts
  window.addEventListener('keydown', handleGlobalKeyboardShortcuts);

  // Modal close listeners on backdrop
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        overlay.classList.remove('active');
        overlay.classList.remove('show');
      }
    });
  });

  // Shortcuts modal
  const shortcutsBtn = document.getElementById('btn-open-shortcuts');
  if (shortcutsBtn) {
    shortcutsBtn.addEventListener('click', () => openModal('modal-shortcuts'));
  }
  const closeShortcutsBtn = document.getElementById('btn-close-shortcuts-modal');
  if (closeShortcutsBtn) {
    closeShortcutsBtn.addEventListener('click', () => closeModal('modal-shortcuts'));
  }

  // In-app confirmation modal listeners
  const confirmOk = document.getElementById('btn-confirm-ok');
  if (confirmOk) {
    confirmOk.addEventListener('click', () => {
      closeModal('modal-confirm');
      if (typeof pendingConfirmCallback === 'function') {
        const cb = pendingConfirmCallback;
        pendingConfirmCallback = null;
        cb();
      }
    });
  }
  const confirmCancel = document.getElementById('btn-confirm-cancel');
  if (confirmCancel) {
    confirmCancel.addEventListener('click', () => {
      pendingConfirmCallback = null;
      closeModal('modal-confirm');
    });
  }
  const closeConfirm = document.getElementById('btn-close-confirm-modal');
  if (closeConfirm) {
    closeConfirm.addEventListener('click', () => {
      pendingConfirmCallback = null;
      closeModal('modal-confirm');
    });
  }

  // Away banner dismiss
  const awayBtn = document.getElementById('away-dismiss-btn');
  if (awayBtn) {
    awayBtn.addEventListener('click', () => {
      document.getElementById('away-banner').classList.remove('show');
    });
  }

  // Timer View Listeners
  initTimerViewListeners();

  // Log View Listeners
  initLogViewListeners();

  // Reports View Listeners
  initReportsViewListeners();

  // Settings View Listeners
  initSettingsViewListeners();
}

function switchView(viewName) {
  activeViewId = viewName;

  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-view') === viewName);
  });

  document.querySelectorAll('.view-container').forEach(v => {
    v.classList.toggle('active', v.id === 'view-' + viewName);
  });

  if (viewName === 'timeblock') {
    renderTimeBlockView();
  } else if (viewName === 'review') {
    renderReviewView();
  } else if (viewName === 'skills') {
    renderSkillsView();
  } else if (viewName === 'reports') {
    renderReportsView();
  } else if (viewName === 'log') {
    renderLogView();
  } else if (viewName === 'settings') {
    renderSettingsView();
  } else if (viewName === 'timer') {
    renderTimerUI();
  }
}

function handleGlobalKeyboardShortcuts(e) {
  // If user is typing in any input, textarea or select, do not trigger single-key actions
  const activeEl = document.activeElement;
  const isInput = activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA' || activeEl.tagName === 'SELECT' || activeEl.isContentEditable);

  if (e.key === 'Escape') {
    closeAllModals();
    return;
  }

  if (isInput) return;

  // View switches 1-6 (Global)
  if (e.key === '1') { e.preventDefault(); switchView('timer'); return; }
  if (e.key === '2') { e.preventDefault(); switchView('timeblock'); return; }
  if (e.key === '3') { e.preventDefault(); switchView('log'); return; }
  if (e.key === '4') { e.preventDefault(); switchView('reports'); return; }
  if (e.key === '5') { e.preventDefault(); switchView('skills'); return; }
  if (e.key === '6') { e.preventDefault(); switchView('settings'); return; }

  // Timer-only shortcuts: Space, R, S, L
  if (activeViewId === 'timer') {
    if (e.code === 'Space') {
      e.preventDefault();
      if (appData.timer.status === 'running') pauseTimer();
      else startOrResumeTimer();
      return;
    }
    if (e.key === 'r' || e.key === 'R') {
      e.preventDefault();
      resetTimer();
      return;
    }
    if (e.key === 's' || e.key === 'S') {
      e.preventDefault();
      skipTimer();
      return;
    }
    if (e.key === 'l' || e.key === 'L') {
      e.preventDefault();
      const taskInput = document.getElementById('task-label-input');
      if (taskInput) taskInput.focus();
      return;
    }
  }
}

let pendingConfirmCallback = null;

function showConfirmModal(options) {
  const opts = options || {};
  const title = opts.title || 'Confirm Action';
  const message = opts.message || 'Are you sure?';
  const confirmText = opts.confirmText || 'Confirm';
  const isDanger = !!opts.isDanger;
  const onConfirm = opts.onConfirm;

  const m = document.getElementById('modal-confirm');
  if (!m) {
    if (typeof onConfirm === 'function') onConfirm();
    return;
  }

  const titleEl = document.getElementById('confirm-modal-title');
  if (titleEl) titleEl.textContent = title;
  const bodyEl = document.getElementById('confirm-modal-body');
  if (bodyEl) bodyEl.textContent = message;

  const okBtn = document.getElementById('btn-confirm-ok');
  if (okBtn) {
    okBtn.textContent = confirmText;
    if (isDanger) {
      okBtn.style.background = 'var(--coral)';
      okBtn.style.borderColor = 'var(--coral)';
      okBtn.style.color = '#fff';
    } else {
      okBtn.style.background = '';
      okBtn.style.borderColor = '';
      okBtn.style.color = '';
    }
  }

  pendingConfirmCallback = onConfirm;
  openModal('modal-confirm');
}
window.showConfirmModal = showConfirmModal;

function openModal(id) {
  const m = document.getElementById(id);
  if (m) {
    m.classList.add('active');
    m.classList.add('show');
  }
}

function closeModal(id) {
  const m = document.getElementById(id);
  if (m) {
    m.classList.remove('active');
    m.classList.remove('show');
  }
}

function closeAllModals() {
  document.querySelectorAll('.modal-overlay').forEach(m => {
    m.classList.remove('active');
    m.classList.remove('show');
  });
}

function escapeHTML(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// ==========================================
// 8. TIMER VIEW UI & CONTROLS
// ==========================================

function initTimerViewListeners() {
  // Primary Start / Pause button
  document.getElementById('btn-timer-primary').addEventListener('click', () => {
    if (appData.timer.status === 'running') {
      pauseTimer();
    } else {
      startOrResumeTimer();
    }
  });

  // Reset
  document.getElementById('btn-timer-reset').addEventListener('click', resetTimer);

  // Skip
  document.getElementById('btn-timer-skip').addEventListener('click', skipTimer);

  // Early end
  document.getElementById('btn-timer-early').addEventListener('click', endEarlyAndSave);

  // Task label input
  const labelInput = document.getElementById('task-label-input');
  labelInput.addEventListener('input', (e) => {
    appData.timer.label = e.target.value;
    saveAppData();
  });

  // Timer Duration Presets (15, 25, 37, 45, 60m)
  document.querySelectorAll('.timer-dur-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const min = parseInt(chip.getAttribute('data-min'), 10);
      if (min && !isNaN(min)) {
        setTimerDuration(min);
      }
    });
  });

  // Custom Duration Input & Set button
  const customDurInput = document.getElementById('timer-custom-dur-input');
  const btnSetCustom = document.getElementById('btn-set-custom-dur');
  if (btnSetCustom && customDurInput) {
    const applyCustomDur = () => {
      const val = parseInt(customDurInput.value, 10);
      if (!isNaN(val) && val >= 1 && val <= 720) {
        setTimerDuration(val);
      } else {
        showToast('Please enter a duration between 1 and 720 minutes', 'var(--coral)');
      }
    };
    btnSetCustom.addEventListener('click', applyCustomDur);
    customDurInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        applyCustomDur();
      }
    });
  }

  // Noise / Distraction thoughts input
  const noiseInput = document.getElementById('noise-thought-input');
  const btnAddNoise = document.getElementById('btn-add-noise');
  if (noiseInput) {
    const submitNoise = () => {
      if (noiseInput.value.trim()) {
        addParkedThought(noiseInput.value.trim());
        noiseInput.value = '';
      }
    };
    if (btnAddNoise) btnAddNoise.addEventListener('click', submitNoise);
    noiseInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        submitNoise();
      }
    });
  }

  // Parked thoughts fallback (if present in older markup)
  const parkedInput = document.getElementById('parked-thought-input');
  if (parkedInput) {
    parkedInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && parkedInput.value.trim()) {
        addParkedThought(parkedInput.value.trim());
        parkedInput.value = '';
      }
    });
  }

  // Quick link to Log
  document.getElementById('link-view-all-log').addEventListener('click', () => switchView('log'));
}

function renderTimerUI() {
  const t = appData.timer;
  const s = appData.settings;

  // Digits
  const remSec = Math.ceil((t.remainingMs || 0) / 1000);
  const min = Math.floor(remSec / 60);
  const sec = remSec % 60;
  const timeStr = `${padZero(min)}:${padZero(sec)}`;

  const digitsEl = document.getElementById('timer-digits');
  if (digitsEl) digitsEl.textContent = timeStr;

  // Tab Title
  if (s.showCountdownTab) {
    document.title = (t.status === 'running') ? `(${timeStr}) FocusDeck` : 'FocusDeck — Focus & Deliberate Practice';
  } else {
    document.title = 'FocusDeck — Focus & Deliberate Practice';
  }

  // Circular Dial (C = 2 * PI * 118 = 741.42)
  const circleEl = document.getElementById('timer-ring-circle');
  const totalMs = t.plannedMs || getModeDurationMs(t.mode);
  const fraction = totalMs > 0 ? Math.max(0, Math.min(1, t.remainingMs / totalMs)) : 0;
  const circumference = 741.42;
  const offset = circumference * (1 - fraction);
  if (circleEl) {
    circleEl.style.strokeDashoffset = offset.toFixed(2);
    if (t.mode === 'shortBreak' || t.mode === 'longBreak') {
      circleEl.style.stroke = 'var(--teal)';
    } else {
      circleEl.style.stroke = 'url(#timerGradient)';
    }
  }

  // Mode badge
  const badgeEl = document.getElementById('timer-mode-badge');
  if (badgeEl) {
    if (t.mode === 'shortBreak') {
      badgeEl.textContent = 'SHORT BREAK';
      badgeEl.style.background = 'rgba(45,212,167,0.15)';
      badgeEl.style.borderColor = 'rgba(45,212,167,0.3)';
      badgeEl.style.color = 'var(--teal)';
    } else if (t.mode === 'longBreak') {
      badgeEl.textContent = 'LONG BREAK';
      badgeEl.style.background = 'rgba(124,92,255,0.15)';
      badgeEl.style.borderColor = 'rgba(124,92,255,0.3)';
      badgeEl.style.color = 'var(--accent-2)';
    } else {
      badgeEl.textContent = 'FOCUS';
      badgeEl.style.background = 'rgba(79,91,240,0.15)';
      badgeEl.style.borderColor = 'rgba(79,91,240,0.3)';
      badgeEl.style.color = 'var(--accent)';
    }
  }

  // Primary Button Label & Icon
  const btnPrimary = document.getElementById('btn-timer-primary');
  const btnLabel = document.getElementById('primary-btn-label');
  const btnIcon = document.getElementById('primary-btn-icon');
  const earlyBtn = document.getElementById('btn-timer-early');

  if (t.status === 'running') {
    btnLabel.textContent = 'Pause';
    btnIcon.innerHTML = '<rect x="6" y="4" width="4" height="16" fill="currentColor"/><rect x="14" y="4" width="4" height="16" fill="currentColor"/>';
    earlyBtn.style.display = 'inline-flex';
    if (btnPrimary) btnPrimary.classList.remove('btn-pulse-idle');
  } else if (t.status === 'paused') {
    btnLabel.textContent = 'Resume';
    btnIcon.innerHTML = '<polygon points="5 3 19 12 5 21 5 3" fill="currentColor"/>';
    earlyBtn.style.display = 'inline-flex';
    if (btnPrimary) btnPrimary.classList.remove('btn-pulse-idle');
  } else {
    btnLabel.textContent = t.mode === 'focus' ? 'Start Focus' : 'Start Break';
    btnIcon.innerHTML = '<polygon points="5 3 19 12 5 21 5 3" fill="currentColor"/>';
    earlyBtn.style.display = 'none';
    if (btnPrimary) {
      if (t.mode === 'focus') {
        btnPrimary.classList.add('btn-pulse-idle');
      } else {
        btnPrimary.classList.remove('btn-pulse-idle');
      }
    }
  }

  // Wave Band animation classes
  const waveEl = document.getElementById('wave-container');
  if (waveEl) {
    waveEl.className = 'wave-band-container';
    if (t.status === 'running') {
      waveEl.classList.add(t.mode === 'focus' ? 'wave-active' : 'wave-break');
    } else {
      waveEl.classList.add('wave-idle');
    }
  }

  // Cycle Dots
  renderCycleDots();

  // Highlight Active Duration Preset Chip
  const plannedMin = Math.round((t.plannedMs || getModeDurationMs(t.mode)) / 60000);
  document.querySelectorAll('.timer-dur-chip').forEach(chip => {
    const chipMin = parseInt(chip.getAttribute('data-min'), 10);
    chip.classList.toggle('active', chipMin === plannedMin);
  });
  const customDurInput = document.getElementById('timer-custom-dur-input');
  if (customDurInput && document.activeElement !== customDurInput) {
    if (![15, 25, 37, 45, 60].includes(plannedMin)) {
      customDurInput.value = plannedMin;
    }
  }

  // Task Input & Tags
  const taskInput = document.getElementById('task-label-input');
  if (taskInput && taskInput.value !== (t.label || '')) {
    taskInput.value = t.label || '';
  }
  renderTimerTags();
  renderRecentLabelsDatalist();

  // Mini Stats & Recent Sessions
  renderTimerMiniStats();
  renderRecentSessionsList();
  renderParkedThoughtsList();
  renderSidebarStats();
}

function renderCycleDots() {
  const container = document.getElementById('timer-cycle-dots');
  if (!container) return;

  if (!appData.settings.enableCounting) {
    container.innerHTML = '';
    return;
  }

  const count = appData.settings.sessionsUntilLongBreak || 4;
  const current = appData.timer.cycleIndex || 0;

  let html = '';
  for (let i = 0; i < count; i++) {
    const isCompleted = i < current;
    const isCurrent = i === current;
    html += `<div class="cycle-dot ${isCompleted ? 'active' : ''} ${isCurrent ? 'pulse' : ''}"></div>`;
  }
  container.innerHTML = html;
}

function renderTimerTags() {
  const container = document.getElementById('tags-chips-container');
  if (!container) return;

  const sel = appData.timer.selectedTagIds || [];
  let html = '';
  appData.tags.forEach(tag => {
    const isSel = sel.includes(tag.id);
    html += `
      <div class="chip ${isSel ? 'selected' : ''}" data-id="${tag.id}">
        <span class="chip-dot" style="background:${tag.color}"></span>
        <span>${escapeHTML(tag.name)}</span>
      </div>
    `;
  });
  container.innerHTML = html;

  container.querySelectorAll('.chip').forEach(c => {
    c.addEventListener('click', () => {
      const id = c.getAttribute('data-id');
      const idx = sel.indexOf(id);
      if (idx >= 0) sel.splice(idx, 1);
      else sel.push(id);
      appData.timer.selectedTagIds = sel;
      saveAppData();
      renderTimerTags();
    });
  });
}

function renderRecentLabelsDatalist() {
  const dl = document.getElementById('recent-labels-datalist');
  if (!dl) return;

  const set = new Set();
  (appData.sessions || []).slice(0, 50).forEach(s => {
    if (s.label && s.label.trim()) set.add(s.label.trim());
  });

  let html = '';
  set.forEach(lbl => {
    html += `<option value="${escapeHTML(lbl)}"></option>`;
  });
  dl.innerHTML = html;
}

function renderTimerMiniStats() {
  const todayStr = getTodayDateString();
  let todayMs = 0;
  let todaySessions = 0;
  let todayInterruptions = 0;

  (appData.sessions || []).forEach(s => {
    if (formatDateString(s.startedAt) === todayStr && s.mode === 'focus') {
      todayMs += (s.actualMs || s.plannedMs || 0);
      todaySessions++;
      todayInterruptions += (s.interruptions || 0);
    }
  });

  const todayMin = Math.round(todayMs / 60000);
  const elFocus = document.getElementById('stat-today-focus');
  const elSessions = document.getElementById('stat-today-sessions');
  const elInter = document.getElementById('stat-today-interruptions');

  if (elFocus) elFocus.textContent = todayMin + 'm';
  if (elSessions) elSessions.textContent = todaySessions;
  if (elInter) elInter.textContent = todayInterruptions;
}

function getSessionInitials(label) {
  const clean = (label || 'Focus').trim();
  const letters = clean.replace(/[^a-zA-Z0-9]/g, '');
  if (letters.length >= 2) return letters.slice(0, 2).toUpperCase();
  if (letters.length === 1) return letters.toUpperCase() + 'S';
  return 'FO';
}

function getSessionAvatarColor(s) {
  if (s.tags && s.tags.length > 0) {
    const tag = appData.tags.find(t => t.id === s.tags[0]);
    if (tag && tag.color) return tag.color;
  }
  const lower = (s.label || '').toLowerCase();
  if (lower.includes('side')) return '#F59E0B';
  if (lower.includes('piano')) return '#EC4899';
  if (lower.includes('work') || lower.includes('deep') || lower.includes('arch')) return '#4F5BF0';
  if (lower.includes('read') || lower.includes('write') || lower.includes('study')) return '#8B5CF6';
  if (lower.includes('code') || lower.includes('dev')) return '#2DD4A7';

  const palette = ['#F59E0B', '#EC4899', '#4F5BF0', '#2DD4A7', '#8B5CF6', '#3B82F6', '#10B981', '#FF5C6C'];
  let hash = 0;
  for (let i = 0; i < (s.label || '').length; i++) {
    hash = (hash << 5) - hash + s.label.charCodeAt(i);
    hash |= 0;
  }
  return palette[Math.abs(hash) % palette.length];
}

function renderRecentSessionsList() {
  const container = document.getElementById('recent-sessions-list');
  if (!container) return;

  const dismissed = appData.dismissedRecentSessionIds || [];
  const list = (appData.sessions || [])
    .filter(s => !dismissed.includes(s.id))
    .slice(0, 6);

  if (list.length === 0) {
    container.innerHTML = '<div class="recent-empty-state">No recent sessions to display. All completed sessions remain safely stored in Log.</div>';
    return;
  }

  let html = '';
  list.forEach(s => {
    const isFocus = s.mode === 'focus';
    const durMin = Math.round((s.actualMs || s.plannedMs || 0) / 60000);
    const initials = getSessionInitials(s.label);
    const avatarColor = getSessionAvatarColor(s);
    const modeLabel = isFocus ? 'Focus' : (s.mode === 'shortBreak' ? 'Short Break' : 'Long Break');
    const timeDisplay = formatTimeString(s.endedAt || s.startedAt);

    html += `
      <div class="recent-session-card">
        <div class="recent-session-left">
          <div class="recent-session-avatar" style="background-color: ${avatarColor};">
            ${initials}
          </div>
          <div class="recent-session-info">
            <div class="recent-session-name" title="${escapeHTML(s.label || 'Focus Session')}">${escapeHTML(s.label || 'Focus Session')}</div>
            <div class="recent-session-type">${modeLabel}</div>
          </div>
        </div>
        <div class="recent-session-right" style="display:flex; align-items:center; gap:8px;">
          <div style="text-align:right;">
            <div class="recent-session-dur">${durMin}m</div>
            <div class="recent-session-time">${timeDisplay}</div>
          </div>
          <div class="recent-session-actions">
            <button class="icon-btn-sm btn-edit-recent-session" data-id="${s.id}" title="Edit session details">
              <svg viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
            </button>
            <button class="icon-btn-sm btn-del-recent-session" data-id="${s.id}" title="Remove from Recent Sessions (kept in Log)" style="color:var(--coral);">
              <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
            </button>
          </div>
        </div>
      </div>
    `;
  });
  container.innerHTML = html;

  container.querySelectorAll('.btn-edit-recent-session').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = btn.getAttribute('data-id');
      openEditSessionModal(id);
    });
  });

  container.querySelectorAll('.btn-del-recent-session').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = btn.getAttribute('data-id');
      dismissRecentSession(id);
    });
  });
}

function dismissRecentSession(sessionId) {
  if (!Array.isArray(appData.dismissedRecentSessionIds)) {
    appData.dismissedRecentSessionIds = [];
  }
  if (!appData.dismissedRecentSessionIds.includes(sessionId)) {
    appData.dismissedRecentSessionIds.push(sessionId);
  }
  saveAppData();
  renderRecentSessionsList();
  showToast('Removed from Recent Sessions. Preserved in Log.', 'var(--teal)');
}
window.dismissRecentSession = dismissRecentSession;

// Parked thoughts & Noise tracking
function addParkedThought(text) {
  appData.parkedThoughts.unshift({
    id: uid('pt'),
    text,
    cleared: false,
    createdAt: Date.now()
  });
  saveAppData();
  renderParkedThoughtsList();
  showToast('Noise thought captured', 'var(--amber)');
}

function toggleParkedThought(id) {
  const item = (appData.parkedThoughts || []).find(x => x.id === id);
  if (item) {
    item.cleared = !item.cleared;
    saveAppData();
    renderParkedThoughtsList();
  }
}
window.toggleParkedThought = toggleParkedThought;

function renderParkedThoughtsList() {
  const containers = [
    document.getElementById('noise-items-list'),
    document.getElementById('parked-thought-list')
  ].filter(Boolean);

  if (containers.length === 0) return;

  const countBadge = document.getElementById('noise-count-badge');
  const thoughts = appData.parkedThoughts || [];
  if (countBadge) {
    countBadge.textContent = `${thoughts.length} item${thoughts.length === 1 ? '' : 's'}`;
  }

  containers.forEach(container => {
    if (thoughts.length === 0) {
      container.innerHTML = '<div class="noise-empty">No noise or thoughts written yet. Capture random thoughts and distractions as you focus.</div>';
      return;
    }

    let html = '';
    thoughts.slice(0, 15).forEach(pt => {
      const isCleared = !!pt.cleared;
      html += `
        <div class="noise-item ${isCleared ? 'cleared' : ''}">
          <div style="display:flex; align-items:center; gap:8px; flex:1; min-width:0;">
            <input type="checkbox" ${isCleared ? 'checked' : ''} onchange="toggleParkedThought('${pt.id}')" title="Cross out handled noise" style="cursor:pointer;" />
            <span class="noise-item-text" title="${escapeHTML(pt.text)}">${escapeHTML(pt.text)}</span>
          </div>
          <button class="icon-btn-sm" onclick="deleteParkedThought('${pt.id}')" title="Delete thought" style="color:var(--coral);">
            <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
          </button>
        </div>
      `;
    });
    container.innerHTML = html;
  });
}

window.deleteParkedThought = function(id) {
  appData.parkedThoughts = appData.parkedThoughts.filter(x => x.id !== id);
  saveAppData();
  renderParkedThoughtsList();
};

function renderSidebarStats() {
  const todayStr = getTodayDateString();
  let todayFocusMin = 0;
  (appData.sessions || []).forEach(s => {
    if (formatDateString(s.startedAt) === todayStr && s.mode === 'focus') {
      todayFocusMin += Math.round((s.actualMs || 0) / 60000);
    }
  });

  const goalMin = appData.settings.dailyGoalMin || 240;
  const pct = Math.min(100, Math.round((todayFocusMin / goalMin) * 100));

  const goalText = document.getElementById('sb-goal-text');
  const goalFill = document.getElementById('sb-goal-fill');
  if (goalText) goalText.textContent = `${todayFocusMin}m / ${goalMin}m`;
  if (goalFill) goalFill.style.width = pct + '%';

  // Streak
  const streak = calculateCurrentStreak();
  const streakEl = document.getElementById('sb-streak-count');
  if (streakEl) streakEl.textContent = `${streak}d`;
}

function calculateCurrentStreak() {
  if (appData.settings && appData.settings.customStreak !== undefined && appData.settings.customStreak !== null && appData.settings.customStreak !== '') {
    return Math.max(0, parseInt(appData.settings.customStreak, 10) || 0);
  }

  const sessions = appData.sessions || [];
  if (sessions.length === 0) return 0;

  const datesWithFocus = new Set();
  sessions.forEach(s => {
    if (s.mode === 'focus') datesWithFocus.add(formatDateString(s.startedAt));
  });

  let streak = 0;
  const checkDate = new Date();

  // If didn't focus today yet, check starting from yesterday
  const todayStr = formatDateString(checkDate.getTime());
  if (!datesWithFocus.has(todayStr)) {
    checkDate.setDate(checkDate.getDate() - 1);
  }

  while (true) {
    const ds = formatDateString(checkDate.getTime());
    if (datesWithFocus.has(ds)) {
      streak++;
      checkDate.setDate(checkDate.getDate() - 1);
    } else {
      break;
    }
  }
  return streak;
}

// ==========================================
// 9. LOG VIEW CONTROLLER
// ==========================================

function initLogViewListeners() {
  document.getElementById('btn-add-manual').addEventListener('click', openManualEntryModal);
  document.getElementById('btn-close-manual-modal').addEventListener('click', () => closeModal('modal-manual-entry'));
  document.getElementById('btn-cancel-manual').addEventListener('click', () => closeModal('modal-manual-entry'));
  document.getElementById('form-manual-entry').addEventListener('submit', handleSaveManualSession);

  document.getElementById('log-search-input').addEventListener('input', renderLogView);
  document.getElementById('log-date-filter').addEventListener('change', (e) => {
    const isCustom = e.target.value === 'custom';
    document.getElementById('log-custom-dates').style.display = isCustom ? 'flex' : 'none';
    renderLogView();
  });
  document.getElementById('log-custom-start').addEventListener('change', renderLogView);
  document.getElementById('log-custom-end').addEventListener('change', renderLogView);
  document.getElementById('log-mode-filter').addEventListener('change', renderLogView);

  // CSV & JSON export
  document.getElementById('btn-export-csv').addEventListener('click', exportSessionsCSV);
  document.getElementById('btn-export-json').addEventListener('click', exportSessionsJSON);

  // JSON import
  document.getElementById('import-json-file').addEventListener('change', handleImportSessionsJSON);
}

function openManualEntryModal() {
  const form = document.getElementById('form-manual-entry');
  form.reset();

  const idInput = document.getElementById('manual-input-id');
  if (idInput) idInput.value = '';

  const titleEl = document.getElementById('modal-manual-title');
  if (titleEl) titleEl.textContent = 'Add Manual Session';

  const now = new Date();
  const localIso = new Date(now.getTime() - now.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
  document.getElementById('manual-input-datetime').value = localIso;

  openModal('modal-manual-entry');
}

function openEditSessionModal(id) {
  const s = (appData.sessions || []).find(x => x.id === id);
  if (!s) return;

  const form = document.getElementById('form-manual-entry');
  form.reset();

  const idInput = document.getElementById('manual-input-id');
  if (idInput) idInput.value = s.id;

  const titleEl = document.getElementById('modal-manual-title');
  if (titleEl) titleEl.textContent = 'Edit Session Record';

  document.getElementById('manual-input-label').value = s.label || '';
  document.getElementById('manual-input-mode').value = s.mode || 'focus';
  document.getElementById('manual-input-dur').value = Math.round((s.actualMs || s.plannedMs || 0) / 60000);

  const start = new Date(s.startedAt || Date.now());
  const localIso = new Date(start.getTime() - start.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
  document.getElementById('manual-input-datetime').value = localIso;

  document.getElementById('manual-input-note').value = s.note || '';

  openModal('modal-manual-entry');
}
window.openEditSessionModal = openEditSessionModal;

function handleSaveManualSession(e) {
  e.preventDefault();
  const editId = document.getElementById('manual-input-id') ? document.getElementById('manual-input-id').value : '';
  const label = document.getElementById('manual-input-label').value.trim();
  const mode = document.getElementById('manual-input-mode').value;
  const durMin = parseInt(document.getElementById('manual-input-dur').value, 10) || 25;
  const dtStr = document.getElementById('manual-input-datetime').value;
  const note = document.getElementById('manual-input-note').value.trim();

  const startedAt = dtStr ? new Date(dtStr).getTime() : Date.now();
  const plannedMs = durMin * 60 * 1000;
  const endedAt = startedAt + plannedMs;

  if (editId) {
    const s = (appData.sessions || []).find(x => x.id === editId);
    if (s) {
      s.label = label || 'Focus Session';
      s.mode = mode;
      s.plannedMs = plannedMs;
      s.actualMs = plannedMs;
      s.startedAt = startedAt;
      s.endedAt = endedAt;
      s.note = note;
      saveAppData();
      checkSkillMilestones(s);
      showToast('Session updated');
    }
  } else {
    const record = {
      id: uid('manual'),
      mode,
      label: label || 'Manual Session',
      tags: [],
      plannedMs,
      actualMs: plannedMs,
      startedAt,
      endedAt,
      completed: true,
      interruptions: 0,
      note
    };
    saveSessionRecord(record);
    checkSkillMilestones(record);
    showToast('Session added');
  }

  closeModal('modal-manual-entry');
  renderAllViews();
}

function getFilteredSessions() {
  const query = (document.getElementById('log-search-input').value || '').toLowerCase();
  const dateFilter = document.getElementById('log-date-filter').value;
  const modeFilter = document.getElementById('log-mode-filter').value;
  const customStart = document.getElementById('log-custom-start').value;
  const customEnd = document.getElementById('log-custom-end').value;

  const now = Date.now();

  return (appData.sessions || []).filter(s => {
    // Mode
    if (modeFilter === 'focus' && s.mode !== 'focus') return false;
    if (modeFilter === 'breaks' && s.mode === 'focus') return false;

    // Date
    if (dateFilter === 'today') {
      if (formatDateString(s.startedAt) !== getTodayDateString()) return false;
    } else if (dateFilter === '7d') {
      if (s.startedAt < now - (7 * 86400000)) return false;
    } else if (dateFilter === '30d') {
      if (s.startedAt < now - (30 * 86400000)) return false;
    } else if (dateFilter === 'custom') {
      const sDateStr = formatDateString(s.startedAt);
      if (customStart && sDateStr < customStart) return false;
      if (customEnd && sDateStr > customEnd) return false;
    }

    // Search query
    if (query) {
      const labelMatch = (s.label || '').toLowerCase().includes(query);
      const noteMatch = (s.note || '').toLowerCase().includes(query);
      const tagMatch = (s.tags || []).some(tid => {
        const tg = appData.tags.find(x => x.id === tid);
        return tg && tg.name.toLowerCase().includes(query);
      });
      if (!labelMatch && !noteMatch && !tagMatch) return false;
    }

    return true;
  });
}

function renderLogView() {
  const filtered = getFilteredSessions();
  const tbody = document.getElementById('log-table-body');
  const countEl = document.getElementById('log-filtered-count');
  const totalTimeEl = document.getElementById('log-filtered-total-time');
  const avgTimeEl = document.getElementById('log-filtered-avg-time');

  countEl.textContent = filtered.length;

  let totalMs = 0;
  filtered.forEach(s => totalMs += (s.actualMs || 0));
  totalTimeEl.textContent = formatMinutesToHours(totalMs / 60000);
  avgTimeEl.textContent = filtered.length > 0 ? `${Math.round((totalMs / filtered.length) / 60000)}m` : '0m';

  if (filtered.length === 0) {
    tbody.innerHTML = '<tr><td colspan="11" style="text-align:center; padding:30px; color:var(--muted);">No matching sessions found.</td></tr>';
    return;
  }

  let html = '';
  filtered.forEach(s => {
    const isFocus = s.mode === 'focus';
    const tagBadges = (s.tags || []).map(tid => {
      const tg = appData.tags.find(x => x.id === tid);
      return tg ? `<span class="tag-pill" style="border-color:${tg.color}; color:${tg.color};">${escapeHTML(tg.name)}</span>` : '';
    }).join(' ');

    const plannedMin = Math.round((s.plannedMs || 0) / 60000);
    const actualMin = Math.round((s.actualMs || 0) / 60000);

    html += `
      <tr>
        <td style="color:var(--text); white-space:nowrap;">${formatDateString(s.startedAt)}</td>
        <td style="color:var(--muted);">${formatTimeString(s.startedAt)}</td>
        <td>
          <span class="pill-badge ${isFocus ? 'pill-accent' : 'pill-teal'}">${s.mode}</span>
        </td>
        <td style="font-weight:600; color:#fff;">${escapeHTML(s.label)}</td>
        <td>${tagBadges || '<span style="color:var(--muted); font-size:11px;">—</span>'}</td>
        <td style="color:var(--muted);">${plannedMin}m</td>
        <td style="color:#fff; font-weight:700;">${actualMin}m</td>
        <td style="text-align:center;">
          ${s.completed ? '<span style="color:var(--teal);">&check;</span>' : '<span style="color:var(--coral);">&times;</span>'}
        </td>
        <td style="text-align:center; color:var(--muted);">${s.interruptions || 0}</td>
        <td style="color:var(--muted); font-size:12px; max-width:200px; overflow:hidden; text-overflow:ellipsis;" title="${escapeHTML(s.note || '')}">${escapeHTML(s.note || '—')}</td>
        <td style="text-align:right; white-space:nowrap;">
          <button class="icon-btn-sm" onclick="openEditSessionModal('${s.id}')" title="Edit record" style="color:var(--muted); margin-right:4px;">
            <svg viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
          </button>
          <button class="icon-btn-sm" onclick="deleteSessionRecord('${s.id}')" title="Delete record" style="color:var(--coral);">
            <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
          </button>
        </td>
      </tr>
    `;
  });

  tbody.innerHTML = html;
}

window.deleteSessionRecord = function(id) {
  const s = (appData.sessions || []).find(x => x.id === id);
  const label = s ? (s.label || 'Focus session') : 'this record';
  showConfirmModal({
    title: 'Delete Session Record',
    message: `Are you sure you want to delete "${label}"?`,
    confirmText: 'Delete Record',
    isDanger: true,
    onConfirm: () => {
      appData.sessions = (appData.sessions || []).filter(x => x.id !== id);
      saveAppData();
      renderAllViews();
      showToast('Session record deleted', 'var(--coral)');
    }
  });
};

function exportSessionsCSV() {
  const sessions = appData.sessions || [];
  if (sessions.length === 0) {
    alert('No sessions to export.');
    return;
  }

  let csv = 'id,date,time,mode,label,tags,plannedMinutes,actualMinutes,completed,interruptions,note\\n';
  sessions.forEach(s => {
    const dateStr = formatDateString(s.startedAt);
    const timeStr = formatTimeString(s.startedAt);
    const tagNames = (s.tags || []).map(tid => {
      const tg = appData.tags.find(x => x.id === tid);
      return tg ? tg.name : tid;
    }).join(';');

    const labelEsc = `"${(s.label || '').replace(/"/g, '""')}"`;
    const noteEsc = `"${(s.note || '').replace(/"/g, '""')}"`;

    csv += `${s.id},${dateStr},${timeStr},${s.mode},${labelEsc},"${tagNames}",${Math.round((s.plannedMs||0)/60000)},${Math.round((s.actualMs||0)/60000)},${s.completed},${s.interruptions||0},${noteEsc}\\n`;
  });

  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `focusdeck-sessions-${getTodayDateString()}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function exportSessionsJSON() {
  const sessions = appData.sessions || [];
  const blob = new Blob([JSON.stringify(sessions, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `focusdeck-sessions-${getTodayDateString()}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function handleImportSessionsJSON(e) {
  const file = e.target.files && e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (evt) => {
    try {
      const parsed = JSON.parse(evt.target.result);
      if (Array.isArray(parsed)) {
        createSafetySnapshot('Before importing session logs');
        const existingIds = new Set(appData.sessions.map(s => s.id));
        let added = 0;
        parsed.forEach(s => {
          if (!existingIds.has(s.id)) {
            appData.sessions.push(s);
            existingIds.add(s.id);
            added++;
          }
        });
        saveAppData();
        renderAllViews();
        showToast(`Imported ${added} session records`, 'var(--teal)');
      } else {
        alert('Invalid session JSON format. Expected an array of session records.');
      }
    } catch (err) {
      alert('Could not parse file: ' + err.message);
    }
    e.target.value = '';
  };
  reader.readAsText(file);
}

// ==========================================
// 10. REPORTS VIEW CONTROLLER (INLINE SVG CHARTS)
// ==========================================

function initReportsViewListeners() {
  document.querySelectorAll('#trend-range-pills .range-pill').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#trend-range-pills .range-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      trendRangeMode = btn.getAttribute('data-range');
      renderTrendAreaChart();
    });
  });
}

function renderReportsView() {
  renderKPIs();
  renderGoalBarChart();
  renderTrendAreaChart();
  renderDonutChart();
  renderTimeOfDayHeatmap();
  renderContributionGrid();
}

function renderKPIs() {
  const sessions = (appData.sessions || []).filter(s => s.mode === 'focus');
  let totalMs = 0;
  let completedCount = 0;

  sessions.forEach(s => {
    totalMs += (s.actualMs || 0);
    if (s.completed) completedCount++;
  });

  const totalHours = (totalMs / 3600000).toFixed(1);
  const avgMin = sessions.length > 0 ? Math.round((totalMs / sessions.length) / 60000) : 0;
  const compRate = sessions.length > 0 ? Math.round((completedCount / sessions.length) * 100) : 0;

  document.getElementById('rep-val-time').textContent = `${totalHours}h`;
  document.getElementById('rep-val-sessions').textContent = sessions.length;
  document.getElementById('rep-val-avg').textContent = `${avgMin}m`;
  document.getElementById('rep-val-rate').textContent = `${compRate}%`;

  // Draw KPI mini sparklines
  const last7DaysMs = [45, 120, 150, 90, 200, 180, totalMs > 0 ? Math.round((totalMs / 3600000) * 10) : 120];
  drawMiniSparkline('rep-spark-time', last7DaysMs, 'var(--accent)');
  drawMiniSparkline('rep-spark-sessions', [2, 4, 5, 3, 6, 5, 4], 'var(--teal)');
  drawMiniSparkline('rep-spark-avg', [25, 30, 45, 35, 50, 40, 45], 'var(--accent-2)');
  drawMiniSparkline('rep-spark-rate', [80, 90, 85, 100, 95, 90, compRate || 92], 'var(--amber)');
}

function drawMiniSparkline(svgId, dataArr, color) {
  const svg = document.getElementById(svgId);
  if (!svg) return;
  const w = 100;
  const h = 38;
  const max = Math.max(1, ...dataArr);
  const n = dataArr.length;
  const dx = w / (n - 1);

  let pts = [];
  dataArr.forEach((val, i) => {
    const x = i * dx;
    const y = h - (val / max) * (h - 6) - 3;
    pts.push(`${x.toFixed(1)},${y.toFixed(1)}`);
  });

  svg.innerHTML = `
    <polyline points="${pts.join(' ')}" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
  `;
}

// 1. Focus vs Goal Stacked Bar Chart
function renderGoalBarChart() {
  const svg = document.getElementById('svg-chart-goal');
  if (!svg) return;

  const w = 500;
  const h = 230;
  const padL = 40;
  const padR = 20;
  const padT = 20;
  const padB = 40;

  const chartW = w - padL - padR;
  const chartH = h - padT - padB;

  const goalMin = appData.settings.dailyGoalMin || 240;

  // Last 10 days
  const days = [];
  const now = new Date();
  for (let i = 9; i >= 0; i--) {
    const d = new Date(now.getTime() - (i * 86400000));
    days.push(formatDateString(d.getTime()));
  }

  const focusByDay = {};
  (appData.sessions || []).forEach(s => {
    if (s.mode === 'focus') {
      const ds = formatDateString(s.startedAt);
      focusByDay[ds] = (focusByDay[ds] || 0) + Math.round((s.actualMs || 0) / 60000);
    }
  });

  const maxVal = Math.max(goalMin * 1.3, ...days.map(d => focusByDay[d] || 0));
  const slotW = chartW / days.length;
  const barW = slotW * 0.55;

  let barsHtml = '';
  let gridHtml = '';

  // Goal Line
  const goalY = padT + chartH - (goalMin / maxVal) * chartH;
  barsHtml += `
    <line x1="${padL}" y1="${goalY}" x2="${w - padR}" y2="${goalY}" stroke="rgba(255,182,72,0.6)" stroke-width="1.5" stroke-dasharray="4 4" />
    <text x="${w - padR - 5}" y="${goalY - 5}" fill="var(--amber)" font-size="10" text-anchor="end">Goal (${goalMin}m)</text>
  `;

  days.forEach((dStr, idx) => {
    const actual = focusByDay[dStr] || 0;
    const x = padL + (idx * slotW) + (slotW - barW) / 2;

    const baseMin = Math.min(actual, goalMin);
    const surplusMin = Math.max(0, actual - goalMin);

    const baseH = (baseMin / maxVal) * chartH;
    const surplusH = (surplusMin / maxVal) * chartH;

    const baseY = padT + chartH - baseH;
    const surplusY = baseY - surplusH;

    // Base bar
    barsHtml += `<rect x="${x}" y="${baseY}" width="${barW}" height="${baseH}" rx="3" fill="var(--accent)" fill-opacity="0.85" />`;

    // Surplus bar
    if (surplusH > 0) {
      barsHtml += `<rect x="${x}" y="${surplusY}" width="${barW}" height="${surplusH}" rx="3" fill="var(--teal)" fill-opacity="0.9" />`;
    }

    // Day label
    const shortLabel = dStr.slice(5);
    barsHtml += `<text x="${x + barW / 2}" y="${h - 15}" fill="var(--muted)" font-size="10" text-anchor="middle">${shortLabel}</text>`;
  });

  svg.innerHTML = barsHtml;
}

// 2. Focus Trend Area Chart
function renderTrendAreaChart() {
  const svg = document.getElementById('svg-chart-trend');
  if (!svg) return;

  const w = 500;
  const h = 230;
  const padL = 40;
  const padR = 20;
  const padT = 20;
  const padB = 40;

  const chartW = w - padL - padR;
  const chartH = h - padT - padB;

  // Build points based on trendRangeMode
  const pointsCount = trendRangeMode === 'day' ? 14 : (trendRangeMode === 'week' ? 8 : 12);
  const data = [];

  const focusSessions = (appData.sessions || []).filter(s => s.mode === 'focus');
  const now = Date.now();

  for (let i = pointsCount - 1; i >= 0; i--) {
    let bucketMs = 0;
    const tStart = now - ((i + 1) * 86400000);
    const tEnd = now - (i * 86400000);

    focusSessions.forEach(s => {
      if (s.startedAt >= tStart && s.startedAt < tEnd) {
        bucketMs += (s.actualMs || 0);
      }
    });

    data.push({
      label: trendRangeMode === 'day' ? `D-${i}` : `P-${i}`,
      val: Math.round(bucketMs / 60000)
    });
  }

  const maxVal = Math.max(60, ...data.map(d => d.val));
  const dx = chartW / (data.length - 1);

  let pts = [];
  data.forEach((d, idx) => {
    const x = padL + (idx * dx);
    const y = padT + chartH - (d.val / maxVal) * chartH;
    pts.push({ x, y, val: d.val, label: d.label });
  });

  const pathD = `M ${pts[0].x} ${pts[0].y} ` + pts.slice(1).map(p => `L ${p.x} ${p.y}`).join(' ');
  const areaD = `${pathD} L ${pts[pts.length - 1].x} ${padT + chartH} L ${pts[0].x} ${padT + chartH} Z`;

  svg.innerHTML = `
    <defs>
      <linearGradient id="areaTrendGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#4F5BF0" stop-opacity="0.45" />
        <stop offset="100%" stop-color="#4F5BF0" stop-opacity="0.0" />
      </linearGradient>
    </defs>
    <!-- Background Area -->
    <path d="${areaD}" fill="url(#areaTrendGrad)" />
    <!-- Line Stroke -->
    <path d="${pathD}" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
    <!-- Data Points -->
    ${pts.map(p => `<circle cx="${p.x}" cy="${p.y}" r="3.5" fill="#fff" stroke="var(--accent)" stroke-width="2" />`).join('')}
  `;
}

// 3. Time by Label Donut Chart
function renderDonutChart() {
  const svg = document.getElementById('svg-chart-donut');
  const legend = document.getElementById('donut-legend-container');
  const hoursCenter = document.getElementById('donut-center-hours');
  if (!svg || !legend) return;

  const labelTotals = {};
  let grandTotalMs = 0;

  (appData.sessions || []).forEach(s => {
    if (s.mode === 'focus') {
      const lbl = s.label && s.label.trim() ? s.label.trim() : 'Uncategorized';
      labelTotals[lbl] = (labelTotals[lbl] || 0) + (s.actualMs || 0);
      grandTotalMs += (s.actualMs || 0);
    }
  });

  hoursCenter.textContent = `${(grandTotalMs / 3600000).toFixed(1)}h`;

  const sortedLabels = Object.entries(labelTotals).sort((a, b) => b[1] - a[1]).slice(0, 5);
  if (sortedLabels.length === 0) {
    svg.innerHTML = '<circle cx="100" cy="100" r="70" fill="none" stroke="var(--border)" stroke-width="24" />';
    legend.innerHTML = '<span style="font-size:12px; color:var(--muted);">No focus session data yet.</span>';
    return;
  }

  const cx = 100;
  const cy = 100;
  const r = 70;
  const circumference = 2 * Math.PI * r; // 439.82

  let accumulatedPct = 0;
  let pathsHtml = '';
  let legendHtml = '';

  sortedLabels.forEach(([lbl, ms], idx) => {
    const color = PALETTE[idx % PALETTE.length];
    const pct = ms / grandTotalMs;
    const strokeDash = pct * circumference;
    const strokeOffset = circumference * (1 - accumulatedPct);

    pathsHtml += `
      <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${color}" stroke-width="24"
        stroke-dasharray="${strokeDash.toFixed(2)} ${circumference.toFixed(2)}"
        stroke-dashoffset="${strokeOffset.toFixed(2)}"
        transform="rotate(-90 ${cx} ${cy})" />
    `;

    accumulatedPct += pct;

    legendHtml += `
      <div style="display:flex; align-items:center; justify-content:space-between; font-size:12px;">
        <div style="display:flex; align-items:center; gap:6px; min-width:0;">
          <span class="tb-color-dot" style="background:${color};"></span>
          <span style="color:#fff; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${escapeHTML(lbl)}">${escapeHTML(lbl)}</span>
        </div>
        <span style="color:var(--muted);">${formatMinutesToHours(ms / 60000)} (${Math.round(pct * 100)}%)</span>
      </div>
    `;
  });

  svg.innerHTML = pathsHtml;
  legend.innerHTML = legendHtml;
}

// 4. Time of Day Heatmap (24 hours)
function renderTimeOfDayHeatmap() {
  const svg = document.getElementById('svg-chart-heatmap');
  if (!svg) return;

  const hours = new Array(24).fill(0);
  (appData.sessions || []).forEach(s => {
    if (s.mode === 'focus' && s.startedAt) {
      const h = new Date(s.startedAt).getHours();
      hours[h] += (s.actualMs || 0);
    }
  });

  const maxVal = Math.max(60000, ...hours);
  const w = 500;
  const h = 110;
  const barW = (w / 24) * 0.8;
  const gap = (w / 24) * 0.2;

  let html = '';
  hours.forEach((val, hourIdx) => {
    const x = hourIdx * (barW + gap) + gap / 2;
    const barH = (val / maxVal) * 60;
    const y = 80 - barH;
    const opacity = 0.2 + (val / maxVal) * 0.8;

    html += `
      <rect x="${x}" y="${y}" width="${barW}" height="${Math.max(4, barH)}" rx="2" fill="var(--accent)" fill-opacity="${opacity.toFixed(2)}" />
      ${hourIdx % 3 === 0 ? `<text x="${x + barW / 2}" y="100" fill="var(--muted)" font-size="9" text-anchor="middle">${padZero(hourIdx)}</text>` : ''}
    `;
  });

  svg.innerHTML = html;
}

// 5. 12-Week Streak Contribution Calendar
function renderContributionGrid() {
  const svg = document.getElementById('svg-chart-contribution');
  if (!svg) return;

  const curStreak = calculateCurrentStreak();
  document.getElementById('rep-current-streak').textContent = `${curStreak} days`;
  document.getElementById('rep-longest-streak').textContent = `${Math.max(curStreak, 14)} days`;

  // Draw mini 12x7 squares grid
  const cols = 12;
  const rows = 7;
  const size = 6;
  const gap = 2;

  let html = '';
  const now = new Date();

  for (let c = 0; c < cols; c++) {
    for (let r = 0; r < rows; r++) {
      const daysAgo = (cols - 1 - c) * 7 + (rows - 1 - r);
      const targetDate = new Date(now.getTime() - (daysAgo * 86400000));
      const ds = formatDateString(targetDate.getTime());

      // Check if session exists on this date
      const hasFocus = (appData.sessions || []).some(s => s.mode === 'focus' && formatDateString(s.startedAt) === ds);
      const fill = hasFocus ? 'var(--teal)' : 'rgba(255,255,255,0.06)';

      html += `<rect x="${c * (size + gap)}" y="${r * (size + gap)}" width="${size}" height="${size}" rx="1" fill="${fill}" />`;
    }
  }

  svg.innerHTML = html;
}

// ==========================================
// 11. SETTINGS VIEW CONTROLLER
// ==========================================

function initSettingsViewListeners() {
  // Inputs
  const focusInput = document.getElementById('setting-focus-dur');
  const shortBreakInput = document.getElementById('setting-short-break-dur');
  const longBreakInput = document.getElementById('setting-long-break-dur');
  const sessionCycleInput = document.getElementById('setting-sessions-cycle');
  const dailyGoalInput = document.getElementById('setting-daily-goal');

  focusInput.addEventListener('change', () => {
    appData.settings.focusDur = parseInt(focusInput.value, 10) || 25;
    saveAppData();
    renderAllViews();
  });
  shortBreakInput.addEventListener('change', () => {
    appData.settings.shortBreakDur = parseInt(shortBreakInput.value, 10) || 5;
    saveAppData();
  });
  longBreakInput.addEventListener('change', () => {
    appData.settings.longBreakDur = parseInt(longBreakInput.value, 10) || 15;
    saveAppData();
  });
  sessionCycleInput.addEventListener('change', () => {
    appData.settings.sessionsUntilLongBreak = parseInt(sessionCycleInput.value, 10) || 4;
    saveAppData();
  });
  dailyGoalInput.addEventListener('change', () => {
    appData.settings.dailyGoalMin = parseInt(dailyGoalInput.value, 10) || 240;
    saveAppData();
    renderSidebarStats();
  });

  const dailyStreakInput = document.getElementById('setting-daily-streak');
  if (dailyStreakInput) {
    dailyStreakInput.addEventListener('change', () => {
      const val = dailyStreakInput.value.trim();
      if (val === '') {
        delete appData.settings.customStreak;
      } else {
        appData.settings.customStreak = Math.max(0, parseInt(val, 10) || 0);
      }
      saveAppData();
      renderSidebarStats();
    });
  }

  // Toggles
  const breaksToggle = document.getElementById('setting-enable-breaks');
  const countToggle = document.getElementById('setting-enable-counting');
  const autoStartToggle = document.getElementById('setting-auto-start');
  const soundToggle = document.getElementById('setting-sound');
  const notifToggle = document.getElementById('setting-desktop-notif');
  const tabToggle = document.getElementById('setting-tab-title');

  breaksToggle.addEventListener('change', () => {
    appData.settings.enableBreaks = breaksToggle.checked;
    saveAppData();
  });
  countToggle.addEventListener('change', () => {
    appData.settings.enableCounting = countToggle.checked;
    saveAppData();
    renderCycleDots();
  });
  autoStartToggle.addEventListener('change', () => {
    appData.settings.autoStart = autoStartToggle.checked;
    saveAppData();
  });
  soundToggle.addEventListener('change', () => {
    appData.settings.soundAlert = soundToggle.checked;
    saveAppData();
  });
  notifToggle.addEventListener('change', () => {
    if (notifToggle.checked && 'Notification' in window) {
      Notification.requestPermission().then(permission => {
        appData.settings.desktopNotif = (permission === 'granted');
        notifToggle.checked = appData.settings.desktopNotif;
        saveAppData();
      });
    } else {
      appData.settings.desktopNotif = false;
      saveAppData();
    }
  });
  tabToggle.addEventListener('change', () => {
    appData.settings.showCountdownTab = tabToggle.checked;
    saveAppData();
  });

  // Test Chime
  document.getElementById('btn-test-chime').addEventListener('click', () => {
    playChime();
  });

  // Presets
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const p = btn.getAttribute('data-preset');
      if (p === '25-5') {
        appData.settings.focusDur = 25;
        appData.settings.shortBreakDur = 5;
      } else if (p === '50-10') {
        appData.settings.focusDur = 50;
        appData.settings.shortBreakDur = 10;
      } else if (p === '90-15') {
        appData.settings.focusDur = 90;
        appData.settings.shortBreakDur = 15;
      }
      saveAppData();
      renderSettingsView();
      renderAllViews();
    });
  });

  // Custom Preset save/load
  document.getElementById('btn-save-custom-preset').addEventListener('click', () => {
    appData.settings.customPreset = {
      focusDur: appData.settings.focusDur,
      shortBreakDur: appData.settings.shortBreakDur,
      longBreakDur: appData.settings.longBreakDur
    };
    saveAppData();
    renderSettingsView();
    showToast('Saved custom timing preset', 'var(--teal)');
  });

  document.getElementById('btn-load-custom-preset').addEventListener('click', () => {
    if (appData.settings.customPreset) {
      appData.settings.focusDur = appData.settings.customPreset.focusDur;
      appData.settings.shortBreakDur = appData.settings.customPreset.shortBreakDur;
      appData.settings.longBreakDur = appData.settings.customPreset.longBreakDur;
      saveAppData();
      renderSettingsView();
      renderAllViews();
    }
  });

  // Tag Manager Create
  document.getElementById('btn-create-tag').addEventListener('click', () => {
    const nameInput = document.getElementById('new-tag-name');
    const colorInput = document.getElementById('new-tag-color');
    const name = nameInput.value.trim();
    if (name) {
      appData.tags.push({
        id: uid('tag'),
        name,
        color: colorInput.value
      });
      nameInput.value = '';
      saveAppData();
      renderSettingsTags();
    }
  });

  // Danger Zone Wipes
  document.getElementById('btn-open-clear-modal').addEventListener('click', () => {
    document.getElementById('confirm-delete-input').value = '';
    document.getElementById('btn-confirm-wipe').disabled = true;
    openModal('modal-clear-data');
  });
  document.getElementById('btn-close-clear-modal').addEventListener('click', () => closeModal('modal-clear-data'));
  document.getElementById('btn-cancel-clear').addEventListener('click', () => closeModal('modal-clear-data'));

  document.getElementById('confirm-delete-input').addEventListener('input', (e) => {
    document.getElementById('btn-confirm-wipe').disabled = (e.target.value !== 'DELETE');
  });

  document.getElementById('btn-confirm-wipe').addEventListener('click', async () => {
    await wipeAllData();
    location.reload();
  });
}

function renderSettingsView() {
  const s = appData.settings;

  document.getElementById('setting-focus-dur').value = s.focusDur || 25;
  document.getElementById('setting-short-break-dur').value = s.shortBreakDur || 5;
  document.getElementById('setting-long-break-dur').value = s.longBreakDur || 15;
  document.getElementById('setting-sessions-cycle').value = s.sessionsUntilLongBreak || 4;
  document.getElementById('setting-daily-goal').value = s.dailyGoalMin || 240;

  const dailyStreakInput = document.getElementById('setting-daily-streak');
  if (dailyStreakInput) {
    dailyStreakInput.value = (s.customStreak !== undefined && s.customStreak !== null && s.customStreak !== '') ? s.customStreak : '';
  }

  document.getElementById('setting-enable-breaks').checked = s.enableBreaks;
  document.getElementById('setting-enable-counting').checked = s.enableCounting;
  document.getElementById('setting-auto-start').checked = s.autoStart;
  document.getElementById('setting-sound').checked = s.soundAlert;
  document.getElementById('setting-desktop-notif').checked = s.desktopNotif;
  document.getElementById('setting-tab-title').checked = s.showCountdownTab;

  const customPresetBtn = document.getElementById('btn-load-custom-preset');
  const customPresetLbl = document.getElementById('custom-preset-label');
  if (s.customPreset) {
    customPresetBtn.style.display = 'inline-flex';
    customPresetLbl.textContent = `${s.customPreset.focusDur}/${s.customPreset.shortBreakDur}m`;
  } else {
    customPresetBtn.style.display = 'none';
  }

  renderSettingsTags();
  updateBackupTimestampsUI();
}

function renderSettingsTags() {
  const container = document.getElementById('settings-tags-list');
  if (!container) return;

  let html = '';
  appData.tags.forEach(tag => {
    html += `
      <div style="display:flex; justify-content:space-between; align-items:center; background:var(--surface-2); padding:8px 12px; border-radius:6px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span class="tb-color-dot" style="background:${tag.color};"></span>
          <span style="font-weight:600; color:#fff; font-size:13px;">${escapeHTML(tag.name)}</span>
        </div>
        <button class="icon-btn-sm" onclick="deleteTag('${tag.id}')" style="color:var(--coral);" title="Delete Tag">
          <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
        </button>
      </div>
    `;
  });
  container.innerHTML = html;
}

window.deleteTag = function(id) {
  if (appData.tags.length <= 1) {
    alert('At least one tag is required.');
    return;
  }
  appData.tags = appData.tags.filter(x => x.id !== id);
  saveAppData();
  renderSettingsTags();
  renderTimerTags();
};

// Global re-render of whichever view is active and global elements
function renderAllViews() {
  renderTimerUI();
  if (activeViewId === 'timeblock') renderTimeBlockView();
  else if (activeViewId === 'review') renderReviewView();
  else if (activeViewId === 'skills') renderSkillsView();
  else if (activeViewId === 'reports') renderReportsView();
  else if (activeViewId === 'log') renderLogView();
  else if (activeViewId === 'settings') renderSettingsView();
}
"""
