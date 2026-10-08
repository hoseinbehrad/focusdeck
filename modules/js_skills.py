# JavaScript 10,000 Hours Mastery Module
JS_SKILLS = """
// ==========================================
// 5. 10,000 HOURS MASTERY ENGINE
// ==========================================

const ALL_MILESTONES = [
  { hours: 10, name: 'First Steps', badge: '10h' },
  { hours: 50, name: 'Committed', badge: '50h' },
  { hours: 100, name: 'Foundation', badge: '100h' },
  { hours: 250, name: 'Apprentice', badge: '250h' },
  { hours: 500, name: 'Practitioner', badge: '500h' },
  { hours: 1000, name: 'Journeyman (1k)', badge: '1,000h' },
  { hours: 2000, name: 'Skilled (2k)', badge: '2,000h' },
  { hours: 3000, name: 'Proficient (3k)', badge: '3,000h' },
  { hours: 4000, name: 'Adept (4k)', badge: '4,000h' },
  { hours: 5000, name: 'Halfway Master (5k)', badge: '5,000h' },
  { hours: 6000, name: 'Senior (6k)', badge: '6,000h' },
  { hours: 7000, name: 'Specialist (7k)', badge: '7,000h' },
  { hours: 8000, name: 'Authority (8k)', badge: '8,000h' },
  { hours: 9000, name: 'Virtuoso (9k)', badge: '9,000h' },
  { hours: 10000, name: 'Grandmaster (10k)', badge: '10,000h' }
];

function initSkillsView() {
  const addBtn = document.getElementById('btn-open-add-skill');
  if (addBtn) addBtn.addEventListener('click', () => openAddSkillModal());
  const emptyBtn = document.getElementById('btn-empty-add-skill');
  if (emptyBtn) emptyBtn.addEventListener('click', () => openAddSkillModal());
  const closeSkill = document.getElementById('btn-close-skill-modal');
  if (closeSkill) closeSkill.addEventListener('click', () => closeModal('modal-add-skill'));
  const cancelSkill = document.getElementById('btn-cancel-skill-modal');
  if (cancelSkill) cancelSkill.addEventListener('click', () => closeModal('modal-add-skill'));
  const formSkill = document.getElementById('form-add-skill');
  if (formSkill) formSkill.addEventListener('submit', handleSaveSkillForm);

  const closeDetail = document.getElementById('btn-close-skill-detail');
  if (closeDetail) closeDetail.addEventListener('click', () => closeModal('modal-skill-detail'));
  const closeBacklog = document.getElementById('btn-close-backlog-modal');
  if (closeBacklog) closeBacklog.addEventListener('click', () => closeModal('modal-add-backlog'));
  const cancelBacklog = document.getElementById('btn-cancel-backlog');
  if (cancelBacklog) cancelBacklog.addEventListener('click', () => closeModal('modal-add-backlog'));
  const formBacklog = document.getElementById('form-add-backlog');
  if (formBacklog) formBacklog.addEventListener('submit', handleSaveBacklogForm);
}

function deleteSkill(skillId) {
  const skill = (appData.skills || []).find(x => x.id === skillId);
  if (!skill) return;
  showConfirmModal({
    title: 'Delete Skill',
    message: `Are you sure you want to delete "${skill.name}"? Historical sessions and backlogs will remain.`,
    confirmText: 'Delete Skill',
    isDanger: true,
    onConfirm: () => {
      appData.skills = (appData.skills || []).filter(x => x.id !== skillId);
      saveAppData();
      renderSkillsView();
      showToast(`Deleted skill "${skill.name}"`, 'var(--coral)');
    }
  });
}
window.deleteSkill = deleteSkill;
window.deleteSkillById = function(id) { deleteSkill(id); };
window.openAddSkillModalById = function(id) {
  const skill = (appData.skills || []).find(x => x.id === id);
  if (skill) openAddSkillModal(skill);
};
window.openAddBacklogModalById = function(id) { openAddBacklogModal(id); };
window.openSkillDetailModalById = function(id) { openSkillDetailModal(id); };

// Calculate Total Hours for a skill (focus sessions + manual backlog)
function getSkillTotalHours(skill) {
  let sessionMs = 0;
  const countedSessionIds = new Set();

  (appData.sessions || []).forEach(sess => {
    if (sess.mode !== 'focus') return;
    if (countedSessionIds.has(sess.id)) return;

    const matchesLabel = (skill.linkedLabels || []).includes(sess.label);
    const matchesTag = (skill.linkedTags || []).some(t => (sess.tags || []).includes(t));

    if (matchesLabel || matchesTag) {
      countedSessionIds.add(sess.id);
      sessionMs += (sess.actualMs || 0);
    }
  });

  let backlogHours = 0;
  (appData.manualBacklogEntries || []).forEach(entry => {
    if (entry.skillId === skill.id) {
      backlogHours += (parseFloat(entry.hours) || 0);
    }
  });

  return (sessionMs / 3600000) + backlogHours;
}

// 30-day stats: hours in last 30 days, pace per week, daily hours array
function getSkill30DayStats(skill) {
  const now = Date.now();
  const thirtyDaysAgo = now - (30 * 86400000);
  const dailyHours = new Array(30).fill(0);
  const countedSessionIds = new Set();
  let total30dMs = 0;
  let practicedToday = false;
  const todayStr = getTodayDateString();

  (appData.sessions || []).forEach(sess => {
    if (sess.mode !== 'focus') return;
    if (sess.startedAt < thirtyDaysAgo) return;
    if (countedSessionIds.has(sess.id)) return;

    const matchesLabel = (skill.linkedLabels || []).includes(sess.label);
    const matchesTag = (skill.linkedTags || []).some(t => (sess.tags || []).includes(t));

    if (matchesLabel || matchesTag) {
      countedSessionIds.add(sess.id);
      total30dMs += (sess.actualMs || 0);

      const dayIdx = Math.min(29, Math.max(0, Math.floor((sess.startedAt - thirtyDaysAgo) / 86400000)));
      dailyHours[dayIdx] += (sess.actualMs / 3600000);

      if (formatDateString(sess.startedAt) === todayStr) {
        practicedToday = true;
      }
    }
  });

  const total30dHours = total30dMs / 3600000;
  const hoursPerWeek = (total30dHours / 30) * 7;

  return {
    total30dHours,
    hoursPerWeek,
    dailyHours,
    practicedToday
  };
}

// Projected completion date
function getProjectedCompletionString(remainingHours, hoursLast30Days) {
  if (remainingHours <= 0) return 'Goal Completed!';
  if (!hoursLast30Days || hoursLast30Days <= 0.1) return 'No recent activity';

  const dailyAvg = hoursLast30Days / 30;
  const daysRemaining = Math.ceil(remainingHours / dailyAvg);
  const finishDate = new Date(Date.now() + (daysRemaining * 86400000));

  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  return `${months[finishDate.getMonth()]} ${finishDate.getFullYear()} (~${Math.round(daysRemaining / 30.4)} mos)`;
}

// Milestone calculations
function getMilestoneProgress(totalHours, goalHours) {
  const earned = [];
  let nextMilestone = null;

  ALL_MILESTONES.forEach(m => {
    if (m.hours <= goalHours) {
      if (totalHours >= m.hours) {
        earned.push(m);
      } else if (!nextMilestone) {
        nextMilestone = m;
      }
    }
  });

  if (!nextMilestone && totalHours < goalHours) {
    nextMilestone = { hours: goalHours, name: 'Mastery Goal', badge: `${goalHours}h` };
  }

  let prevHours = 0;
  if (earned.length > 0) {
    prevHours = earned[earned.length - 1].hours;
  }

  let progressPct = 100;
  let hoursNeeded = 0;
  if (nextMilestone) {
    hoursNeeded = Math.max(0, nextMilestone.hours - totalHours);
    const span = nextMilestone.hours - prevHours;
    const completedInSpan = totalHours - prevHours;
    progressPct = span > 0 ? Math.min(100, Math.max(0, (completedInSpan / span) * 100)) : 100;
  }

  return { earned, nextMilestone, progressPct, hoursNeeded };
}

function renderSkillsView() {
  const grid = document.getElementById('skills-grid');
  const emptyState = document.getElementById('skills-empty-state');

  if (!appData.skills || appData.skills.length === 0) {
    grid.style.display = 'none';
    emptyState.style.display = 'block';
    return;
  }

  grid.style.display = 'grid';
  emptyState.style.display = 'none';

  let html = '';
  appData.skills.forEach(skill => {
    const totalHours = getSkillTotalHours(skill);
    const goalHours = skill.goalHours || 10000;
    const pct = Math.min(100, Math.max(0, (totalHours / goalHours) * 100));
    const stats30d = getSkill30DayStats(skill);
    const remainingHours = Math.max(0, goalHours - totalHours);
    const etaStr = getProjectedCompletionString(remainingHours, stats30d.total30dHours);
    const milestoneInfo = getMilestoneProgress(totalHours, goalHours);

    // Sparkline SVG
    const sparklineSvg = createSkillSparklineSvg(stats30d.dailyHours, skill.color);

    // Jar SVG
    const jarSvg = createJarSvg(skill, pct, stats30d.practicedToday);

    html += `
      <div class="card skill-card" id="skill-card-${skill.id}">
        <div class="skill-card-header">
          <div>
            <div class="skill-card-title">${escapeHTML(skill.name)}</div>
            <div class="skill-card-goal">${goalHours.toLocaleString()} Hours Mastery Goal</div>
          </div>
          <div style="display:flex; gap:6px;">
            <button class="icon-btn-sm btn-edit-skill" onclick="openAddSkillModalById('${skill.id}')" data-id="${skill.id}" title="Edit Skill" style="color:var(--muted);">
              <svg viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
            </button>
            <button class="icon-btn-sm btn-del-skill" onclick="deleteSkillById('${skill.id}')" data-id="${skill.id}" title="Delete Skill" style="color:var(--coral);">
              <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
            </button>
          </div>
        </div>

        <div class="skill-jar-container" id="jar-wrap-${skill.id}" onclick="triggerJarCelebration('${skill.id}')" data-id="${skill.id}" title="Click jar to celebrate progress!">
          ${jarSvg}
        </div>

        <div class="skill-stats-row">
          <div class="skill-stat-block">
            <span class="skill-stat-label">Total Practice</span>
            <span class="skill-stat-val" style="color:#fff;">${totalHours.toLocaleString(undefined, {minimumFractionDigits: 1, maximumFractionDigits: 1})} hrs</span>
          </div>
          <div class="skill-stat-block" style="text-align:right;">
            <span class="skill-stat-label">Progress</span>
            <span class="skill-stat-val" style="color:${skill.color};">${pct.toFixed(1)}%</span>
          </div>
        </div>

        <!-- Next Milestone Card -->
        <div class="milestone-box">
          <div style="display:flex; justify-content:space-between; align-items:center; font-size:11px; margin-bottom:4px;">
            <span style="color:var(--muted);">Next: <strong style="color:#fff;">${milestoneInfo.nextMilestone ? milestoneInfo.nextMilestone.name : 'Mastery Achieved!'}</strong></span>
            <span style="color:var(--teal);">${milestoneInfo.nextMilestone ? `${milestoneInfo.hoursNeeded.toFixed(1)} hrs to unlock` : 'Done'}</span>
          </div>
          <div class="prog-bar-bg" style="height:5px;">
            <div class="prog-bar-fill" style="width:${milestoneInfo.progressPct}%; background:${skill.color};"></div>
          </div>
        </div>

        <!-- Pace & ETA -->
        <div class="skill-pace-row">
          <span>${stats30d.hoursPerWeek.toFixed(1)} hrs/wk (30d)</span>
          <span>ETA: <strong>${etaStr}</strong></span>
        </div>

        <!-- 30-day sparkline -->
        <div style="margin-top:10px; height:32px;">
          ${sparklineSvg}
        </div>

        <!-- Bottom Actions -->
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:14px; border-top:1px solid var(--border); padding-top:12px;">
          <button class="btn btn-secondary btn-sm btn-open-backlog" onclick="openAddBacklogModalById('${skill.id}')" data-id="${skill.id}" style="font-size:11px; padding:4px 8px;">
            <svg viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            <span>Log Backlog Hours</span>
          </button>
          <button class="btn btn-secondary btn-sm btn-open-detail" onclick="openSkillDetailModalById('${skill.id}')" data-id="${skill.id}" style="font-size:11px; padding:4px 8px;">
            <span>Details & History &rarr;</span>
          </button>
        </div>
      </div>
    `;
  });

  grid.innerHTML = html;

  attachSkillCardListeners(grid);
}

// Hand-drawn Inline SVG Jar with Wave Liquid, Markers, and Bubbles
function createJarSvg(skill, pct, practicedToday) {
  const jarWidth = 140;
  const jarHeight = 200;
  const clipId = `jar-clip-${skill.id}`;
  const gradId = `jar-grad-${skill.id}`;

  const innerTop = 32;
  const innerBottom = 188;
  const innerHeight = innerBottom - innerTop; // 156px

  const fillHeight = (pct / 100) * innerHeight;
  const liquidY = innerBottom - fillHeight;

  // Bubbles
  let bubblesHtml = '';
  if (practicedToday) {
    bubblesHtml = `
      <circle class="jar-bubble bubble-1" cx="55" cy="180" r="3" fill="${skill.color}" fill-opacity="0.7"/>
      <circle class="jar-bubble bubble-2" cx="70" cy="170" r="4.5" fill="${skill.color}" fill-opacity="0.6"/>
      <circle class="jar-bubble bubble-3" cx="85" cy="185" r="3.5" fill="${skill.color}" fill-opacity="0.7"/>
    `;
  }

  return `
    <svg class="jar-svg" viewBox="0 0 ${jarWidth} ${jarHeight}">
      <defs>
        <linearGradient id="${gradId}" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="${skill.color}" stop-opacity="0.9" />
          <stop offset="100%" stop-color="${skill.color}" stop-opacity="0.4" />
        </linearGradient>
        <clipPath id="${clipId}">
          <!-- Glass inner cavity contour -->
          <path d="M 32 30 L 32 170 Q 32 188 50 188 L 90 188 Q 108 188 108 170 L 108 30 Z" />
        </clipPath>
      </defs>

      <!-- Glass back highlight -->
      <path d="M 30 28 L 30 172 Q 30 190 50 190 L 90 190 Q 110 190 110 172 L 110 28 Z" fill="rgba(255,255,255,0.03)" />

      <!-- Clipped Liquid Fill -->
      <g clip-path="url(#${clipId})">
        <!-- Liquid Volume -->
        <rect x="25" y="${liquidY}" width="90" height="${fillHeight + 20}" fill="url(#${gradId})" />

        <!-- Liquid Wave Surface -->
        <path class="jar-liquid-wave" fill="${skill.color}" d="M 20 ${liquidY} Q 45 ${liquidY - 5} 70 ${liquidY} T 120 ${liquidY} L 120 ${liquidY + 10} L 20 ${liquidY + 10} Z" />

        <!-- Internal Bubbles -->
        ${bubblesHtml}

        <!-- 25%, 50%, 75% Milestone Marker Ticks inside Jar -->
        <line x1="32" y1="${innerBottom - 0.25 * innerHeight}" x2="48" y2="${innerBottom - 0.25 * innerHeight}" stroke="rgba(255,255,255,0.3)" stroke-width="1.5" stroke-dasharray="2 2" />
        <text x="52" y="${innerBottom - 0.25 * innerHeight + 3}" fill="rgba(255,255,255,0.4)" font-size="8" font-family="sans-serif">25%</text>

        <line x1="32" y1="${innerBottom - 0.50 * innerHeight}" x2="48" y2="${innerBottom - 0.50 * innerHeight}" stroke="rgba(255,255,255,0.3)" stroke-width="1.5" stroke-dasharray="2 2" />
        <text x="52" y="${innerBottom - 0.50 * innerHeight + 3}" fill="rgba(255,255,255,0.4)" font-size="8" font-family="sans-serif">50%</text>

        <line x1="32" y1="${innerBottom - 0.75 * innerHeight}" x2="48" y2="${innerBottom - 0.75 * innerHeight}" stroke="rgba(255,255,255,0.3)" stroke-width="1.5" stroke-dasharray="2 2" />
        <text x="52" y="${innerBottom - 0.75 * innerHeight + 3}" fill="rgba(255,255,255,0.4)" font-size="8" font-family="sans-serif">75%</text>
      </g>

      <!-- Glass Outline & Cork / Rim -->
      <!-- Rim Neck -->
      <path d="M 38 18 L 102 18 L 102 26 L 38 26 Z" fill="rgba(255,255,255,0.06)" stroke="rgba(255,255,255,0.35)" stroke-width="1.8" />
      <ellipse cx="70" cy="18" rx="32" ry="5" fill="rgba(255,255,255,0.12)" stroke="rgba(255,255,255,0.4)" stroke-width="1.5" />

      <!-- Glass Body Wall -->
      <path d="M 30 26 L 30 172 Q 30 190 50 190 L 90 190 Q 110 190 110 172 L 110 26" fill="none" stroke="rgba(255,255,255,0.35)" stroke-width="2" />

      <!-- Glass Left Reflection Highlight Streak -->
      <path d="M 36 34 L 36 168 Q 36 178 44 182" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="2.5" stroke-linecap="round" />
    </svg>
  `;
}

// 30-day sparkline SVG
function createSkillSparklineSvg(dailyArr, color) {
  const w = 240;
  const h = 32;
  const max = Math.max(1, ...dailyArr);
  const n = dailyArr.length;
  const dx = w / (n - 1);

  let pts = [];
  dailyArr.forEach((val, i) => {
    const x = i * dx;
    const y = h - (val / max) * (h - 6) - 3;
    pts.push(`${x.toFixed(1)},${y.toFixed(1)}`);
  });

  return `
    <svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" style="width:100%; height:100%;">
      <polyline points="${pts.join(' ')}" fill="none" stroke="${color || '#4F5BF0'}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
    </svg>
  `;
}

function attachSkillCardListeners(grid) {
  // Actions are wired directly with onclick attributes on card elements for 100% reliable execution
}

function triggerJarCelebration(skillId) {
  const wrap = document.getElementById(`jar-wrap-${skillId}`);
  if (wrap) {
    wrap.classList.remove('jar-celebrate');
    void wrap.offsetWidth; // retrigger reflow
    wrap.classList.add('jar-celebrate');
    setTimeout(() => wrap.classList.remove('jar-celebrate'), 1500);
  }
}

// Add / Edit Skill Modal
let skillModalSelectedTags = [];
let skillModalSelectedLabels = [];

function openAddSkillModal(skillToEdit) {
  const form = document.getElementById('form-add-skill');
  form.reset();

  const isEdit = !!skillToEdit;
  document.getElementById('modal-skill-title').textContent = isEdit ? 'Edit Mastery Skill' : 'Add Mastery Skill';
  document.getElementById('skill-input-id').value = isEdit ? skillToEdit.id : '';
  document.getElementById('skill-input-name').value = isEdit ? skillToEdit.name : '';
  document.getElementById('skill-input-goal').value = isEdit ? skillToEdit.goalHours : 10000;
  document.getElementById('skill-input-color').value = isEdit ? skillToEdit.color : PALETTE[Math.floor(Math.random() * PALETTE.length)];

  skillModalSelectedTags = isEdit ? [ ...(skillToEdit.linkedTags || []) ] : [];
  skillModalSelectedLabels = isEdit ? [ ...(skillToEdit.linkedLabels || []) ] : [];

  renderSkillModalTaxonomies();
  openModal('modal-add-skill');
}

function renderSkillModalTaxonomies() {
  // Tags
  const tagContainer = document.getElementById('skill-link-tags-container');
  let tagHtml = '';
  appData.tags.forEach(tag => {
    const isSel = skillModalSelectedTags.includes(tag.id);
    tagHtml += `
      <div class="chip ${isSel ? 'selected' : ''}" data-id="${tag.id}">
        <span class="chip-dot" style="background:${tag.color}"></span>
        <span>${escapeHTML(tag.name)}</span>
      </div>
    `;
  });
  tagContainer.innerHTML = tagHtml;

  tagContainer.querySelectorAll('.chip').forEach(c => {
    c.addEventListener('click', () => {
      const id = c.getAttribute('data-id');
      const idx = skillModalSelectedTags.indexOf(id);
      if (idx >= 0) skillModalSelectedTags.splice(idx, 1);
      else skillModalSelectedTags.push(id);
      renderSkillModalTaxonomies();
    });
  });

  // Distinct Labels from history
  const labelContainer = document.getElementById('skill-link-labels-container');
  const distinctLabels = new Set();
  (appData.sessions || []).forEach(s => {
    if (s.label && s.label.trim()) distinctLabels.add(s.label.trim());
  });
  (appData.timeblockPlans ? Object.values(appData.timeblockPlans) : []).forEach(p => {
    (p.blocks || []).forEach(b => {
      if (b.label && b.label.trim()) distinctLabels.add(b.label.trim());
    });
  });

  if (distinctLabels.size === 0) {
    labelContainer.innerHTML = '<span style="font-size:12px; color:var(--muted);">No past labels recorded yet.</span>';
    return;
  }

  let labelHtml = '<div style="display:flex; flex-wrap:wrap; gap:6px;">';
  Array.from(distinctLabels).sort().forEach(lbl => {
    const isSel = skillModalSelectedLabels.includes(lbl);
    labelHtml += `
      <span class="chip ${isSel ? 'selected' : ''}" data-label="${escapeHTML(lbl)}" style="font-size:11px;">
        <span>${escapeHTML(lbl)}</span>
      </span>
    `;
  });
  labelHtml += '</div>';
  labelContainer.innerHTML = labelHtml;

  labelContainer.querySelectorAll('.chip').forEach(c => {
    c.addEventListener('click', () => {
      const lbl = c.getAttribute('data-label');
      const idx = skillModalSelectedLabels.indexOf(lbl);
      if (idx >= 0) skillModalSelectedLabels.splice(idx, 1);
      else skillModalSelectedLabels.push(lbl);
      renderSkillModalTaxonomies();
    });
  });
}

function handleSaveSkillForm(e) {
  e.preventDefault();
  const id = document.getElementById('skill-input-id').value;
  const name = document.getElementById('skill-input-name').value.trim();
  const goal = parseInt(document.getElementById('skill-input-goal').value, 10) || 10000;
  const color = document.getElementById('skill-input-color').value || '#4F5BF0';

  if (!id) {
    const newSkill = {
      id: uid('skill'),
      name,
      goalHours: goal,
      color,
      linkedTags: [ ...skillModalSelectedTags ],
      linkedLabels: [ ...skillModalSelectedLabels ],
      createdAt: Date.now()
    };
    appData.skills.push(newSkill);
    showToast(`Created skill "${name}"`, color);
  } else {
    const s = appData.skills.find(x => x.id === id);
    if (s) {
      s.name = name;
      s.goalHours = goal;
      s.color = color;
      s.linkedTags = [ ...skillModalSelectedTags ];
      s.linkedLabels = [ ...skillModalSelectedLabels ];
      showToast(`Updated "${name}"`, color);
    }
  }

  saveAppData();
  closeModal('modal-add-skill');
  renderSkillsView();
}

// Backlog Hours Modal
function openAddBacklogModal(skillId) {
  const form = document.getElementById('form-add-backlog');
  form.reset();
  document.getElementById('backlog-skill-id').value = skillId;
  openModal('modal-add-backlog');
  document.getElementById('backlog-hours-input').focus();
}

function handleSaveBacklogForm(e) {
  e.preventDefault();
  const skillId = document.getElementById('backlog-skill-id').value;
  const hours = parseFloat(document.getElementById('backlog-hours-input').value) || 0;
  const note = document.getElementById('backlog-note-input').value.trim();

  if (hours <= 0) return;

  const entry = {
    id: uid('bk'),
    skillId,
    hours,
    note: note || 'Historical deliberate practice',
    addedAt: Date.now()
  };

  appData.manualBacklogEntries.push(entry);
  saveAppData();
  closeModal('modal-add-backlog');
  renderSkillsView();

  const skill = appData.skills.find(x => x.id === skillId);
  showToast(`Added ${hours} backlog hours to ${skill ? skill.name : 'skill'}`, 'var(--teal)');
}

// Skill Detail Modal
function openSkillDetailModal(skillId) {
  const skill = appData.skills.find(x => x.id === skillId);
  if (!skill) return;

  document.getElementById('detail-skill-title').textContent = `${skill.name} — Mastery Detail`;
  document.getElementById('detail-skill-color').style.background = skill.color;

  const totalHours = getSkillTotalHours(skill);
  const goalHours = skill.goalHours || 10000;
  const pct = Math.min(100, Math.max(0, (totalHours / goalHours) * 100));
  const stats30d = getSkill30DayStats(skill);
  const milestoneInfo = getMilestoneProgress(totalHours, goalHours);

  // Filter sessions matching this skill
  const matchingSessions = (appData.sessions || []).filter(s => {
    if (s.mode !== 'focus') return false;
    const matchesLabel = (skill.linkedLabels || []).includes(s.label);
    const matchesTag = (skill.linkedTags || []).some(t => (s.tags || []).includes(t));
    return matchesLabel || matchesTag;
  });

  const matchingBacklogs = (appData.manualBacklogEntries || []).filter(b => b.skillId === skill.id);

  const content = document.getElementById('detail-skill-content');
  content.innerHTML = `
    <div style="display:grid; grid-template-columns:140px 1fr; gap:24px; align-items:center; margin-bottom:20px;">
      <div style="width:140px;">
        ${createJarSvg(skill, pct, stats30d.practicedToday)}
      </div>
      <div>
        <div style="font-size:26px; font-weight:800; color:#fff;">${totalHours.toFixed(1)} / ${goalHours.toLocaleString()} hrs</div>
        <div style="font-size:14px; color:${skill.color}; font-weight:700; margin-bottom:12px;">${pct.toFixed(2)}% of mastery path completed</div>

        <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
          ${milestoneInfo.earned.map(m => `<span class="pill-badge pill-teal">${m.badge} (${m.name})</span>`).join('')}
        </div>

        <div style="font-size:12px; color:var(--muted); line-height:1.6;">
          Linked Labels: <strong>${(skill.linkedLabels || []).join(', ') || 'None'}</strong><br/>
          Linked Tags: <strong>${(skill.linkedTags || []).map(tid => { const tg = appData.tags.find(x => x.id === tid); return tg ? tg.name : tid; }).join(', ') || 'None'}</strong>
        </div>
      </div>
    </div>

    <!-- Historical Backlog Entries -->
    <div style="margin-bottom:20px;">
      <div style="font-weight:700; color:#fff; font-size:14px; margin-bottom:8px;">Manual Backlog Records (${matchingBacklogs.length})</div>
      ${matchingBacklogs.length === 0 ? '<div style="font-size:12px; color:var(--muted);">No backlog credits added yet.</div>' : `
        <div style="display:flex; flex-direction:column; gap:6px;">
          ${matchingBacklogs.map(bk => `
            <div style="background:var(--surface-2); padding:8px 12px; border-radius:6px; font-size:12px; display:flex; justify-content:space-between; align-items:center;">
              <div><strong>+${bk.hours} hrs</strong> — <span style="color:var(--muted);">${escapeHTML(bk.note || 'Backlog')}</span></div>
              <span style="font-size:11px; color:var(--muted);">${formatDateString(bk.addedAt)}</span>
            </div>
          `).join('')}
        </div>
      `}
    </div>

    <!-- Recent Matching Sessions -->
    <div>
      <div style="font-weight:700; color:#fff; font-size:14px; margin-bottom:8px;">Recent Focus Sessions (${matchingSessions.length} total)</div>
      <div style="max-height:220px; overflow-y:auto; border:1px solid var(--border); border-radius:8px;">
        <table class="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Task Label</th>
              <th>Duration</th>
            </tr>
          </thead>
          <tbody>
            ${matchingSessions.slice(0, 15).map(s => `
              <tr>
                <td>${formatDateString(s.startedAt)}</td>
                <td>${escapeHTML(s.label)}</td>
                <td>${Math.round(s.actualMs / 60000)} mins</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;

  openModal('modal-skill-detail');
}
"""
