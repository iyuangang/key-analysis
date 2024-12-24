// 获取当前环境
const ENV = import.meta.env.MODE || 'development'

// 环境配置
const config = {
  development: {
    debug: true,
    api: {
      baseURL: '/api'
    }
  },
  production: {
    debug: false,
    api: {
      baseURL: 'https://your-production-domain.com'
    }
  }
}

// 获取当前环境的配置
export const currentConfig = config[ENV as keyof typeof config] 
