// 基础Service Worker配置
const CACHE_NAME = 'voa-talk-v1';
const OFFLINE_PAGE = '/offline.html';

// 注入构建资源列表（Workbox会自动替换此占位符）
const PRECACHE_ASSETS = self.__WB_MANIFEST || [];

// 安装阶段：预缓存核心资源
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll([...PRECACHE_ASSETS, OFFLINE_PAGE]);
      })
      .then(() => self.skipWaiting())
  );
});

// 激活阶段：清理旧缓存
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
    .then(() => self.clients.claim())
  );
});

// 处理请求：缓存优先策略
self.addEventListener('fetch', event => {
  // 只处理GET请求
  if (event.request.method !== 'GET') return;
  
  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        // 缓存命中，直接返回
        if (cachedResponse) {
          return cachedResponse;
        }
        
        // 缓存未命中，发起网络请求
        return fetch(event.request)
          .then(networkResponse => {
            // 克隆响应，因为响应流只能使用一次
            const responseToCache = networkResponse.clone();
            
            // 将新请求加入缓存
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });
            
            return networkResponse;
          })
          .catch(() => {
            // 网络请求失败，返回离线页面
            return caches.match(OFFLINE_PAGE);
          });
      })
  );
});
