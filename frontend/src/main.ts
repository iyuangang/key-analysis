import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

// 全局错误处理
app.config.errorHandler = (err, instance, info) => {
  console.error('Vue Error:', err)
  console.error('Component:', instance)
  console.error('Error Info:', info)
}

// 全局警告处理
app.config.warnHandler = (msg, instance, trace) => {
  console.warn('Vue Warning:', msg)
  console.warn('Component:', instance)
  console.warn('Trace:', trace)
}

app.mount('#app') 
