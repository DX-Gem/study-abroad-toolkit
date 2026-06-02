// 应用内更新检查器
(function() {
    var CURRENT_VERSION = 16;
    var VERSION_URL = 'https://gitee.com/dianxun-liu/study-abroad-toolkit/raw/main/version.json';

    setTimeout(checkUpdate, 2500);

    function checkUpdate() {
        // 检查今天是否已提醒过（同版本一天只提醒一次）
        var lastCheck = localStorage.getItem('update_last_check');
        var today = new Date().toDateString();
        if (lastCheck === today + '_v' + CURRENT_VERSION) return;

        try {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', VERSION_URL, true);
            xhr.timeout = 10000;
            xhr.onload = function() {
                if (xhr.status !== 200) return;
                try {
                    var info = JSON.parse(xhr.responseText);
                    if (info.versionCode > CURRENT_VERSION) {
                        // 检查这个版本是否被跳过
                        var skipped = localStorage.getItem('update_skipped_version');
                        if (skipped && parseInt(skipped) >= info.versionCode) return;
                        showUpdateModal(info);
                    }
                    localStorage.setItem('update_last_check', today + '_v' + CURRENT_VERSION);
                } catch(e) {}
            };
            xhr.onerror = function() {};
            xhr.send();
        } catch(e) {}
    }

    function showUpdateModal(info) {
        var items = (info.changelog || '').split('·').filter(function(s) { return s.trim(); });
        var listHtml = items.map(function(item) {
            return '<li>' + item.trim() + '</li>';
        }).join('');

        var html = '<div class="modal-overlay" id="updateModal">' +
            '<div class="modal-dialog">' +
                '<div class="modal-header">' +
                    '<div class="version-badge">NEW</div>' +
                    '<h2>' + info.versionName + '</h2>' +
                '</div>' +
                '<div class="modal-body">' +
                    '<ul class="changelog-list">' + listHtml + '</ul>' +
                    '<div class="file-size">' + (info.apkSize || '') + '</div>' +
                '</div>' +
                '<div class="modal-footer">' +
                    '<button class="modal-btn-cancel" onclick="window._skipUpdate()">跳过此版本</button>' +
                    '<button class="modal-btn-update" onclick="window._doUpdate()">立即更新</button>' +
                '</div>' +
            '</div>' +
        '</div>';

        var div = document.createElement('div');
        div.innerHTML = html;
        document.body.appendChild(div.firstElementChild);

        window._updateUrl = info.apkUrl;
        window._updateInfo = info;
        window._skipUpdate = function() {
            // 跳过此版本：记录已跳过的版本号，不再提醒
            if (window._updateInfo) {
                localStorage.setItem('update_skipped_version', window._updateInfo.versionCode);
            }
            var modal = document.getElementById('updateModal');
            if (modal) { modal.style.opacity = '0'; setTimeout(function() { modal.remove(); }, 200); }
        };
        window._doUpdate = function() {
            var modal = document.getElementById('updateModal');
            if (modal) modal.remove();
            if (window.AndroidUpdate) {
                window.AndroidUpdate.downloadAndInstall(window._updateUrl);
            } else {
                window.open(window._updateUrl, '_blank');
            }
        };
    }
})();
