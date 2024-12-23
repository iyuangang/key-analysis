export const isDev = process.env.NODE_ENV === 'development'

export const config = {
  apiBaseUrl: isDev ? 'http://localhost:8000/api' : '/api',
  debug: isDev,
  logLevel: isDev ? 'debug' : 'error'
} 
