// ============================================================
// 版本检查器 — 检测 Gitee 上的 version.json
// 用于 APK 更新提示和兜底更新检测
// ============================================================
(function() {
  var CURRENT_VERSION = 50;  // 与 version.json 同步
  var VERSION_URL = 'https://gitee.com/dianxun-liu/study-abroad-toolkit/raw/main/frontend/version.json';
  var LOCAL_FALLBACK = 'version.json';  // 本地降级

  setTimeout(checkUpdate, 3000);

  function checkUpdate() {
    // PWA 场景：SW 自动更新已覆盖，这里作为 APK/兜底
    try {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', VERSION_URL, true);
      xhr.timeout = 8000;
      xhr.onload = function() {
        if (xhr.status !== 200) return;
        try {
          var info = JSON.parse(xhr.responseText);
          processVersion(info);
        } catch(e) {}
      };
      xhr.onerror = function() {
        // Gitee 不通，尝试本地
        tryLocal();
      };
      xhr.send();
    } catch(e) {
      tryLocal();
    }
  }

  function tryLocal() {
    try {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', LOCAL_FALLBACK, true);
      xhr.timeout = 5000;
      xhr.onload = function() {
        if (xhr.status !== 200) return;
        try {
          var info = JSON.parse(xhr.responseText);
          processVersion(info);
        } catch(e) {}
      };
      xhr.send();
    } catch(e) {}
  }

  function processVersion(info) {
    var latestCode = info.versionCode || 0;
    if (latestCode <= CURRENT_VERSION) return;

    // 已跳过此版本
    var skipped = parseInt(localStorage.getItem('update_skipped_version') || '0');
    if (skipped >= latestCode) return;

    // 24小时内不重复弹
    var lastShown = parseInt(localStorage.getItem('update_last_shown') || '0');
    if (Date.now() - lastShown < 86400000) return;

    localStorage.setItem('update_last_shown', Date.now());

    // 检测是否在 APK WebView 中
    var isAPK = (window.AndroidUpdate || navigator.userAgent.includes('Android'));
    showUpdateModal(info, isAPK);
  }

  function showUpdateModal(info, isAPK) {
    var html = '<div class="modal-overlay" id="updateModal">'
      + '<div class="modal-dialog">'
        + '<div class="modal-header">'
          + '<div class="version-badge">NEW</div>'
          + '<h2>' + (info.versionName || '新版本') + '</h2>'
        + '</div>'
        + '<div class="modal-body">'
          + '<p style="font-size:0.875rem;color:var(--text-muted);margin-bottom:8px;">' + (info.changelog || '有新版本可用') + '</p>'
          + '<div style="font-size:0.75rem;color:var(--text-muted);">' + (info.apkSize || '') + '</div>'
        + '</div>'
        + '<div class="modal-footer">'
          + '<button class="modal-btn-cancel" onclick="window._skipUpdate()">跳过</button>';

    if (isAPK && info.apkUrl) {
      // APK 更新：打开浏览器下载（移除 REQUEST_INSTALL_PACKAGES 权限后不再应用内安装）
      html += '<button class="modal-btn-update" onclick="window._doUpdate()">下载更新</button>';
    } else {
      html += '<button class="modal-btn-update" onclick="window._doReload()">刷新页面</button>';
    }

    html += '</div></div></div>';

    var div = document.createElement('div');
    div.innerHTML = html;
    document.body.appendChild(div.firstElementChild);

    window._updateInfo = info;
    window._updateUrl = info.apkUrl;

    window._skipUpdate = function() {
      if (window._updateInfo) {
        localStorage.setItem('update_skipped_version', window._updateInfo.versionCode);
      }
      var modal = document.getElementById('updateModal');
      if (modal) { modal.style.opacity = '0'; setTimeout(function() { modal.remove(); }, 200); }
    };

    window._doUpdate = function() {
      var modal = document.getElementById('updateModal');
      if (modal) modal.remove();
      // 统一用浏览器打开下载链接（兼容所有手机，无需特殊权限）
      window.open(window._updateUrl, '_blank');
    };

    window._doReload = function() {
      var modal = document.getElementById('updateModal');
      if (modal) modal.remove();
      // 强制清除 SW 缓存并刷新
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.getRegistrations().then(function(regs) {
          regs.forEach(function(reg) { reg.unregister(); });
        }).then(function() {
          if ('caches' in window) {
            caches.keys().then(function(keys) {
              Promise.all(keys.map(function(k) { return caches.delete(k); }));
            });
          }
        }).then(function() {
          window.location.reload();
        });
      } else {
        window.location.reload();
      }
    };
  }
})();
