// 应用内更新检查器
(function() {
    var CURRENT_VERSION = 8; // 当前版本号（与 version.json 同步更新）
    var VERSION_URL = 'https://gitee.com/dianxun-liu/study-abroad-toolkit/raw/main/version.json';

    // 延迟检查，等页面加载完
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
                        showUpdateDialog(info);
                    }
                } catch(e) {}
            };
            xhr.onerror = function() {};
            xhr.send();
        } catch(e) {}
    }

    function showUpdateDialog(info) {
        var msg = '\u{1F310} 发现新版本 ' + info.versionName + '\n\n';
        msg += '更新内容：\n' + (info.changelog || '优化和修复') + '\n\n';
        msg += '大小：' + (info.apkSize || '未知') + '\n\n';
        msg += '是否立即更新？';

        if (confirm(msg)) {
            doUpdate(info.apkUrl);
        }
    }

    function doUpdate(url) {
        if (window.AndroidUpdate) {
            window.AndroidUpdate.downloadAndInstall(url);
        } else {
            // 浏览器环境：直接打开下载链接
            window.open(url, '_blank');
        }
    }
})();
