// ============================================================
// PWA 注册 + 自动更新检测 + 更新弹窗
// ============================================================
(function() {
  if (!('serviceWorker' in navigator)) return;

  var isUpdating = false;

  // 注册 SW
  var scriptPath = document.currentScript ? document.currentScript.src : '';
  var basePath = scriptPath.replace(/\/app\.js.*$/, '');
  var swPath = basePath ? basePath + '/sw.js' : 'sw.js';

  navigator.serviceWorker.register(swPath)
    .then(function(reg) {
      console.log('[SW] registered:', reg.scope);

      // 已有等待中的 SW → 立即弹窗
      if (reg.waiting) {
        showUpdateBanner(reg);
      }

      // 发现新 SW 正在安装
      reg.addEventListener('updatefound', function() {
        var newSW = reg.installing;
        if (!newSW) return;
        console.log('[SW] new version found, installing...');

        newSW.addEventListener('statechange', function() {
          // 安装完成，等待激活 → 弹窗
          if (newSW.state === 'installed' && navigator.serviceWorker.controller) {
            console.log('[SW] new version ready, showing banner');
            showUpdateBanner(reg);
          }
        });
      });
    })
    .catch(function(err) {
      console.log('[SW] registration failed:', err);
    });

  // 新 SW 接管后 → 自动刷新
  navigator.serviceWorker.addEventListener('controllerchange', function() {
    if (!isUpdating) return;
    console.log('[SW] new version activated, reloading...');
    window.location.reload();
  });

  // 显示更新横幅
  function showUpdateBanner(reg) {
    // 避免重复弹窗
    if (document.getElementById('updateBanner')) return;
    if (localStorage.getItem('update_dismissed') === 'v' + (new Date().toDateString())) return;

    var banner = document.createElement('div');
    banner.id = 'updateBanner';
    banner.innerHTML = '<span>🔄 发现新版本</span>'
      + '<button id="updateBtn">立即更新</button>'
      + '<button id="updateDismiss" style="background:transparent;color:#fff;opacity:0.6;font-size:0.75rem;border:none;padding:8px;">✕</button>';
    banner.style.cssText = 'position:fixed;bottom:80px;left:16px;right:16px;'
      + 'background:#1C1A18;color:#fff;padding:14px 18px;border-radius:16px;'
      + 'z-index:9999;display:flex;align-items:center;justify-content:space-between;gap:10px;'
      + 'font-size:0.875rem;font-weight:600;box-shadow:0 8px 32px rgba(0,0,0,0.3);'
      + 'animation:slideUp 0.3s ease-out;';
    document.body.appendChild(banner);

    document.getElementById('updateBtn').addEventListener('click', function() {
      isUpdating = true;
      banner.innerHTML = '<span style="text-align:center;width:100%;">⏳ 更新中...</span>';
      // 通知 SW 立即激活
      if (reg.waiting) {
        reg.waiting.postMessage('SKIP_WAITING');
      }
      // 兜底：2秒后强制刷新
      setTimeout(function() { window.location.reload(); }, 2000);
    });

    document.getElementById('updateDismiss').addEventListener('click', function() {
      banner.remove();
      localStorage.setItem('update_dismissed', 'v' + (new Date().toDateString()));
    });
  }
})();

// ============================================================
// 添加动画
// ============================================================
(function() {
  var style = document.createElement('style');
  style.textContent = '@keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }';
  document.head.appendChild(style);
})();

// ============================================================
// PWA 安装提示
// ============================================================
var deferredPrompt;
window.addEventListener('beforeinstallprompt', function(e) {
  e.preventDefault();
  deferredPrompt = e;
  var banner = document.getElementById('installBanner');
  if (banner) banner.style.display = 'flex';
});

window.installPWA = function() {
  if (deferredPrompt) {
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then(function(result) {
      console.log('PWA install:', result.outcome);
      deferredPrompt = null;
      var banner = document.getElementById('installBanner');
      if (banner) banner.style.display = 'none';
    });
  }
};

// ============================================================
// PWA 独立模式检测
// ============================================================
if (window.matchMedia('(display-mode: standalone)').matches) {
  document.documentElement.classList.add('pwa-standalone');
}

// ============================================================
// 全局消息红点
// ============================================================
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
  setInterval(updateBadge, 30000);
})();
