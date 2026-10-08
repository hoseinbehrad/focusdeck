# JavaScript Time Block Planner Module
JS_TIMEBLOCK = """
// ==========================================
// 4. TIME BLOCK PLANNER ENGINE
// ==========================================

let selectedTbDate = getTodayDateString();
let tbNowLineInterval = null;
let tbDragState = null; // for dragging/resizing blocks on timeline
const TB_PIXELS_PER_MIN = 1.3; // 60 mins = 78px

function initTimeBlockView() {
  // Date navigator
  const datePicker = document.getElementById('tb-date-picker');
  datePicker.value = selectedTbDate;

  document.getElementById('tb-btn-prev-day').addEventListener('click', () => {
    shiftTbDate(-1);
  });
  document.getElementById('tb-btn-next-day').addEventListener('click', () => {
    shiftTbDate(1);
  });
  document.getElementById('tb-btn-today').addEventListener('click', () => {
    selectedTbDate = getTodayDateString();
    datePicker.value = selectedTbDate;
    renderTimeBlockView();
  });
  datePicker.addEventListener('change', (e) => {
    if (e.target.value) {
      selectedTbDate = e.target.value;
      renderTimeBlockView();
    }
  });

  // Day window time inputs
  const winStartInput = document.getElementById('tb-window-start');
  const winEndInput = document.getElementById('tb-window-end');

  winStartInput.value = minToTimeOfDay(appData.dayWindow.startMin);
  winEndInput.value = minToTimeOfDay(appData.dayWindow.endMin);

  winStartInput.addEventListener('change', () => {
    const sMin = timeOfDayToMin(winStartInput.value);
    if (sMin < appData.dayWindow.endMin - 60) {
      appData.dayWindow.startMin = sMin;
      saveAppData();
      renderTimeBlockView();
    } else {
      winStartInput.value = minToTimeOfDay(appData.dayWindow.startMin);
    }
  });

  winEndInput.addEventListener('change', () => {
    const eMin = timeOfDayToMin(winEndInput.value);
    if (eMin > appData.dayWindow.startMin + 60) {
      appData.dayWindow.endMin = eMin;
      saveAppData();
      renderTimeBlockView();
    } else {
      winEndInput.value = minToTimeOfDay(appData.dayWindow.endMin);
    }
  });

  // Toolbar Actions
  document.getElementById('btn-tb-copy-yesterday').addEventListener('click', copyYesterdayPlan);
  document.getElementById('btn-tb-save-template').addEventListener('click', openSaveTemplateModal);
  document.getElementById('btn-tb-load-template').addEventListener('click', openLoadTemplateModal);
  document.getElementById('btn-tb-reschedule').addEventListener('click', rescheduleRemainingDay);

  // Quick Rest Buttons (5, 15, 30 min)
  document.querySelectorAll('.btn-tb-rest').forEach(btn => {
    btn.addEventListener('click', () => {
      const min = parseInt(btn.getAttribute('data-min'), 10) || 15;
      addQuickRestBlock(min);
    });
  });

  // Add Block Modal
  document.getElementById('btn-tb-open-add').addEventListener('click', () => {
    openAddBlockModal();
  });
  document.getElementById('btn-close-tb-modal').addEventListener('click', () => closeModal('modal-add-timeblock'));
  document.getElementById('btn-cancel-tb-modal').addEventListener('click', () => closeModal('modal-add-timeblock'));
  document.getElementById('btn-close-template-modal').addEventListener('click', () => closeModal('modal-tb-templates'));

  document.getElementById('form-add-timeblock').addEventListener('submit', handleSaveBlockForm);

  // Timeline Drag & Resize Listeners
  initTimelineMouseEvents();

  // Sticky Note Listeners
  initStickyNoteListeners();

  // Periodic Now-line update
  if (tbNowLineInterval) clearInterval(tbNowLineInterval);
  tbNowLineInterval = setInterval(updateNowLinePosition, 60000);
}

function shiftTbDate(deltaDays) {
  const cur = new Date(selectedTbDate + 'T00:00:00');
  cur.setDate(cur.getDate() + deltaDays);
  selectedTbDate = formatDateString(cur.getTime());
  renderTimeBlockView();
}

function getSelectedPlan() {
  if (!appData.timeblockPlans[selectedTbDate]) {
    appData.timeblockPlans[selectedTbDate] = { blocks: [], notes: '' };
  }
  if (!Array.isArray(appData.timeblockPlans[selectedTbDate].blocks)) {
    appData.timeblockPlans[selectedTbDate].blocks = [];
  }
  if (appData.timeblockPlans[selectedTbDate].notes === undefined) {
    appData.timeblockPlans[selectedTbDate].notes = '';
  }
  return appData.timeblockPlans[selectedTbDate];
}

// Compute stacked positions for all blocks in the day
function computeStackedBlocks(blocks) {
  const dayStart = appData.dayWindow.startMin;
  let cursor = dayStart;

  return blocks.map(b => {
    const isManual = (b.manualStartMin !== undefined && b.manualStartMin !== null);
    const startMin = isManual ? Math.max(dayStart, b.manualStartMin) : cursor;
    const dur = Math.max(5, b.durationMin || 30);
    const endMin = startMin + dur;

    cursor = endMin;

    return {
      ...b,
      startMin,
      endMin,
      durationMin: dur
    };
  });
}

function renderTimeBlockView() {
  const datePicker = document.getElementById('tb-date-picker');
  if (datePicker && datePicker.value !== selectedTbDate) {
    datePicker.value = selectedTbDate;
  }

  // Update Weekday Badge beside Date Picker (e.g., Mon, Tue, Wed...)
  const weekdayEl = document.getElementById('tb-date-weekday');
  if (weekdayEl && selectedTbDate) {
    const parts = selectedTbDate.split('-');
    if (parts.length === 3) {
      const d = new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, parseInt(parts[2], 10));
      const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
      weekdayEl.textContent = days[d.getDay()] || '';
    }
  }

  const plan = getSelectedPlan();
  const stackedBlocks = computeStackedBlocks(plan.blocks);

  // 1. Render Left Builder List
  renderBlockBuilderList(stackedBlocks);

  // 2. Render Main Timeline Canvas
  renderTimelineCanvas(stackedBlocks);

  // 3. Update Reschedule Overrun Button Visibility
  checkOverrunReschedule(stackedBlocks);

  // 4. Render Sticky Note for Current Day
  renderStickyNote();
}

function renderBlockBuilderList(blocks) {
  const container = document.getElementById('tb-blocks-list');
  const statsEl = document.getElementById('tb-builder-stats');

  let totalPlannedMin = 0;
  blocks.forEach(b => totalPlannedMin += (b.durationMin || 0));
  statsEl.textContent = `${blocks.length} blocks • ${formatMinutesToHours(totalPlannedMin)}`;

  if (blocks.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:30px 10px; color:var(--muted); font-size:13px;">
        <p style="margin-bottom:10px;">No blocks scheduled for this date.</p>
        <button class="btn btn-secondary btn-sm" onclick="openLoadTemplateModal()">Load a Template</button>
      </div>
    `;
    return;
  }

  let html = '';
  blocks.forEach((b, idx) => {
    const isDone = b.status === 'done';
    const isRunning = b.status === 'inProgress';
    const timeRangeStr = `${minToTimeOfDay(b.startMin)} - ${minToTimeOfDay(b.endMin)}`;

    html += `
      <div class="tb-block-row" data-id="${b.id}" draggable="true">
        <div class="tb-drag-handle" title="Drag to reorder">
          <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" fill="none"><circle cx="9" cy="6" r="1"/><circle cx="9" cy="12" r="1"/><circle cx="9" cy="18" r="1"/><circle cx="15" cy="6" r="1"/><circle cx="15" cy="12" r="1"/><circle cx="15" cy="18" r="1"/></svg>
        </div>
        <div class="tb-color-dot" style="background:${b.color || '#4F5BF0'};"></div>
        <input type="text" class="tb-row-label" value="${escapeHTML(b.label)}" data-id="${b.id}" title="${escapeHTML(b.label)} (${timeRangeStr})" />
        <input type="number" class="tb-row-dur" value="${b.durationMin}" min="5" max="480" data-id="${b.id}" title="Duration in minutes" />
        <span style="font-size:10px; color:var(--muted); margin-right:2px;">m</span>

        <!-- Start Timer Button -->
        <button class="icon-btn-sm btn-tb-timer" data-id="${b.id}" title="Start Timer for this block" style="color:var(--accent);">
          <svg viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3" fill="currentColor"/></svg>
        </button>

        <!-- Status Checkbox -->
        <input type="checkbox" class="tb-status-check" data-id="${b.id}" ${isDone ? 'checked' : ''} title="Mark Done (Offline / Meeting)" />

        <!-- Delete Button -->
        <button class="icon-btn-sm btn-tb-delete" data-id="${b.id}" title="Delete block" style="color:var(--coral);">
          <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
        </button>
      </div>
    `;
  });

  container.innerHTML = html;

  // Builder Row Event Listeners
  attachBuilderRowEvents(container);
}

function attachBuilderRowEvents(container) {
  // Label Edit
  container.querySelectorAll('.tb-row-label').forEach(input => {
    input.addEventListener('change', () => {
      const id = input.getAttribute('data-id');
      const plan = getSelectedPlan();
      const b = plan.blocks.find(x => x.id === id);
      if (b && input.value.trim()) {
        b.label = input.value.trim();
        saveAppData();
        renderTimelineCanvas(computeStackedBlocks(plan.blocks));
      }
    });
  });

  // Duration Edit
  container.querySelectorAll('.tb-row-dur').forEach(input => {
    input.addEventListener('change', () => {
      const id = input.getAttribute('data-id');
      const plan = getSelectedPlan();
      const b = plan.blocks.find(x => x.id === id);
      const val = parseInt(input.value, 10);
      if (b && !isNaN(val) && val >= 5) {
        b.durationMin = val;
        saveAppData();
        renderTimeBlockView();
      }
    });
  });

  // Start Timer for block
  container.querySelectorAll('.btn-tb-timer').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.getAttribute('data-id');
      startTimerForBlock(id);
    });
  });

  // Status Checkbox (Offline Mark Done)
  container.querySelectorAll('.tb-status-check').forEach(cb => {
    cb.addEventListener('change', () => {
      const id = cb.getAttribute('data-id');
      const plan = getSelectedPlan();
      const b = plan.blocks.find(x => x.id === id);
      if (!b) return;

      if (cb.checked) {
        const promptMinutes = prompt(`Mark "${b.label}" done. Actual minutes practiced:`, b.durationMin);
        if (promptMinutes !== null) {
          const actualMin = parseFloat(promptMinutes) || b.durationMin;
          b.status = 'done';
          b.actualMs = actualMin * 60000;
          saveAppData();
          renderTimeBlockView();
        } else {
          cb.checked = false;
        }
      } else {
        b.status = 'planned';
        b.actualMs = 0;
        saveAppData();
        renderTimeBlockView();
      }
    });
  });

  // Delete Block
  container.querySelectorAll('.btn-tb-delete').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.getAttribute('data-id');
      const plan = getSelectedPlan();
      plan.blocks = plan.blocks.filter(x => x.id !== id);
      saveAppData();
      renderTimeBlockView();
    });
  });

  // Drag-and-drop row reordering
  let draggedRowId = null;
  container.querySelectorAll('.tb-block-row').forEach(row => {
    row.addEventListener('dragstart', (e) => {
      draggedRowId = row.getAttribute('data-id');
      row.classList.add('dragging');
    });
    row.addEventListener('dragend', () => {
      row.classList.remove('dragging');
      draggedRowId = null;
    });
    row.addEventListener('dragover', (e) => {
      e.preventDefault();
    });
    row.addEventListener('drop', (e) => {
      e.preventDefault();
      const targetId = row.getAttribute('data-id');
      if (draggedRowId && targetId && draggedRowId !== targetId) {
        const plan = getSelectedPlan();
        const fromIdx = plan.blocks.findIndex(x => x.id === draggedRowId);
        const toIdx = plan.blocks.findIndex(x => x.id === targetId);
        if (fromIdx >= 0 && toIdx >= 0) {
          const item = plan.blocks.splice(fromIdx, 1)[0];
          // Clear explicit manual position when reordering so it auto-stacks
          delete item.manualStartMin;
          plan.blocks.splice(toIdx, 0, item);
          saveAppData();
          renderTimeBlockView();
        }
      }
    });
  });
}

// Start Timer bound to this Time Block
function startTimerForBlock(blockId) {
  const plan = getSelectedPlan();
  const block = plan.blocks.find(b => b.id === blockId);
  if (!block) return;

  // Use the block's configured duration directly so the user gets their full intended session
  const targetMinutes = Math.max(1, block.durationMin || 25);

  // If block was completed previously, restart clean
  if (block.status === 'done') {
    block.actualMs = 0;
  }
  block.status = 'inProgress';

  // Set Timer State without permanently changing user default setting
  appData.timer.mode = 'focus';
  appData.timer.label = block.label;
  appData.timer.selectedTagIds = [ ...(block.tags || []) ];
  appData.timer.remainingMs = targetMinutes * 60 * 1000;
  appData.timer.plannedMs = appData.timer.remainingMs;
  appData.timer.linkedBlock = { date: selectedTbDate, blockId: block.id };

  saveAppData();

  // Switch to Timer view and start
  switchView('timer');
  startOrResumeTimer();
}

// 2. Render Timeline Canvas with Hour gridlines, Blocks, Gaps, and Now-line
function renderTimelineCanvas(blocks) {
  const hourLabelsEl = document.getElementById('tb-hour-labels');
  const trackEl = document.getElementById('tb-track');
  const dayStart = appData.dayWindow.startMin;
  const dayEnd = appData.dayWindow.endMin;
  const totalMin = Math.max(60, dayEnd - dayStart);
  const totalHeight = totalMin * TB_PIXELS_PER_MIN;

  trackEl.style.height = totalHeight + 'px';
  hourLabelsEl.style.height = totalHeight + 'px';

  // Draw Hour Gridlines & Labels
  let hourHtml = '';
  let gridHtml = '';

  const firstHour = Math.ceil(dayStart / 60);
  const lastHour = Math.floor(dayEnd / 60);

  for (let h = firstHour; h <= lastHour; h++) {
    const minFromStart = (h * 60) - dayStart;
    const topPx = minFromStart * TB_PIXELS_PER_MIN;

    hourHtml += `<div class="tb-hour-label" style="top:${topPx}px;">${padZero(h)}:00</div>`;
    gridHtml += `<div class="tb-hour-gridline" style="top:${topPx}px;"></div>`;

    // 30 min subdivision
    if (minFromStart + 30 < totalMin) {
      gridHtml += `<div class="tb-halfhour-gridline" style="top:${topPx + 30 * TB_PIXELS_PER_MIN}px;"></div>`;
    }
  }
  hourLabelsEl.innerHTML = hourHtml;

  // Calculate and Render Gaps & Blocks
  let elementsHtml = gridHtml;

  // Compute Gaps
  let gapCursor = dayStart;
  const sortedBlocks = [ ...blocks ].sort((a, b) => a.startMin - b.startMin);

  sortedBlocks.forEach(b => {
    if (b.startMin > gapCursor + 4) {
      const gapMin = b.startMin - gapCursor;
      const top = (gapCursor - dayStart) * TB_PIXELS_PER_MIN;
      const height = gapMin * TB_PIXELS_PER_MIN;
      elementsHtml += `
        <div class="tb-gap" style="top:${top}px; height:${height}px;" data-start="${gapCursor}" data-dur="${gapMin}">
          <span>Unscheduled — ${formatMinutesToHours(gapMin)}</span>
        </div>
      `;
    }
    gapCursor = Math.max(gapCursor, b.endMin);
  });

  if (dayEnd > gapCursor + 4) {
    const gapMin = dayEnd - gapCursor;
    const top = (gapCursor - dayStart) * TB_PIXELS_PER_MIN;
    const height = gapMin * TB_PIXELS_PER_MIN;
    elementsHtml += `
      <div class="tb-gap" style="top:${top}px; height:${height}px;" data-start="${gapCursor}" data-dur="${gapMin}">
        <span>Unscheduled — ${formatMinutesToHours(gapMin)}</span>
      </div>
    `;
  }

  // Render Blocks
  sortedBlocks.forEach(b => {
    const top = (b.startMin - dayStart) * TB_PIXELS_PER_MIN;
    const height = Math.max(26, b.durationMin * TB_PIXELS_PER_MIN);
    const color = b.color || '#4F5BF0';
    const isDone = b.status === 'done';
    const isInProgress = b.status === 'inProgress';

    const actualMs = b.actualMs || 0;
    const plannedMs = (b.durationMin || 1) * 60000;
    const isOverrun = actualMs > plannedMs;
    const overrunMin = isOverrun ? Math.round((actualMs - plannedMs) / 60000) : 0;

    // Actual bar overlay
    let actualBarHtml = '';
    if (isDone) {
      const barClass = isOverrun ? 'red' : 'green';
      actualBarHtml = `<div class="tb-actual-bar ${barClass}"></div>`;
    }

    // Overrun tail extending past bottom edge
    let overrunTailHtml = '';
    if (isDone && isOverrun) {
      const tailHeight = overrunMin * TB_PIXELS_PER_MIN;
      overrunTailHtml = `<div class="tb-overrun-tail" style="top:${top + height}px; height:${tailHeight}px;">+${overrunMin}m overrun</div>`;
    }

    const timeRangeStr = `${minToTimeOfDay(b.startMin)} - ${minToTimeOfDay(b.endMin)}`;

    elementsHtml += `
      ${overrunTailHtml}
      <div class="tb-block-item ${isInProgress ? 'inProgress' : ''}" style="top:${top}px; height:${height}px; background:${color}22; border-color:${color};" data-id="${b.id}">
        ${actualBarHtml}
        <div class="tb-block-header">
          <span class="tb-block-title" style="color:#fff;" title="${escapeHTML(b.label)}">${escapeHTML(b.label)}</span>
          <span class="tb-block-time" style="color:${color};">${timeRangeStr}</span>
        </div>
        ${height > 45 ? `<div style="font-size:11px; color:var(--muted);">${b.durationMin} mins planned</div>` : ''}
        <div class="tb-block-resize-handle" data-id="${b.id}" title="Drag edge to resize"></div>
      </div>
    `;
  });

  // Render "Now" line if selected date is today
  if (selectedTbDate === getTodayDateString()) {
    const now = new Date();
    const currentMin = now.getHours() * 60 + now.getMinutes();
    if (currentMin >= dayStart && currentMin <= dayEnd) {
      const nowTop = (currentMin - dayStart) * TB_PIXELS_PER_MIN;
      elementsHtml += `
        <div class="tb-now-line" id="tb-now-line" style="top:${nowTop}px;">
          <div class="tb-now-dot"></div>
        </div>
      `;
    }
  }

  trackEl.innerHTML = elementsHtml;

  // Attach Gap click events (prefills add block modal)
  trackEl.querySelectorAll('.tb-gap').forEach(gapEl => {
    gapEl.addEventListener('click', () => {
      const startMin = parseInt(gapEl.getAttribute('data-start'), 10);
      const dur = parseInt(gapEl.getAttribute('data-dur'), 10);
      openAddBlockModal({ startMin, durationMin: dur });
    });
  });
}

function updateNowLinePosition() {
  if (selectedTbDate !== getTodayDateString()) return;
  const line = document.getElementById('tb-now-line');
  if (!line) return;
  const now = new Date();
  const currentMin = now.getHours() * 60 + now.getMinutes();
  const dayStart = appData.dayWindow.startMin;
  const dayEnd = appData.dayWindow.endMin;
  if (currentMin >= dayStart && currentMin <= dayEnd) {
    const nowTop = (currentMin - dayStart) * TB_PIXELS_PER_MIN;
    line.style.top = nowTop + 'px';
  }
}

// Mouse Drag-to-Move and Drag-to-Resize on timeline
function initTimelineMouseEvents() {
  const trackEl = document.getElementById('tb-track');

  trackEl.addEventListener('mousedown', (e) => {
    const resizeHandle = e.target.closest('.tb-block-resize-handle');
    const blockEl = e.target.closest('.tb-block-item');

    if (resizeHandle) {
      e.stopPropagation();
      const id = resizeHandle.getAttribute('data-id');
      const plan = getSelectedPlan();
      const block = plan.blocks.find(b => b.id === id);
      if (!block) return;

      tbDragState = {
        mode: 'resize',
        id,
        initialY: e.clientY,
        initialDur: block.durationMin
      };
      document.body.style.cursor = 'ns-resize';
    } else if (blockEl) {
      const id = blockEl.getAttribute('data-id');
      const plan = getSelectedPlan();
      const stacked = computeStackedBlocks(plan.blocks);
      const block = stacked.find(b => b.id === id);
      if (!block) return;

      tbDragState = {
        mode: 'move',
        id,
        initialY: e.clientY,
        initialStartMin: block.startMin,
        element: blockEl
      };
      blockEl.classList.add('is-moving');
      document.body.style.cursor = 'grabbing';
    }
  });

  window.addEventListener('mousemove', (e) => {
    if (!tbDragState) return;

    const deltaY = e.clientY - tbDragState.initialY;
    const deltaMin = Math.round((deltaY / TB_PIXELS_PER_MIN) / 5) * 5; // snap to 5 mins

    if (tbDragState.mode === 'resize') {
      const newDur = Math.max(10, tbDragState.initialDur + deltaMin);
      const plan = getSelectedPlan();
      const block = plan.blocks.find(b => b.id === tbDragState.id);
      if (block && block.durationMin !== newDur) {
        block.durationMin = newDur;
        renderTimeBlockView();
      }
    } else if (tbDragState.mode === 'move') {
      const newStart = Math.max(appData.dayWindow.startMin, tbDragState.initialStartMin + deltaMin);
      const plan = getSelectedPlan();
      const block = plan.blocks.find(b => b.id === tbDragState.id);
      if (block && block.manualStartMin !== newStart) {
        block.manualStartMin = newStart;
        renderTimeBlockView();
      }
    }
  });

  window.addEventListener('mouseup', () => {
    if (tbDragState) {
      if (tbDragState.element) tbDragState.element.classList.remove('is-moving');
      tbDragState = null;
      document.body.style.cursor = '';
      saveAppData();
      renderTimeBlockView();
    }
  });
}

// Reschedule remaining day: shifts subsequent blocks later by the overrun amount
function checkOverrunReschedule(blocks) {
  const btn = document.getElementById('btn-tb-reschedule');
  const amountPill = document.getElementById('tb-reschedule-amount');
  let totalOverrunMin = 0;

  blocks.forEach(b => {
    if (b.status === 'done' && b.actualMs && b.actualMs > (b.durationMin * 60000)) {
      totalOverrunMin += Math.round((b.actualMs - (b.durationMin * 60000)) / 60000);
    }
  });

  if (totalOverrunMin > 0) {
    btn.style.display = 'inline-flex';
    amountPill.textContent = `+${totalOverrunMin}m`;
  } else {
    btn.style.display = 'none';
  }
}

function rescheduleRemainingDay() {
  const plan = getSelectedPlan();
  const stacked = computeStackedBlocks(plan.blocks);

  // Find first overrun block
  let overrunShift = 0;
  let hasTriggered = false;

  stacked.forEach((b, idx) => {
    if (!hasTriggered) {
      if (b.status === 'done' && b.actualMs && b.actualMs > (b.durationMin * 60000)) {
        overrunShift += Math.round((b.actualMs - (b.durationMin * 60000)) / 60000);
        hasTriggered = true;
      }
    } else {
      // Shift this later block by overrunShift
      const targetBlock = plan.blocks.find(x => x.id === b.id);
      if (targetBlock && targetBlock.status !== 'done') {
        const curStart = (targetBlock.manualStartMin !== undefined) ? targetBlock.manualStartMin : b.startMin;
        targetBlock.manualStartMin = curStart + overrunShift;
      }
    }
  });

  saveAppData();
  renderTimeBlockView();
  showToast(`Rescheduled remaining day: shifted blocks +${overrunShift}m later`, 'var(--teal)');
}

// Quick Rest Block Adder (5, 15, 30 min)
function addQuickRestBlock(durationMin) {
  const plan = getSelectedPlan();
  const dur = parseInt(durationMin, 10) || 15;
  const label = dur <= 10 ? 'Quick Rest & Hydrate' : (dur <= 20 ? 'Mindful Break & Stretch' : 'Rest & Refreshment');

  const newBlock = {
    id: uid('tb'),
    label: label,
    tags: [],
    durationMin: dur,
    status: 'planned',
    actualMs: 0,
    linkedSessionIds: [],
    color: '#2DD4A7' // Calming teal for rest/recovery
  };

  plan.blocks.push(newBlock);
  saveAppData();
  renderTimeBlockView();
  showToast(`Added ${dur}m Rest Block to schedule`, 'var(--teal)');
}
window.addQuickRestBlock = addQuickRestBlock;

// Copy yesterday's plan quick action
function copyYesterdayPlan() {
  const cur = new Date(selectedTbDate + 'T00:00:00');
  cur.setDate(cur.getDate() - 1);
  const yestStr = formatDateString(cur.getTime());

  const yestPlan = appData.timeblockPlans[yestStr];
  if (!yestPlan || !yestPlan.blocks || yestPlan.blocks.length === 0) {
    alert(`No blocks found on yesterday (${yestStr}).`);
    return;
  }

  if (confirm(`Copy ${yestPlan.blocks.length} blocks from ${yestStr} into ${selectedTbDate}?`)) {
    const plan = getSelectedPlan();
    const cloned = yestPlan.blocks.map(b => ({
      ...b,
      id: uid('tb'),
      status: 'planned',
      actualMs: 0,
      linkedSessionIds: []
    }));

    plan.blocks = [ ...plan.blocks, ...cloned ];
    saveAppData();
    renderTimeBlockView();
    showToast(`Copied ${cloned.length} blocks from yesterday`, 'var(--accent)');
  }
}

// Templates: Save & Load
function openSaveTemplateModal() {
  const plan = getSelectedPlan();
  if (!plan.blocks || plan.blocks.length === 0) {
    alert('Add some blocks before saving as a template.');
    return;
  }

  const name = prompt('Name for this routine template:', 'Daily Deep Flow');
  if (name && name.trim()) {
    const template = {
      id: uid('tpl'),
      name: name.trim(),
      blocks: plan.blocks.map(b => ({
        label: b.label,
        tags: [ ...(b.tags || []) ],
        durationMin: b.durationMin,
        color: b.color || '#4F5BF0'
      }))
    };
    appData.timeblockTemplates.push(template);
    saveAppData();
    showToast(`Saved template "${name.trim()}"`, 'var(--teal)');
  }
}

function openLoadTemplateModal() {
  const modal = document.getElementById('modal-tb-templates');
  const content = document.getElementById('template-modal-content');

  if (appData.timeblockTemplates.length === 0) {
    content.innerHTML = `
      <div style="text-align:center; padding:20px; color:var(--muted);">
        <p style="margin-bottom:12px;">No templates saved yet.</p>
        <button class="btn btn-secondary btn-sm" onclick="closeModal('modal-tb-templates')">Close</button>
      </div>
    `;
  } else {
    let html = '<div style="display:flex; flex-direction:column; gap:12px;">';
    appData.timeblockTemplates.forEach(tpl => {
      const blockSummary = tpl.blocks.map(b => `${escapeHTML(b.label)} (${b.durationMin}m)`).join(', ');
      html += `
        <div class="card" style="background:var(--surface-2); padding:14px; display:flex; justify-content:space-between; align-items:center;">
          <div style="flex:1; min-width:0; margin-right:12px;">
            <div style="font-weight:700; color:#fff; font-size:14px;">${escapeHTML(tpl.name)}</div>
            <div style="font-size:11px; color:var(--muted); margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${blockSummary}</div>
          </div>
          <div style="display:flex; gap:6px;">
            <button class="btn btn-primary btn-sm btn-apply-template" data-id="${tpl.id}">Load into Day</button>
            <button class="icon-btn-sm btn-del-template" data-id="${tpl.id}" style="color:var(--coral);" title="Delete template">
              <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
            </button>
          </div>
        </div>
      `;
    });
    html += '</div>';
    content.innerHTML = html;

    content.querySelectorAll('.btn-apply-template').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-id');
        const tpl = appData.timeblockTemplates.find(x => x.id === id);
        if (tpl) {
          const plan = getSelectedPlan();
          const cloned = tpl.blocks.map(b => ({
            ...b,
            id: uid('tb'),
            status: 'planned',
            actualMs: 0,
            linkedSessionIds: []
          }));
          plan.blocks = [ ...plan.blocks, ...cloned ];
          saveAppData();
          closeModal('modal-tb-templates');
          renderTimeBlockView();
          showToast(`Loaded template "${tpl.name}"`, 'var(--accent)');
        }
      });
    });

    content.querySelectorAll('.btn-del-template').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-id');
        if (confirm('Delete this template?')) {
          appData.timeblockTemplates = appData.timeblockTemplates.filter(x => x.id !== id);
          saveAppData();
          openLoadTemplateModal();
        }
      });
    });
  }

  openModal('modal-tb-templates');
}

// Add/Edit Block Modal Form Handlers
let tbModalSelectedTags = [];

function openAddBlockModal(prefill) {
  const form = document.getElementById('form-add-timeblock');
  form.reset();
  document.getElementById('tb-input-id').value = '';
  document.getElementById('modal-tb-title').textContent = 'Add Time Block';
  document.getElementById('tb-input-color').value = PALETTE[Math.floor(Math.random() * PALETTE.length)];

  if (prefill) {
    if (prefill.label) document.getElementById('tb-input-label').value = prefill.label;
    if (prefill.durationMin) document.getElementById('tb-input-dur').value = prefill.durationMin;
    if (prefill.startMin !== undefined) {
      document.getElementById('tb-input-starttime').value = minToTimeOfDay(prefill.startMin);
    }
  }

  tbModalSelectedTags = [];
  renderTbModalTags();
  openModal('modal-add-timeblock');
  document.getElementById('tb-input-label').focus();
}

function renderTbModalTags() {
  const container = document.getElementById('tb-modal-tags-container');
  let html = '';
  appData.tags.forEach(tag => {
    const isSel = tbModalSelectedTags.includes(tag.id);
    html += `
      <div class="chip ${isSel ? 'selected' : ''}" data-id="${tag.id}">
        <span class="chip-dot" style="background:${tag.color}"></span>
        <span>${escapeHTML(tag.name)}</span>
      </div>
    `;
  });
  container.innerHTML = html;

  container.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      const id = chip.getAttribute('data-id');
      const idx = tbModalSelectedTags.indexOf(id);
      if (idx >= 0) tbModalSelectedTags.splice(idx, 1);
      else tbModalSelectedTags.push(id);
      renderTbModalTags();
    });
  });
}

function handleSaveBlockForm(e) {
  e.preventDefault();
  const label = document.getElementById('tb-input-label').value.trim();
  const dur = parseInt(document.getElementById('tb-input-dur').value, 10) || 30;
  const startStr = document.getElementById('tb-input-starttime').value;
  const color = document.getElementById('tb-input-color').value || '#4F5BF0';

  const plan = getSelectedPlan();
  const newBlock = {
    id: uid('tb'),
    label,
    tags: [ ...tbModalSelectedTags ],
    durationMin: dur,
    status: 'planned',
    actualMs: 0,
    linkedSessionIds: [],
    color
  };

  if (startStr) {
    newBlock.manualStartMin = timeOfDayToMin(startStr);
  }

  plan.blocks.push(newBlock);
  saveAppData();
  closeModal('modal-add-timeblock');
  renderTimeBlockView();
}

// ==========================================
// STICKY NOTE / SCRATCHPAD LOGIC
// ==========================================
let tbStickySaveTimeout = null;

function renderStickyNote() {
  const plan = getSelectedPlan();
  const noteInput = document.getElementById('tb-sticky-note-input');
  if (noteInput && document.activeElement !== noteInput) {
    noteInput.value = plan.notes || '';
  }
  updateStickyNoteMeta(plan.notes || '');
}

function updateStickyNoteMeta(text) {
  const metaEl = document.getElementById('tb-sticky-note-meta');
  if (!metaEl) return;
  const trimmed = (text || '').trim();
  const words = trimmed ? trimmed.split(/\\s+/).filter(Boolean).length : 0;
  const chars = (text || '').length;
  metaEl.textContent = `${words} ${words === 1 ? 'word' : 'words'} • ${chars} chars`;
}

function initStickyNoteListeners() {
  const noteInput = document.getElementById('tb-sticky-note-input');
  const clearBtn = document.getElementById('btn-tb-sticky-clear');
  const toBlockBtn = document.getElementById('btn-tb-note-to-block');
  const statusEl = document.getElementById('tb-sticky-save-status');

  if (noteInput) {
    noteInput.addEventListener('input', () => {
      const plan = getSelectedPlan();
      plan.notes = noteInput.value;
      updateStickyNoteMeta(noteInput.value);

      if (statusEl) {
        statusEl.textContent = 'Saving...';
        statusEl.style.color = '#F59E0B';
      }

      if (tbStickySaveTimeout) clearTimeout(tbStickySaveTimeout);
      tbStickySaveTimeout = setTimeout(() => {
        saveAppData();
        if (statusEl) {
          statusEl.textContent = 'Auto-saved ✓';
          statusEl.style.color = 'rgba(251, 191, 36, 0.85)';
        }
      }, 350);
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      const plan = getSelectedPlan();
      if (!plan.notes || !plan.notes.trim()) return;
      if (confirm('Clear the sticky note for this day?')) {
        plan.notes = '';
        if (noteInput) noteInput.value = '';
        saveAppData();
        updateStickyNoteMeta('');
        if (statusEl) {
          statusEl.textContent = 'Cleared';
          setTimeout(() => {
            if (statusEl) statusEl.textContent = 'Auto-saved';
          }, 1500);
        }
        showToast('Sticky note cleared', 'var(--muted)');
      }
    });
  }

  if (toBlockBtn) {
    toBlockBtn.addEventListener('click', () => {
      if (!noteInput) return;
      let text = '';
      const start = noteInput.selectionStart;
      const end = noteInput.selectionEnd;
      if (start !== undefined && end !== undefined && start !== end) {
        text = noteInput.value.substring(start, end).trim();
      }
      if (!text) {
        const lines = (noteInput.value || '').split('\\n').map(l => l.trim()).filter(Boolean);
        text = lines[0] || '';
      }
      if (!text) {
        openAddBlockModal();
        return;
      }
      const label = text.split('\\n')[0].substring(0, 80);
      openAddBlockModal({ label: label, durationMin: 30 });
      showToast(`Prefilled block from note: "${label}"`, 'var(--accent)');
    });
  }
}
"""
