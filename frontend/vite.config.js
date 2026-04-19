import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import fs from 'fs'
import https from 'https'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@assets': path.resolve(__dirname, './src/assets')
    }
  },
  server: {
    port: 8080,
    host: '0.0.0.0',
    open: true,
    https: false
  },
  configureServer(server) {
    server.httpServer.on('listening', () => {
      // 加载HTTPS证书
      const httpsOptions = {
        key: fs.readFileSync(path.resolve(__dirname, './cert.key')),
        cert: fs.readFileSync(path.resolve(__dirname, './cert.crt'))
      }
      // 启动HTTPS服务器，监听8443端口
      https.createServer(httpsOptions, server.middlewares).listen(8443, '0.0.0.0', () => {
        console.log('HTTPS 服务启动: https://localhost:8443')
      })
      console.log('HTTP 服务启动: http://localhost:8080')
    })
  },
  build: {
    chunkSizeWarningLimit: 1500
  }
})
