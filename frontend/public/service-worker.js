
const CONFIG = {
    CACHE_NAME: 'voa-talk-v1.2.11', // 版本号更新
    OFFLINE_PAGE: '/offline.html',
    // 1. 核心必缓存资源（入口HTML + 兜底页 + 图片）
    CORE_ASSETS: [
        '/index.html',          // SPA 唯一入口HTML（关键！）
        '/offline.html',
        '/voatalk64.png',
        '/voatalk128.png',
        '/voatalk256.png'
    ],
    // 2. 需要缓存的静态资源类型（正则匹配）
    CACHEABLE_ASSET_PATTERNS: [
        /^\/assets\/.+\.(js|css|png|svg|woff2|woff|ttf)$/, // Vite打包的静态资源
        /^\/@vite\/client/,                                // Vite客户端脚本
        /^\/@id\/.+/                                       // Vite模块ID脚本
    ]
};

/* ---------------------------------------
 * 1. 安装：只缓存核心资源（入口HTML+图片）
 * ------------------------------------- */
self.addEventListener('install', event => {
    console.log('[SW] 安装中（仅缓存静态资源）:', CONFIG.CACHE_NAME);

    const installTask = async () => {
        const cache = await caches.open(CONFIG.CACHE_NAME);
        // 只缓存核心资源（入口HTML+图片），JS/CSS等在首次请求时缓存
        try {
            await cache.addAll(CONFIG.CORE_ASSETS);
            console.log('[SW] 核心资源（入口HTML/图片）缓存完成');
        } catch (err) {
            console.error('[SW] 核心资源缓存失败:', err);
        }
        await self.skipWaiting();
    };

    event.waitUntil(installTask());
});

/* ---------------------------------------
 * 2. 激活：清理旧缓存 + 接管客户端
 * ------------------------------------- */
self.addEventListener('activate', event => {
    console.log('[SW] 激活新版本');

    const activateTask = async () => {
        // 清理所有旧缓存
        const cacheNames = await caches.keys();
        await Promise.all(
            cacheNames.map(name => name !== CONFIG.CACHE_NAME && caches.delete(name))
        );
        // 强制接管所有客户端
        await self.clients.claim();
        console.log('[SW] 激活完成，旧缓存已清理');

        // 通知客户端刷新
        const allClients = await self.clients.matchAll({ type: 'window' });
        allClients.forEach(client => {
            client.postMessage({ type: 'SW_UPDATED', cacheName: CONFIG.CACHE_NAME });
        });
    };

    event.waitUntil(activateTask());
});

/* ---------------------------------------
 * 3. 拦截请求：核心逻辑（缓存JS/CSS，路由返回入口HTML）
 * ------------------------------------- */
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);

    // 跳过：非GET请求、API请求、跨域请求
    if (
        request.method !== 'GET' ||
        !url.origin.includes(self.location.origin) ||
        url.pathname.includes('/voatalk_api/')
    ) {
        return;
    }

    event.respondWith(
        (async () => {
            const cache = await caches.open(CONFIG.CACHE_NAME);
            let response = null;

            // 场景1：请求的是静态资源（JS/CSS/图片等）→ 缓存优先
            if (CONFIG.CACHEABLE_ASSET_PATTERNS.some(pattern => pattern.test(url.pathname))) {
                // 先读缓存
                response = await cache.match(request);
                if (response) {
                    // 后台异步更新缓存（保证资源最新）
                    fetch(request).then(networkResp => {
                        if (networkResp.ok) cache.put(request, networkResp.clone());
                    });
                    return response;
                }
                // 无缓存则走网络，成功后缓存
                try {
                    const networkResp = await fetch(request);
                    if (networkResp.ok) cache.put(request, networkResp.clone());
                    return networkResp;
                } catch (err) {
                    // 静态资源加载失败 → 返回兜底页
                    return cache.match(CONFIG.OFFLINE_PAGE);
                }
            }

            // 场景2：请求的是路由（如/home/task）→ 返回入口HTML
            if (url.pathname !== '/index.html' && !url.pathname.includes('.')) {
                // 先读缓存的入口HTML
                response = await cache.match('/index.html');
                if (response) return response;
                // 无缓存则请求入口HTML并缓存
                try {
                    const networkResp = await fetch('/index.html');
                    if (networkResp.ok) cache.put('/index.html', networkResp.clone());
                    return networkResp;
                } catch (err) {
                    return cache.match(CONFIG.OFFLINE_PAGE);
                }
            }

            // 场景3：请求的是入口HTML → 缓存优先
            response = await cache.match(request);
            if (response) return response;
            // 无缓存则走网络
            try {
                const networkResp = await fetch(request);
                if (networkResp.ok && networkResp.status === 200) cache.put(request, networkResp.clone());
                return networkResp;
            } catch (err) {
                return cache.match(CONFIG.OFFLINE_PAGE);
            }
        })()
    );
});

/* ---------------------------------------
 * 4. 消息通信：兼容手动更新
 * ------------------------------------- */
self.addEventListener('message', event => {
    if (event.data === 'skipWaiting') self.skipWaiting();
    if (event.data.type === 'CLIENT_REFRESHED') {
        console.log('[SW] 客户端已刷新，新缓存生效');
    }
});