# JavaScript installable-app (PWA) module
JS_PWA = r"""
// ==========================================
// 14. INSTALLABLE APP (service worker, updates, install button)
// ==========================================
let _deferredInstallPrompt = null;
let _updateRequested = false;

function initPWA() {
  const secure = location.protocol === 'https:' || location.hostname === 'localhost';
  if (!('serviceWorker' in navigator) || !secure) return; // e.g. the file:// copy on the PC

  navigator.serviceWorker.register('/sw.js').then(reg => {
    const offerIfWaiting = () => {
      if (reg.waiting && navigator.serviceWorker.controller) showUpdateBar(reg.waiting);
    };
    offerIfWaiting();
    reg.addEventListener('updatefound', () => {
      const nw = reg.installing;
      if (nw) nw.addEventListener('statechange', () => { if (nw.state === 'installed') offerIfWaiting(); });
    });
    // Check for a new version hourly while the app stays open (fails quietly when offline)
    setInterval(() => reg.update().catch(() => {}), 60 * 60 * 1000);
  }).catch(err => console.warn('[FocusDeck] service worker registration failed:', err));

  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (!_updateRequested) return; // first install also changes controller; don't reload then
    _updateRequested = false;
    Promise.resolve(flushSaves()).finally(() => location.reload());
  });

  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault();
    _deferredInstallPrompt = e;
    const btn = document.getElementById('btn-install-app');
    if (btn) btn.style.display = '';
  });
  window.addEventListener('appinstalled', () => {
    _deferredInstallPrompt = null;
    const btn = document.getElementById('btn-install-app');
    if (btn) btn.style.display = 'none';
    showToast('FocusDeck installed', 'var(--teal)');
  });

  const btn = document.getElementById('btn-install-app');
  if (btn) btn.addEventListener('click', async () => {
    if (!_deferredInstallPrompt) return;
    _deferredInstallPrompt.prompt();
    try { await _deferredInstallPrompt.userChoice; } catch (e) { /* ignore */ }
    _deferredInstallPrompt = null;
    btn.style.display = 'none';
  });
}

function showUpdateBar(waitingWorker) {
  let bar = document.getElementById('update-bar');
  if (!bar) {
    bar = document.createElement('div');
    bar.id = 'update-bar';
    bar.setAttribute('role', 'status');
    bar.innerHTML = '<span>A new version of FocusDeck is ready.</span>' +
      '<button type="button" id="btn-update-reload">Reload</button>';
    document.body.appendChild(bar);
  }
  bar.style.display = 'flex';
  document.getElementById('btn-update-reload').onclick = () => {
    _updateRequested = true;
    waitingWorker.postMessage('skipWaiting');
  };
}
"""
