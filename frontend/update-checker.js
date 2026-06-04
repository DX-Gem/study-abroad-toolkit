// ============================================================
// 版本检查器 — 优先走后端代理(解决CORS)，兜底直连Gitee
// ============================================================
(function() {
  var CURRENT_VERSION = 50;
  var GITEE_URL = 'https://gitee.com/dianxun-liu/study-abroad-toolkit/raw/main/frontend/version.json';
  var LOCAL_FALLBACK = 'version.json';

  // 确定 API 地址
  var isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  var API_BASE = isLocal ? 'http://localhost:8000' : 'http://100.117.204.31:8000';

  setTimeout(checkUpdate, 3000);

  function fetchJSON(url, timeout) {
    return new Promise(function(resolve, reject) {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', url, true);
      xhr.timeout = timeout || 8000;
      xhr.onload = function() {
        if (xhr.status === 200) {
          try { resolve(JSON.parse(xhr.responseText)); }
          catch(e) { reject(e); }
        } else {
          reject(new Error('HTTP ' + xhr.status));
        }
      };
      xhr.onerror = function() { reject(new Error('Network error')); };
      xhr.ontimeout = function() { reject(new Error('Timeout')); };
      xhr.send();
    });
  }

  function checkUpdate() {
    // 1. 优先走后端代理（手机能通，无CORS问题）
    fetchJSON(API_BASE + '/api/version', 8000)
      .then(function(info) { processVersion(info); })
      .catch(function() {
        // 2. 后端不通，尝试直连Gitee
        return fetchJSON(GITEE_URL, 8000);
      })
      .then(function(info) {
        if (info) processVersion(info);
      })
      .catch(function() {
        // 3. Gitee也不通，用本地文件
        return fetchJSON(LOCAL_FALLBACK, 5000);
      })
      .then(function(info) {
        if (info) processVersion(info);
      })
      .catch(function() {});
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
