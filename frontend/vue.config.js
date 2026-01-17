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
    }
});
