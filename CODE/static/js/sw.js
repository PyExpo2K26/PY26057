var CACHE_NAME = 'farmio-cache-v1';
var urlsToCache = [
  '/',
  '/static/css/style.css', // Adjust path to your main CSS
  '/static/js/main.js'     // Adjust path to your main JS
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});