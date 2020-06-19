const cachePrefix = 'pdf_splitter'
const version = '0.0.1'
const cacheName = `${cachePrefix}-${version}`

var urlsToCache = [
  './',
  './dero.svg',
  './dero_256.ico',
  './dero_192.png',
  './dero_512.png',
  './style.css',
]

self.addEventListener('install', event => {
  console.log('install')
  event.waitUntil(
    caches.open(cacheName)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache)
      })
  )
})

self.addEventListener('fetch', event => {
  console.log('fetch')
  event.respondWith(
    caches.match(event.request, {
      ignoreSearch:true
    })
      .then(response => {
        return response || fetch(event.request)
      }
    )
  )
})

self.addEventListener('activate', event => {
  console.log('activate')
  event.waitUntil(self.clients.claim());
})
