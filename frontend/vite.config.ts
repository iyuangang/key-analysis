import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import UnoCSS from 'unocss/vite'
import { presetIcons } from 'unocss/preset-icons'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [
    vue(),
    UnoCSS({
      presets: [
        presetIcons({
          scale: 1.2,
          cdn: 'https://esm.sh/'
        })
      ]
    })
  ],
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  },
  define: {
    __DEV__: mode === 'development'
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})) 
