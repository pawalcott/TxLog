# -*- coding: utf-8 -*-
"""Builds the installable phone version of Tx Field Log into TxLog/app/ from txlog_app.html.

    python TxLog/build.py

app/ holds index.html (the page with its own <head>), manifest.webmanifest, sw.js (offline cache) and two icons.
Put the app folder on any HTTPS web host (or open index.html straight from the phone's storage); on the phone open it
once and use "Add to Home Screen" (iPhone: Safari > Share; Android: Chrome menu).  It then runs offline.
It also writes index.html beside app/ that opens the app, so the site's own address (e.g. GitHub Pages) shows it.

Updates: the build version (from the page's contents) names the offline cache, and the page is fetched from the
network first (the cached copy only when offline or after 4 s), so a phone gets a new build the next time it opens
the app with a connection.  The build shows at the bottom of the page.
"""
import datetime
import hashlib
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'app')

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0f766e">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Tx Log">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}[hidden]{display:none!important}</style>
'''
TAIL = '''<p style="text-align:center;color:#8a9a96;font:11px system-ui,sans-serif;margin:18px 0 10px">Tx Log build %s</p>
<script>
if ('serviceWorker' in navigator && location.protocol === 'https:') {
  navigator.serviceWorker.register('sw.js').then(function (r) { r.update(); }).catch(function () {});
}
</script>
</body>
</html>
'''
ROOT = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tx Field Log</title>
<meta http-equiv="refresh" content="0; url=app/">
<script>location.replace('app/' + location.search + location.hash);</script>
</head><body style="font:16px system-ui,sans-serif;padding:24px">
<p>Opening <a href="app/">Tx Field Log</a> ...</p>
</body></html>
'''
MANIFEST = '''{
  "name": "Tx Field Log",
  "short_name": "Tx Log",
  "start_url": "./index.html",
  "display": "standalone",
  "background_color": "#eef1f0",
  "theme_color": "#0f766e",
  "icons": [
    {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}
  ]
}
'''
SW = '''const CACHE = '%s';
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
'''


def icon(size, path):
    """Teal rounded square with a white transmitter pulse."""
    from PIL import Image, ImageDraw
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, size - 1, size - 1), radius=size // 5, fill=(15, 118, 110, 255))
    s, w = size / 100.0, max(2, size // 16)
    pts = [(14, 62), (30, 62), (30, 34), (50, 34), (50, 62), (70, 62), (70, 34), (86, 34)]
    d.line([(x * s, y * s) for x, y in pts], fill=(255, 255, 255, 255), width=w, joint='curve')
    im.save(path)


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(HERE, 'txlog_app.html'), encoding='utf-8') as f:
        page = f.read()
    page = re.sub(r'<meta name="claude:[^>]*>\s*', '', page)    # only meaningful inside the artifact viewer
    build = '{} {}'.format(datetime.date.today().isoformat(), hashlib.sha1(page.encode('utf-8')).hexdigest()[:7])
    title, rest = page.split('\n', 1)
    with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(HEAD + title + '\n</head>\n<body>\n' + rest + TAIL % build)
    with open(os.path.join(OUT, 'manifest.webmanifest'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(MANIFEST)
    with open(os.path.join(OUT, 'sw.js'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(SW % ('txlog-' + build.split()[1]))
    with open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(ROOT)
    icon(192, os.path.join(OUT, 'icon-192.png'))
    icon(512, os.path.join(OUT, 'icon-512.png'))
    print('Built', OUT, '- build', build)


if __name__ == '__main__':
    main()
