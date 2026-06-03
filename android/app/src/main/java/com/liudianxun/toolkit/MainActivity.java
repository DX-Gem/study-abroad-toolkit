package com.liudianxun.toolkit;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.view.WindowManager;
import android.os.Build;
import android.view.View;
import android.speech.tts.TextToSpeech;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Locale;

public class MainActivity extends Activity {
    private WebView webView;
    private TextToSpeech tts;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 保留状态栏，不遮挡电量/时间
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            getWindow().setStatusBarColor(android.graphics.Color.parseColor("#C85D3F"));
        }
        // 系统默认白字状态栏（深色背景），无需额外设置

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        // 允许 file:// 下的 fetch 加载本地 JSON 和跨域 API
        settings.setAllowFileAccessFromFileURLs(true);
        settings.setAllowUniversalAccessFromFileURLs(true);
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);
        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        settings.setMediaPlaybackRequiresUserGesture(false);
        // 修复 vivo 等国产手机文字缩放导致的排版问题
        settings.setTextZoom(100);
        settings.setLayoutAlgorithm(WebSettings.LayoutAlgorithm.NORMAL);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                if (url.startsWith("file://") || url.startsWith("about:")) {
                    return false;
                }
                if (url.startsWith("https://api.exchangerate-api.com") ||
                    url.startsWith("https://api.mymemory.translated.net")) {
                    return false;
                }
                try {
                    android.content.Intent intent = new android.content.Intent(
                        android.content.Intent.ACTION_VIEW, android.net.Uri.parse(url));
                    startActivity(intent);
                } catch (Exception ignored) {}
                return true;
            }
        });

        webView.setWebChromeClient(new WebChromeClient());

        // 原生 TTS 引擎（Web Speech API 在 WebView 中不稳定，提供原生兜底）
        tts = new TextToSpeech(this, null);
        // 初始化 TTS（兼容 vivo 讯飞引擎）
        tts.setLanguage(Locale.CHINESE);

        webView.addJavascriptInterface(new Object() {
            @android.webkit.JavascriptInterface
            public String speak(String text, String lang) {
                try {
                    Locale locale = langToLocale(lang);
                    int result = tts.setLanguage(locale);
                    if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                        return "{\"status\":\"UNSUPPORTED\"}";
                    }
                    tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "toolkit_tts");
                    return "{\"status\":\"OK\"}";
                } catch (Exception e) {
                    return "{\"status\":\"ERROR\"}";
                }
            }

            private Locale langToLocale(String lang) {
                switch (lang) {
                    case "zh-CN": case "zh": return Locale.CHINESE;
                    case "en-GB": case "en": return Locale.UK;
                    case "ru-RU": case "ru": return new Locale("ru", "RU");
                    case "kk-KZ": case "kk": return new Locale("kk", "KZ");
                    case "az-AZ": case "az": return new Locale("az", "AZ");
                    case "ja-JA": case "ja": return Locale.JAPANESE;
                    case "ko-KR": case "ko": return Locale.KOREAN;
                    case "de-DE": case "de": return Locale.GERMAN;
                    case "fr-FR": case "fr": return Locale.FRENCH;
                    case "ms-MY": case "ms": return new Locale("ms", "MY");
                    default: return Locale.UK;
                }
            }
        }, "AndroidTTS");

        // 应用内更新接口（v3.8.2起改为浏览器下载，不再需要REQUEST_INSTALL_PACKAGES权限）
        webView.addJavascriptInterface(new Object() {
            @android.webkit.JavascriptInterface
            public void downloadAndInstall(String apkUrl) {
                // 统一用浏览器打开下载链接，兼容所有手机
                try {
                    Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(apkUrl));
                    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    startActivity(intent);
                } catch (Exception e) {
                    new Handler(Looper.getMainLooper()).post(() ->
                        Toast.makeText(MainActivity.this, "请手动复制链接到浏览器下载", Toast.LENGTH_LONG).show());
                }
            }
        }, "AndroidUpdate");

        // 加载本地首页
        webView.loadUrl("file:///android_asset/index.html");
    }

    @Override
    protected void onDestroy() {
        if (tts != null) {
            tts.stop();
            tts.shutdown();
        }
        super.onDestroy();
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
