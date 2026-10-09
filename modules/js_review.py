# JavaScript Review Module (end-of-day shutdown review + weekly review)
JS_REVIEW = r"""
// ==========================================
// 15. REVIEWS (daily shutdown + weekly)
// ==========================================
let reviewTab = 'day';        // 'day' | 'week'
let reviewDayDate = null;     // 'YYYY-MM-DD'
let reviewWeekStart = null;   // 'YYYY-MM-DD' (first day of the week)
let _reviewSaveTimer = null;
const REVIEW_PROMPT_KEY = 'focusdeck.reviewPrompt.v1';

// ---------- date helpers ----------
function addDaysStr(dateStr, n) {
  const d = new Date(dateStr + 'T00:00:00');
  d.setDate(d.getDate() + n);
  return formatDateString(d.getTime());
}

function getWeekStartDay() {
  const v = parseInt(appData.settings.weekStart, 10);
  return [0, 1, 6].includes(v) ? v : 6;
}

function weekStartOf(dateStr) {
  const d = new Date(dateStr + 'T00:00:00');
  const diff = (d.getDay() - getWeekStartDay() + 7) % 7;
  d.setDate(d.getDate() - diff);
  return formatDateString(d.getTime());
}

function shortDayLabel(dateStr) {
  const d = new Date(dateStr + 'T00:00:00');
  return d.toLocaleDateString('en-US', { weekday: 'short', day: 'numeric', month: 'short' });
}

function fmtMs(ms) {
  return formatMinutesToHours(Math.round((ms || 0) / 60000));
}

// ---------- calculations ----------
function sessionMatchesSkill(sess, skill) {
  const byLabel = (skill.linkedLabels || []).includes(sess.label);
  const byTag = (skill.linkedTags || []).some(t => (sess.tags || []).includes(t));
  return byLabel || byTag;
}

// Plan vs reality for one day. A block marked done counts as fully kept even without timer time.
function computeDayStats(dateStr) {
  const plan = appData.timeblockPlans[dateStr];
  const blocks = (plan && Array.isArray(plan.blocks)) ? plan.blocks : [];
  const linked = new Set();

  const rows = blocks.map(b => {
    (b.linkedSessionIds || []).forEach(id => linked.add(id));
    const plannedMs = Math.max(0, (b.durationMin || 0) * 60000);
    const actualMs = Math.max(0, b.actualMs || 0);
    const done = b.status === 'done';
    const keptMs = done ? plannedMs : Math.min(actualMs, plannedMs);
    return {
      id: b.id, label: b.label || 'Untitled', color: b.color || PALETTE[0],
      plannedMs, actualMs, keptMs, done,
      status: b.status || 'planned',
      movedTo: b.movedTo || null, movedFrom: b.movedFrom || null,
      unfinished: !done && actualMs < plannedMs && !b.movedTo
    };
  });

  const focus = (appData.sessions || []).filter(s => s.mode === 'focus' && formatDateString(s.startedAt) === dateStr);
  const focusMs = focus.reduce((n, s) => n + (s.actualMs || 0), 0);
  const unplannedMs = focus.filter(s => !linked.has(s.id)).reduce((n, s) => n + (s.actualMs || 0), 0);
  const plannedMs = rows.reduce((n, r) => n + r.plannedMs, 0);
  const keptMs = rows.reduce((n, r) => n + r.keptMs, 0);
  const thoughts = (appData.parkedThoughts || []).filter(t => formatDateString(t.createdAt) === dateStr).length;

  return {
    date: dateStr, rows,
    plannedMs, keptMs, focusMs, unplannedMs,
    keptPct: plannedMs > 0 ? Math.round((keptMs / plannedMs) * 100) : null,
    doneCount: rows.filter(r => r.done).length,
    blockCount: rows.length,
    movedCount: rows.filter(r => r.movedTo).length,
    sessionCount: focus.length,
    thoughts,
    review: (appData.reviews || {})['day:' + dateStr] || null
  };
}

function computeWeekStats(startStr) {
  const days = [];
  for (let i = 0; i < 7; i++) days.push(computeDayStats(addDaysStr(startStr, i)));
  const endStr = addDaysStr(startStr, 6);

  const plannedMs = days.reduce((n, d) => n + d.plannedMs, 0);
  const keptMs = days.reduce((n, d) => n + d.keptMs, 0);
  const focusMs = days.reduce((n, d) => n + d.focusMs, 0);

  const weekSessions = (appData.sessions || []).filter(s => {
    if (s.mode !== 'focus') return false;
    const ds = formatDateString(s.startedAt);
    return ds >= startStr && ds <= endStr;
  });

  const tagMap = new Map();
  weekSessions.forEach(s => {
    const tags = (s.tags && s.tags.length) ? s.tags : ['__none'];
    tags.forEach(t => tagMap.set(t, (tagMap.get(t) || 0) + (s.actualMs || 0)));
  });
  const tagRows = [...tagMap.entries()].map(([id, ms]) => {
    const tag = (appData.tags || []).find(t => t.id === id);
    return { name: tag ? tag.name : 'No tag', color: tag ? tag.color : '#7A83A6', ms };
  }).sort((a, b) => b.ms - a.ms);

  const skillRows = (appData.skills || []).map(sk => ({
    name: sk.name, color: sk.color || PALETTE[0],
    ms: weekSessions.filter(s => sessionMatchesSkill(s, sk)).reduce((n, s) => n + (s.actualMs || 0), 0)
  })).filter(r => r.ms > 0).sort((a, b) => b.ms - a.ms);

  const withFocus = days.filter(d => d.focusMs > 0);
  const best = withFocus.length ? withFocus.reduce((a, b) => (b.focusMs > a.focusMs ? b : a)) : null;
  const planned = days.filter(d => d.plannedMs > 0);
  const worst = planned.length ? planned.reduce((a, b) => ((b.keptPct ?? 0) < (a.keptPct ?? 0) ? b : a)) : null;

  return {
    start: startStr, end: endStr, days,
    plannedMs, keptMs, focusMs,
    keptPct: plannedMs > 0 ? Math.round((keptMs / plannedMs) * 100) : null,
    movedCount: days.reduce((n, d) => n + d.movedCount, 0),
    shutdowns: days.filter(d => d.review && d.review.shutdown).length,
    tagRows, skillRows, best, worst,
    review: (appData.reviews || {})['week:' + startStr] || null
  };
}

// ---------- actions ----------
function getOrCreateReview(key, base) {
  if (!appData.reviews) appData.reviews = {};
  if (!appData.reviews[key]) appData.reviews[key] = { ...base };
  return appData.reviews[key];
}

function saveReviewField(key, base, field, value, immediate) {
  const r = getOrCreateReview(key, base);
  r[field] = value;
  r.savedAt = Date.now();
  const status = document.getElementById('review-save-status-' + (key.startsWith('week:') ? 'week' : 'day'));
  if (status) status.textContent = 'Saving...';
  if (_reviewSaveTimer) clearTimeout(_reviewSaveTimer);
  _reviewSaveTimer = setTimeout(() => {
    saveAppData();
    if (status) status.textContent = 'Saved';
  }, immediate ? 0 : 700);
}

// Copies the selected unfinished blocks to the next day with the time still left on them.
function carryOverBlocks(dateStr, blockIds) {
  const plan = appData.timeblockPlans[dateStr];
  if (!plan || !blockIds.length) return 0;
  const target = addDaysStr(dateStr, 1);
  if (!appData.timeblockPlans[target]) appData.timeblockPlans[target] = { blocks: [], notes: '' };
  const targetPlan = appData.timeblockPlans[target];
  if (!Array.isArray(targetPlan.blocks)) targetPlan.blocks = [];

  let moved = 0;
  plan.blocks.forEach(b => {
    if (!blockIds.includes(b.id) || b.movedTo) return;
    const leftMin = Math.max(5, Math.round(((b.durationMin || 0) * 60000 - (b.actualMs || 0)) / 60000));
    targetPlan.blocks.push({
      id: uid('tb'),
      label: b.label,
      tags: [ ...(b.tags || []) ],
      durationMin: leftMin,
      status: 'planned',
      actualMs: 0,
      linkedSessionIds: [],
      color: b.color,
      movedFrom: dateStr
    });
    b.movedTo = target;
    moved++;
  });
  if (moved) {
    saveAppData();
    showToast(`Moved ${moved} block${moved === 1 ? '' : 's'} to ${shortDayLabel(target)}`, 'var(--teal)');
  }
  return moved;
}

// ---------- rendering ----------
function pctClass(p) {
  if (p === null) return '';
  if (p >= 80) return 'rv-good';
  if (p >= 50) return 'rv-mid';
  return 'rv-bad';
}

function renderReviewView() {
  if (!reviewDayDate) reviewDayDate = getTodayDateString();
  if (!reviewWeekStart) reviewWeekStart = weekStartOf(getTodayDateString());

  document.querySelectorAll('.rv-tab').forEach(b => b.classList.toggle('active', b.dataset.tab === reviewTab));
  document.getElementById('rv-day-panel').style.display = reviewTab === 'day' ? '' : 'none';
  document.getElementById('rv-week-panel').style.display = reviewTab === 'week' ? '' : 'none';

  if (reviewTab === 'day') renderDayReview();
  else renderWeekReview();
}

function renderDayReview() {
  const st = computeDayStats(reviewDayDate);
  const isToday = reviewDayDate === getTodayDateString();
  document.getElementById('rv-day-label').textContent = (isToday ? 'Today · ' : '') + shortDayLabel(reviewDayDate);

  document.getElementById('rv-day-kpis').innerHTML = `
    <div class="card kpi-card"><div class="kpi-title">Plan kept</div>
      <div class="kpi-value ${pctClass(st.keptPct)}">${st.keptPct === null ? '—' : st.keptPct + '%'}</div>
      <div class="rv-kpi-sub">${fmtMs(st.keptMs)} of ${fmtMs(st.plannedMs)} planned</div></div>
    <div class="card kpi-card"><div class="kpi-title">Focus time</div>
      <div class="kpi-value">${fmtMs(st.focusMs)}</div>
      <div class="rv-kpi-sub">${st.sessionCount} session${st.sessionCount === 1 ? '' : 's'} · ${fmtMs(st.unplannedMs)} unplanned</div></div>
    <div class="card kpi-card"><div class="kpi-title">Blocks done</div>
      <div class="kpi-value">${st.doneCount}/${st.blockCount}</div>
      <div class="rv-kpi-sub">${st.movedCount} moved to next day</div></div>
    <div class="card kpi-card"><div class="kpi-title">Distractions noted</div>
      <div class="kpi-value">${st.thoughts}</div>
      <div class="rv-kpi-sub">from the timer's noise list</div></div>`;

  const body = document.getElementById('rv-day-blocks');
  if (!st.rows.length) {
    body.innerHTML = `<tr><td colspan="5" class="rv-empty">No blocks planned for this day.</td></tr>`;
  } else {
    body.innerHTML = st.rows.map(r => {
      const diff = r.actualMs - r.plannedMs;
      const diffTxt = r.actualMs === 0 ? '—' : (diff === 0 ? '0' : (diff > 0 ? '+' : '−') + fmtMs(Math.abs(diff)));
      const status = r.movedTo ? `<span class="rv-pill rv-pill-moved">Moved → ${escapeHTML(shortDayLabel(r.movedTo))}</span>`
        : r.done ? '<span class="rv-pill rv-pill-done">Done</span>'
        : r.actualMs > 0 ? '<span class="rv-pill rv-pill-part">Partial</span>'
        : '<span class="rv-pill rv-pill-open">Not started</span>';
      return `<tr>
        <td><span class="rv-dot" style="background:${escapeHTML(r.color)}"></span>${escapeHTML(r.label)}${r.movedFrom ? ' <span class="rv-carried">carried over</span>' : ''}</td>
        <td>${fmtMs(r.plannedMs)}</td>
        <td>${r.actualMs ? fmtMs(r.actualMs) : '—'}</td>
        <td class="${diff > 0 && r.actualMs ? 'rv-over' : (r.actualMs && diff < 0 ? 'rv-under' : '')}">${diffTxt}</td>
        <td>${status}</td></tr>`;
    }).join('');
  }

  const open = st.rows.filter(r => r.unfinished);
  const carry = document.getElementById('rv-carry-list');
  const carryBtn = document.getElementById('btn-rv-carry');
  if (!open.length) {
    carry.innerHTML = '<div class="rv-empty">Nothing left over. Clean day.</div>';
    carryBtn.style.display = 'none';
  } else {
    carry.innerHTML = open.map(r => {
      const left = Math.max(5, Math.round((r.plannedMs - r.actualMs) / 60000));
      return `<label class="rv-carry-row"><input type="checkbox" class="rv-carry-cb" value="${escapeHTML(r.id)}" checked />
        <span class="rv-dot" style="background:${escapeHTML(r.color)}"></span>
        <span class="rv-carry-label">${escapeHTML(r.label)}</span>
        <span class="rv-carry-left">${formatMinutesToHours(left)} left</span></label>`;
    }).join('');
    carryBtn.style.display = '';
    carryBtn.querySelector('span').textContent = `Move to ${shortDayLabel(addDaysStr(reviewDayDate, 1))}`;
  }

  const rv = st.review || {};
  const noteEl = document.getElementById('rv-day-note');
  if (document.activeElement !== noteEl) noteEl.value = rv.note || '';
  document.getElementById('rv-day-shutdown').checked = !!rv.shutdown;
  const status = document.getElementById('review-save-status-day');
  if (status) status.textContent = rv.savedAt ? 'Saved' : '';
}

function renderWeekReview() {
  const st = computeWeekStats(reviewWeekStart);
  const thisWeek = reviewWeekStart === weekStartOf(getTodayDateString());
  document.getElementById('rv-week-label').textContent = (thisWeek ? 'This week · ' : '') + shortDayLabel(st.start) + ' – ' + shortDayLabel(st.end);
  document.getElementById('rv-week-start-select').value = String(getWeekStartDay());

  document.getElementById('rv-week-kpis').innerHTML = `
    <div class="card kpi-card"><div class="kpi-title">Focus time</div>
      <div class="kpi-value">${fmtMs(st.focusMs)}</div>
      <div class="rv-kpi-sub">avg ${fmtMs(st.focusMs / 7)} per day</div></div>
    <div class="card kpi-card"><div class="kpi-title">Plan kept</div>
      <div class="kpi-value ${pctClass(st.keptPct)}">${st.keptPct === null ? '—' : st.keptPct + '%'}</div>
      <div class="rv-kpi-sub">${fmtMs(st.keptMs)} of ${fmtMs(st.plannedMs)} planned</div></div>
    <div class="card kpi-card"><div class="kpi-title">Shutdowns done</div>
      <div class="kpi-value">${st.shutdowns}/7</div>
      <div class="rv-kpi-sub">${st.movedCount} block${st.movedCount === 1 ? '' : 's'} carried over</div></div>
    <div class="card kpi-card"><div class="kpi-title">Best / weakest day</div>
      <div class="kpi-value rv-kpi-small">${st.best ? escapeHTML(shortDayLabel(st.best.date).split(',')[0]) : '—'} / ${st.worst ? escapeHTML(shortDayLabel(st.worst.date).split(',')[0]) : '—'}</div>
      <div class="rv-kpi-sub">most focus / lowest plan kept</div></div>`;

  const maxMs = Math.max(1, ...st.days.map(d => Math.max(d.plannedMs, d.focusMs)));
  document.getElementById('rv-week-days').innerHTML = st.days.map(d => `
    <tr class="rv-day-row" data-date="${d.date}">
      <td class="rv-nowrap">${escapeHTML(shortDayLabel(d.date))}</td>
      <td>${d.plannedMs ? fmtMs(d.plannedMs) : '—'}</td>
      <td>${d.focusMs ? fmtMs(d.focusMs) : '—'}</td>
      <td class="${pctClass(d.keptPct)}">${d.keptPct === null ? '—' : d.keptPct + '%'}</td>
      <td>${d.blockCount ? d.doneCount + '/' + d.blockCount : '—'}</td>
      <td>${d.review && d.review.shutdown ? '<span class="rv-check">✓</span>' : ''}</td>
      <td class="rv-bar-cell"><div class="rv-bar-track">
        <div class="rv-bar-plan" style="width:${(d.plannedMs / maxMs * 100).toFixed(1)}%"></div>
        <div class="rv-bar-focus" style="width:${(d.focusMs / maxMs * 100).toFixed(1)}%"></div></div></td>
    </tr>`).join('');

  const barList = (rows, emptyTxt) => {
    if (!rows.length) return `<div class="rv-empty">${emptyTxt}</div>`;
    const max = Math.max(...rows.map(r => r.ms));
    return rows.map(r => `<div class="rv-hbar">
      <span class="rv-hbar-name"><span class="rv-dot" style="background:${escapeHTML(r.color)}"></span>${escapeHTML(r.name)}</span>
      <span class="rv-hbar-track"><span class="rv-hbar-fill" style="width:${(r.ms / max * 100).toFixed(1)}%; background:${escapeHTML(r.color)}"></span></span>
      <span class="rv-hbar-val">${fmtMs(r.ms)}</span></div>`).join('');
  };
  document.getElementById('rv-week-tags').innerHTML = barList(st.tagRows, 'No focus sessions this week.');
  document.getElementById('rv-week-skills').innerHTML = barList(st.skillRows, 'No skill practice this week.');

  const rv = st.review || {};
  const winsEl = document.getElementById('rv-week-wins');
  const nextEl = document.getElementById('rv-week-next');
  if (document.activeElement !== winsEl) winsEl.value = rv.wins || '';
  if (document.activeElement !== nextEl) nextEl.value = rv.next || '';
  const status = document.getElementById('review-save-status-week');
  if (status) status.textContent = rv.savedAt ? 'Saved' : '';
}

// ---------- end-of-day prompt ----------
function checkShutdownPrompt() {
  if (!appData || !appData.dayWindow) return;
  const today = getTodayDateString();
  let flag = null;
  try { flag = localStorage.getItem(REVIEW_PROMPT_KEY); } catch (e) { /* ignore */ }
  if (flag === today) return;
  const rv = (appData.reviews || {})['day:' + today];
  if (rv && rv.shutdown) return;
  const now = new Date();
  const nowMin = now.getHours() * 60 + now.getMinutes();
  if (nowMin < (appData.dayWindow.endMin || 1320)) return;
  showShutdownBar(today);
}

function showShutdownBar(today) {
  let bar = document.getElementById('review-bar');
  if (!bar) {
    bar = document.createElement('div');
    bar.id = 'review-bar';
    bar.setAttribute('role', 'status');
    bar.innerHTML = '<span>Your day is over. Time for the shutdown review.</span>' +
      '<button type="button" id="btn-review-bar-open">Review</button>' +
      '<button type="button" id="btn-review-bar-later" class="rv-later">Later</button>';
    document.body.appendChild(bar);
  }
  bar.style.display = 'flex';
  const dismiss = () => {
    try { localStorage.setItem(REVIEW_PROMPT_KEY, today); } catch (e) { /* ignore */ }
    bar.style.display = 'none';
  };
  document.getElementById('btn-review-bar-open').onclick = () => {
    dismiss();
    reviewTab = 'day';
    reviewDayDate = today;
    switchView('review');
  };
  document.getElementById('btn-review-bar-later').onclick = dismiss;
}

// ---------- wiring ----------
function initReviewView() {
  document.querySelectorAll('.rv-tab').forEach(b => b.addEventListener('click', () => {
    reviewTab = b.dataset.tab;
    renderReviewView();
  }));

  document.getElementById('btn-rv-day-prev').addEventListener('click', () => { reviewDayDate = addDaysStr(reviewDayDate, -1); renderDayReview(); });
  document.getElementById('btn-rv-day-next').addEventListener('click', () => { reviewDayDate = addDaysStr(reviewDayDate, 1); renderDayReview(); });
  document.getElementById('btn-rv-day-today').addEventListener('click', () => { reviewDayDate = getTodayDateString(); renderDayReview(); });
  document.getElementById('btn-rv-week-prev').addEventListener('click', () => { reviewWeekStart = addDaysStr(reviewWeekStart, -7); renderWeekReview(); });
  document.getElementById('btn-rv-week-next').addEventListener('click', () => { reviewWeekStart = addDaysStr(reviewWeekStart, 7); renderWeekReview(); });
  document.getElementById('btn-rv-week-this').addEventListener('click', () => { reviewWeekStart = weekStartOf(getTodayDateString()); renderWeekReview(); });

  document.getElementById('rv-week-start-select').addEventListener('change', e => {
    appData.settings.weekStart = parseInt(e.target.value, 10);
    saveAppData();
    reviewWeekStart = weekStartOf(reviewWeekStart);
    renderWeekReview();
  });

  // Clicking a day in the week table opens that day's review
  document.getElementById('rv-week-days').addEventListener('click', e => {
    const row = e.target.closest('.rv-day-row');
    if (!row) return;
    reviewDayDate = row.dataset.date;
    reviewTab = 'day';
    renderReviewView();
  });

  document.getElementById('btn-rv-carry').addEventListener('click', () => {
    const ids = [...document.querySelectorAll('.rv-carry-cb:checked')].map(cb => cb.value);
    if (!ids.length) { showToast('Select at least one block', 'var(--amber)'); return; }
    carryOverBlocks(reviewDayDate, ids);
    renderDayReview();
  });

  const dayBase = () => ({ kind: 'day', date: reviewDayDate });
  document.getElementById('rv-day-note').addEventListener('input', e => saveReviewField('day:' + reviewDayDate, dayBase(), 'note', e.target.value));
  document.getElementById('rv-day-shutdown').addEventListener('change', e => {
    saveReviewField('day:' + reviewDayDate, dayBase(), 'shutdown', e.target.checked, true);
    if (e.target.checked) {
      showToast('Shutdown complete. Day closed.', 'var(--teal)');
      const bar = document.getElementById('review-bar');
      if (bar && reviewDayDate === getTodayDateString()) bar.style.display = 'none';
    }
    setTimeout(renderDayReview, 10);
  });

  const weekBase = () => ({ kind: 'week', weekStart: reviewWeekStart });
  document.getElementById('rv-week-wins').addEventListener('input', e => saveReviewField('week:' + reviewWeekStart, weekBase(), 'wins', e.target.value));
  document.getElementById('rv-week-next').addEventListener('input', e => saveReviewField('week:' + reviewWeekStart, weekBase(), 'next', e.target.value));

  checkShutdownPrompt();
  setInterval(checkShutdownPrompt, 60000);
}
"""
