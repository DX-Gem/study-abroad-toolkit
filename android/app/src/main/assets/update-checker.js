// 应用内更新检查器
(function() {
    var CURRENT_VERSION = 14;
    var VERSION_URL = 'https://gitee.com/dianxun-liu/study-abroad-toolkit/raw/main/version.json';

    setTimeout(checkUpdate, 2000);

    function checkUpdate() {
        try {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', VERSION_URL, true);
            xhr.timeout = 10000;
            xhr.onload = function() {
                if (xhr.status !== 200) return;
                try {
                    var info = JSON.parse(xhr.responseText);
                    if (info.versionCode > CURRENT_VERSION) {
                        showUpdateModal(info);
                    }
                } catch(e) {}
            };
            xhr.onerror = function() {};
            xhr.send();
        } catch(e) {}
    }

    function showUpdateModal(info) {
        // 解析 changelog 为列表
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
                    '<button class="modal-btn-cancel" onclick="window._dismissUpdate()">以后再说</button>' +
                    '<button class="modal-btn-update" onclick="window._doUpdate()">立即更新</button>' +
                '</div>' +
            '</div>' +
        '</div>';

        var div = document.createElement('div');
        div.innerHTML = html;
        document.body.appendChild(div.firstElementChild);

        window._updateUrl = info.apkUrl;
        window._dismissUpdate = function() {
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
