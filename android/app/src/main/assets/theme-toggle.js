// 暗色模式手动切换 + Toast 提示
(function() {
    // 读取用户偏好
    var saved = localStorage.getItem('dark_mode');
    var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // 手动设置优先于系统
    if (saved === 'true' || (!saved && prefersDark)) {
        document.body.classList.add('dark-mode');
    }

    // 创建切换按钮（浮动右下角）
    var btn = document.createElement('button');
    btn.className = 'theme-toggle';
    btn.title = '切换暗色模式';
    updateIcon();
    btn.onclick = function() {
        document.body.classList.toggle('dark-mode');
        var isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('dark_mode', isDark ? 'true' : 'false');
        updateIcon();
        showToast(isDark ? '已切换暗色模式' : '已切换亮色模式');
    };
    document.body.appendChild(btn);

    function updateIcon() {
        btn.textContent = document.body.classList.contains('dark-mode') ? '☀️' : '\u{1F319}';
    }
})();

// Toast 提示
function showToast(msg) {
    var t = document.createElement('div');
    t.className = 'toast';
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(function() {
        t.style.animation = 'toastOut 0.3s ease-out forwards';
        setTimeout(function() { t.remove(); }, 300);
    }, 1800);
}
