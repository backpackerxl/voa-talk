const { defineConfig } = require('@vue/cli-service');
const fs = require('fs');
const path = require('path');
module.exports = defineConfig({
    transpileDependencies: true,
    configureWebpack: {
        resolve: {
            alias: {
                '@': path.resolve(__dirname, 'src/'),
                '@assets': path.resolve(__dirname, 'src/assets')
            }
        },
        // 构建优化配置
        optimization: {
            splitChunks: {
                chunks: 'all',
                cacheGroups: {
                    vendors: {
                        name: 'chunk-vendors',
                        test: /[\\/]node_modules[\\/]/,
                        priority: 10,
                        chunks: 'initial'
                    },
                    common: {
                        name: 'chunk-common',
                        minChunks: 2,
                        priority: 5,
                        chunks: 'initial',
                        reuseExistingChunk: true
                    }
                }
            }
        }
    },
    devServer: {
        // 主端口（HTTP）
        port: 8080,
        host: '0.0.0.0',
        open: true,
        // 启动HTTPS子服务（监听8443端口）
        setupMiddlewares: (middlewares, devServer) => {
            if (!devServer) {
                throw new Error('webpack-dev-server is not defined');
            }
            // 加载HTTPS证书
            const httpsOptions = {
                key: fs.readFileSync(path.resolve(__dirname, './cert.key')),
                cert: fs.readFileSync(path.resolve(__dirname, './cert.crt')),
            };
            // 启动HTTPS服务器，监听8443端口
            require('https').createServer(httpsOptions, devServer.app).listen(8443, '0.0.0.0', () => {
                console.log('HTTPS 服务启动: https://localhost:8443');
            });
            console.log('HTTP 服务启动: http://localhost:8080');
            return middlewares;
        }
    },
    // PWA配置
    pwa: {
        name: 'VoaTalk',
        short_name: 'VoaTalk',
        appleMobileWebAppCapable: 'yes',
        appleMobileWebAppStatusBarStyle: 'black',
        // 补充关键全局字段（影响移动端适配）
        themeColor: '#ffffff', // 主题色（适配浏览器地址栏/状态栏）
        backgroundColor: '#ffffff', // 应用启动时的背景色
        manifestOptions: {
            display: 'standalone',
            // 补充Manifest必要字段
            background_color: '#ffffff',
            theme_color: '#ffffff',
            start_url: '/', // 启动路径（确保可访问）
            icons: [
                // 必须包含192x192和512x512（PWA强制要求）
                {
                    src: '/logo-236-260.png', // 去掉./public，直接写根路径
                    sizes: '236x260',
                    type: 'image/png'
                },
                {
                    src: '/logo-248-280.png',
                    sizes: '248x280',
                    type: 'image/png'
                },
                // 保留原图标（可选，用于适配小众设备）
                {
                    src: '/logo-97-101.png',
                    sizes: '97x101',
                    type: 'image/png'
                },
                {
                    src: '/logo-206-216.png',
                    sizes: '206x216',
                    type: 'image/png'
                }
            ]
        },
        workboxPluginMode: 'InjectManifest',
        workboxOptions: {
            // 配置自定义Service Worker文件路径（InjectManifest模式必填）
            swSrc: './src/service-worker.js', // 需在src下创建该文件（空文件也可）
            swDest: 'service-worker.js' // 打包后输出的文件名
        }
    }
});
