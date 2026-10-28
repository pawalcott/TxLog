const CACHE = 'txlog-3460dad';
const FILES = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png'];
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())));
// network first (a new build reaches the phone), the cached copy when offline or after 4 s
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  const net = fetch(e.request, {cache: 'no-cache'}).then(res => {
    if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
    return res;
  });
  const slow = new Promise(ok => setTimeout(ok, 4000)).then(() => caches.match(e.request));
  e.respondWith(Promise.race([net, slow.then(r => r || net)]).then(r => r || net)
    .catch(() => caches.match(e.request).then(r => r || caches.match('./index.html'))));
});
