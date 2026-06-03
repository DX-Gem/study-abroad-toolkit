// 自动清理旧 Service Worker（解决路径变更后旧 SW 残留问题）
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.getRegistrations().then((registrations) => {
    registrations.forEach((reg) => {
      console.log('Unregistering old SW:', reg.scope);
      reg.unregister();
    });
  }).then(() => {
    // 清理旧缓存
    if ('caches' in window) {
      caches.keys().then((keys) => {
        keys.forEach((key) => {
          if (key.startsWith('study-abroad-') || key.startsWith('my-app-')) {
            console.log('Deleting old cache:', key);
            caches.delete(key);
          }
        });
      });
    }
  }).then(() => {
    // 延迟注册新 SW，确保旧的全部清理完毕
    setTimeout(() => {
      const scriptPath = document.currentScript ? document.currentScript.src : '';
      const basePath = scriptPath.replace(/\/app\.js.*$/, '');
      const swPath = basePath ? `${basePath}/sw.js` : 'sw.js';

      navigator.serviceWorker.register(swPath)
        .then((reg) => console.log('SW registered:', reg.scope))
        .catch((err) => console.log('SW registration failed:', err));
    }, 500);
  });
}

let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  const banner = document.getElementById('installBanner');
  if (banner) banner.style.display = 'flex';
});

window.installPWA = function() {
  if (deferredPrompt) {
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((result) => {
      console.log('PWA install:', result.outcome);
      deferredPrompt = null;
      const banner = document.getElementById('installBanner');
      if (banner) banner.style.display = 'none';
    });
  }
};

if (window.matchMedia('(display-mode: standalone)').matches) {
  document.documentElement.classList.add('pwa-standalone');
}

// 全局消息红点更新
(function() {
  function updateBadge() {
    try {
      var msgs = JSON.parse(localStorage.getItem('notifications') || '[]');
      var unread = msgs.filter(function(m) { return !m.read; }).length;
      var badge = document.getElementById('notifyBadge');
      if (badge) {
        badge.textContent = unread > 99 ? '99+' : unread;
        if (unread > 0) badge.classList.add('show');
        else badge.classList.remove('show');
      }
    } catch(e) {}
  }
  updateBadge();
  // 每30秒刷新一次红点
  setInterval(updateBadge, 30000);
})();
