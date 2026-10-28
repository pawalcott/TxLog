# -*- coding: utf-8 -*-
"""Builds the installable phone version of Tx Field Log into TxLog/app/ from txlog_app.html.

    python TxLog/build.py

app/ holds index.html (the page with its own <head>), manifest.webmanifest, sw.js (offline cache) and two icons.
Put the app folder on any HTTPS web host (or open index.html straight from the phone's storage); on the phone open it
once and use "Add to Home Screen" (iPhone: Safari > Share; Android: Chrome menu).  It then runs offline.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'app')
VERSION = 'txlog-1'

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
TAIL = '''<script>
if ('serviceWorker' in navigator && location.protocol === 'https:') {
  navigator.serviceWorker.register('sw.js').catch(function () {});
}
</script>
</body>
</html>
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
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => {
    if (res.ok && new URL(e.request.url).origin === location.origin) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }
    return res;
  }).catch(() => caches.match('./index.html'))));
});
''' % VERSION


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
    title, rest = page.split('\n', 1)
    with open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(HEAD + title + '\n</head>\n<body>\n' + rest + TAIL)
    with open(os.path.join(OUT, 'manifest.webmanifest'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(MANIFEST)
    with open(os.path.join(OUT, 'sw.js'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(SW)
    icon(192, os.path.join(OUT, 'icon-192.png'))
    icon(512, os.path.join(OUT, 'icon-512.png'))
    print('Built', OUT)


if __name__ == '__main__':
    main()
