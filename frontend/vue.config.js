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
        }
    },
    devServer: {
        https: {
            key: fs.readFileSync(path.resolve(__dirname, './cert.key')),
            cert: fs.readFileSync(path.resolve(__dirname, './cert.crt')),
        },
        port: 8080,
        host: '0.0.0.0', // 允许外部访问（如同一局域网的手机）
        open: true
    }
});
