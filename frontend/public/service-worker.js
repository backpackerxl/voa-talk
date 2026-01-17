// ==========================
// 打卡工具 Service Worker
// ==========================

const CACHE_NAME = 'voa-talk-v1.2';          // 主缓存
const OFFLINE_PAGE = '/offline.html';             // 兜底页（提前缓存）
const CORE_ASSETS = [
    '/home/chat',
    '/register',
    '/forget',
    '/login',
    '/voatalk64.png',
    '/voatalk128.png',
    '/voatalk256.png',
    OFFLINE_PAGE,   // 把兜底页也一起缓存
];

/* ---------------------------------------
 * 1. 安装：缓存核心资源
 * ------------------------------------- */
self.addEventListener('install', event => {
    console.log('[SW] 安装中...', CACHE_NAME);
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(CORE_ASSETS))
            .then(() => {
                console.log('[SW] 核心资源缓存完成');
                return self.skipWaiting();
            })
            .catch(err => {
                console.error('[SW] 安装缓存失败:', err);
                return self.skipWaiting();
            })
    );
});

/* ---------------------------------------
 * 2. 激活：清理旧缓存
 * ------------------------------------- */
self.addEventListener('activate', event => {
    console.log('[SW] 激活中...');
    event.waitUntil(
        caches.keys().then(names =>
            Promise.all(
                names
                    .filter(n => n !== CACHE_NAME)
                    .map(n => caches.delete(n))
            )
        ).then(() => {
            console.log('[SW] 旧缓存清理完成');
            return self.clients.claim();
        })
    );
});

/* ---------------------------------------
 * 3. 拦截请求：缓存优先 + 后台更新
 * ------------------------------------- */
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);

    // 只处理同源 GET 请求，跳过 API 与非 GET
    if (request.method !== 'GET' ||
        !url.origin.startsWith(self.location.origin) ||
        url.pathname.includes('/api/')) {
        return;
    }

    event.respondWith(
        (async () => {
            // 1) 先读缓存
            const cached = await caches.match(request);

            // 2) 无论有无缓存，都发起网络请求（用于更新/兜底）
            const fetchPromise = fetch(request).catch(() => null);

            if (cached) {
                // 有缓存 → 立即返回，后台更新
                event.waitUntil(
                    (async () => {
                        const networkResp = await fetchPromise;
                        if (networkResp && networkResp.ok) {
                            const cache = await caches.open(CACHE_NAME);
                            await cache.put(request, networkResp.clone());
                        }
                    })()
                );
                return cached;
            }

            // 3) 无缓存 → 等网络
            const networkResp = await fetchPromise;
            if (networkResp && networkResp.ok) {
                const cache = await caches.open(CACHE_NAME);
                await cache.put(request, networkResp.clone());
                return networkResp;
            }

            // 4) 网络也失败 → 返回兜底页
            return caches.match(OFFLINE_PAGE);
        })()
    );
});

/* ---------------------------------------
 * 4. 消息通道：跳过等待
 * ------------------------------------- */
self.addEventListener('message', event => {
    if (event.data === 'skipWaiting') self.skipWaiting();
});