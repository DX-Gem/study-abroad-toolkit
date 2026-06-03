const CACHE_NAME = 'study-abroad-v5-20260603';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/currency.html',
  '/phrasebook.html',
  '/knowledge.html',
  '/timezone.html',
  '/ledger.html',
  '/countdown.html',
  '/diary.html',
  '/profile.html',
  '/cost.html',
  '/packing.html',
  '/select.html',
  '/onboarding.html',
  '/styles.css',
  '/app.js',
  '/update-checker.js',
  '/sw.js',
  '/manifest.json',
  '/icon-192.png',
  '/icon-512.png',
  '/data/cities.json',
  '/data/packing.json',
  '/data/phrases.json',
  '/data/country-data.js',
  '/data/knowledge.js',
  '/data/phrases_embed.js',
  '/data/phrases_en.js',
  '/data/phrases_ja.js',
  '/data/phrases_ko.js',
  '/data/phrases_de.js',
  '/data/phrases_fr.js',
  '/data/phrases_ms.js',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // 外部 API 请求：网络优先，失败用缓存
  if (url.hostname.includes('exchangerate-api.com') || url.hostname.includes('mymemory')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const cloned = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, cloned));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // 静态资源：缓存优先
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  );
});
