# JavaScript Backup & Restore Engine Module
JS_BACKUP = """
// ==========================================
// 6. WHOLE-APP BACKUP & RESTORE ENGINE
// ==========================================

let pendingImportData = null;

function initBackupView() {
  // Export All Data
  document.getElementById('btn-backup-export-all').addEventListener('click', handleExportAllData);

  // Import All Data File Input
  const fileInput = document.getElementById('backup-import-file');
  fileInput.addEventListener('change', handleBackupFileSelect);

  // Restore Last Snapshot
  document.getElementById('btn-backup-restore-snapshot').addEventListener('click', handleRestoreSnapshot);

  // Backup Modal Buttons
  document.getElementById('btn-close-backup-modal').addEventListener('click', () => closeModal('modal-backup-import'));
  document.getElementById('btn-cancel-backup-import').addEventListener('click', () => closeModal('modal-backup-import'));
  document.getElementById('btn-confirm-import-merge').addEventListener('click', () => applyImport('merge'));
  document.getElementById('btn-confirm-import-replace').addEventListener('click', () => applyImport('replace'));

  updateBackupTimestampsUI();
}

function updateBackupTimestampsUI() {
  const exportEl = document.getElementById('backup-last-export-time');
  const importEl = document.getElementById('backup-last-import-time');
  const snapBtn = document.getElementById('btn-backup-restore-snapshot');

  if (exportEl) {
    exportEl.textContent = appData.meta && appData.meta.lastExport
      ? `${formatDateString(appData.meta.lastExport)} ${formatTimeString(appData.meta.lastExport)}`
      : 'Never';
  }

  if (importEl) {
    importEl.textContent = appData.meta && appData.meta.lastImport
      ? `${formatDateString(appData.meta.lastImport)} ${formatTimeString(appData.meta.lastImport)}`
      : 'Never';
  }

  if (snapBtn) {
    if (deviceSnapshots && deviceSnapshots.length > 0) {
      const latest = deviceSnapshots[0];
      snapBtn.disabled = false;
      snapBtn.title = `Rollback to safety snapshot from ${formatTimeString(latest.timestamp)}`;
      snapBtn.querySelector('span').textContent = `Restore Snapshot (${formatTimeString(latest.timestamp)})`;
    } else {
      snapBtn.disabled = true;
      snapBtn.title = 'No snapshots available';
      snapBtn.querySelector('span').textContent = 'Restore Last Snapshot';
    }
  }
}

// 1. Export All Data: timestamped JSON download
function handleExportAllData() {
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = padZero(now.getMonth() + 1);
  const dd = padZero(now.getDate());
  const hh = padZero(now.getHours());
  const min = padZero(now.getMinutes());
  const ss = padZero(now.getSeconds());

  const filename = `focusdeck-backup-${yyyy}-${mm}-${dd}-${hh}${min}${ss}.json`;

  if (!appData.meta) appData.meta = {};
  appData.meta.lastExport = Date.now();
  saveAppData();
  updateBackupTimestampsUI();

  const dataStr = JSON.stringify(exportableAppData(), null, 2);
  const blob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  showToast('Whole-app backup exported successfully', 'var(--teal)');
}

// 2. Validate and show Import confirmation modal
function handleBackupFileSelect(e) {
  const file = e.target.files && e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (evt) => {
    try {
      const parsed = JSON.parse(evt.target.result);
      if (!parsed || typeof parsed !== 'object' || (!parsed.sessions && !parsed.schemaVersion)) {
        alert('Invalid backup file. Missing FocusDeck data schema.');
        e.target.value = '';
        return;
      }

      const migrated = migrate(parsed);
      pendingImportData = migrated;

      // Calculate summary metrics
      const sessCount = (migrated.sessions || []).length;
      const skillsCount = (migrated.skills || []).length;

      let tbCount = 0;
      if (migrated.timeblockPlans) {
        Object.values(migrated.timeblockPlans).forEach(p => {
          tbCount += (p.blocks || []).length;
        });
      }

      let dateRangeStr = 'No sessions recorded';
      if (sessCount > 0) {
        const sortedTimes = migrated.sessions.map(s => s.startedAt).filter(Boolean).sort((a, b) => a - b);
        if (sortedTimes.length > 0) {
          dateRangeStr = `${formatDateString(sortedTimes[0])} to ${formatDateString(sortedTimes[sortedTimes.length - 1])}`;
        }
      }

      // Populate modal summary
      const summaryEl = document.getElementById('backup-import-summary');
      summaryEl.innerHTML = `
        <div style="font-size:12px; color:var(--muted); line-height:1.8;">
          <div>Sessions in file: <strong style="color:#fff;">${sessCount}</strong></div>
          <div>Mastery Skills: <strong style="color:#fff;">${skillsCount}</strong></div>
          <div>Time Block items: <strong style="color:#fff;">${tbCount}</strong></div>
          <div>History range: <strong style="color:var(--accent);">${dateRangeStr}</strong></div>
          <div>Schema Version: <strong style="color:var(--teal);">${migrated.schemaVersion || '1'}</strong></div>
        </div>
      `;

      openModal('modal-backup-import');
    } catch (err) {
      alert('Could not read or parse JSON file: ' + err.message);
    }
    e.target.value = '';
  };
  reader.readAsText(file);
}

// 3. Apply Import (Merge or Replace)
function applyImport(mode) {
  if (!pendingImportData) return;

  // Always create an automatic safety snapshot of current data before modifying (device-only)
  createSafetySnapshot(`Pre-import safety snapshot (${mode})`);

  if (mode === 'replace') {
    // Keep this device's timer and backup times; everything else comes from the file
    const keepTimer = appData.timer;
    const keepMeta = appData.meta;
    appData = pendingImportData;
    appData.timer = keepTimer;
    appData.meta = keepMeta;
  } else if (mode === 'merge') {
    // 1. Merge sessions (deduplicate by id)
    const existingSessIds = new Set(appData.sessions.map(s => s.id));
    (pendingImportData.sessions || []).forEach(sess => {
      if (!existingSessIds.has(sess.id)) {
        appData.sessions.push(sess);
        existingSessIds.add(sess.id);
      }
    });

    // 2. Merge skills (deduplicate by id or name)
    const existingSkillIds = new Set(appData.skills.map(s => s.id));
    const existingSkillNames = new Set(appData.skills.map(s => s.name.toLowerCase()));
    (pendingImportData.skills || []).forEach(sk => {
      if (!existingSkillIds.has(sk.id) && !existingSkillNames.has(sk.name.toLowerCase())) {
        appData.skills.push(sk);
        existingSkillIds.add(sk.id);
      }
    });

    // 3. Merge manual backlogs
    const existingBkIds = new Set((appData.manualBacklogEntries || []).map(b => b.id));
    (pendingImportData.manualBacklogEntries || []).forEach(bk => {
      if (!existingBkIds.has(bk.id)) {
        appData.manualBacklogEntries.push(bk);
        existingBkIds.add(bk.id);
      }
    });

    // 4. Merge time block plans
    if (pendingImportData.timeblockPlans) {
      if (!appData.timeblockPlans) appData.timeblockPlans = {};
      Object.entries(pendingImportData.timeblockPlans).forEach(([dateStr, plan]) => {
        if (!appData.timeblockPlans[dateStr]) {
          appData.timeblockPlans[dateStr] = plan;
        } else {
          // Merge blocks within date
          const existingBlockIds = new Set((appData.timeblockPlans[dateStr].blocks || []).map(b => b.id));
          (plan.blocks || []).forEach(blk => {
            if (!existingBlockIds.has(blk.id)) {
              appData.timeblockPlans[dateStr].blocks.push(blk);
              existingBlockIds.add(blk.id);
            }
          });
        }
      });
    }

    // 5. Merge templates
    const existingTplIds = new Set((appData.timeblockTemplates || []).map(t => t.id));
    (pendingImportData.timeblockTemplates || []).forEach(tpl => {
      if (!existingTplIds.has(tpl.id)) {
        appData.timeblockTemplates.push(tpl);
        existingTplIds.add(tpl.id);
      }
    });

    // 6. Merge tags
    const existingTagNames = new Set(appData.tags.map(t => t.name.toLowerCase()));
    (pendingImportData.tags || []).forEach(t => {
      if (!existingTagNames.has(t.name.toLowerCase())) {
        appData.tags.push(t);
        existingTagNames.add(t.name.toLowerCase());
      }
    });
  }

  if (!appData.meta) appData.meta = {};
  appData.meta.lastImport = Date.now();
  pendingImportData = null;

  saveAppData();
  closeModal('modal-backup-import');
  renderAllViews();
  updateBackupTimestampsUI();
  showToast(`Successfully applied backup import (${mode})`, 'var(--teal)');
}

// 4. Restore Last Snapshot
function handleRestoreSnapshot() {
  if (!deviceSnapshots || deviceSnapshots.length === 0) {
    alert('No recovery snapshot available.');
    return;
  }

  const latest = deviceSnapshots[0];
  const timeStr = `${formatDateString(latest.timestamp)} at ${formatTimeString(latest.timestamp)}`;

  if (confirm(`Revert FocusDeck back to safety snapshot from ${timeStr}?`)) {
    try {
      const restored = JSON.parse(latest.data);
      const keepTimer = appData.timer;
      const keepMeta = appData.meta;
      deviceSnapshots = deviceSnapshots.slice(1);
      saveDeviceSnapshots();
      appData = migrate(restored);
      appData.timer = keepTimer;
      appData.meta = keepMeta;
      saveAppData();
      renderAllViews();
      updateBackupTimestampsUI();
      showToast('Successfully reverted to last safety snapshot', 'var(--accent)');
    } catch (err) {
      alert('Could not restore snapshot: ' + err.message);
    }
  }
}
"""
