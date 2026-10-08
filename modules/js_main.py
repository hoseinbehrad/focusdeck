# JavaScript Main Bootstrapper Module
JS_MAIN = """
// ==========================================
// 12. BOOTSTRAPPER & APPLICATION INITIALIZATION
// ==========================================

window.addEventListener('DOMContentLoaded', async () => {
  // 1. Load persistent data (IndexedDB records; one-time move from old localStorage format)
  await loadAppData();

  // 2. Initialize modules
  initViewsAndNavigation();
  initTimerEngine();
  initTimeBlockView();
  initSkillsView();
  initBackupView();
  initSyncView();

  // 3. Initial rendering
  renderAllViews();
  updateBackupTimestampsUI();
});
"""
