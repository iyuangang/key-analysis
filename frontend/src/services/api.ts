import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api'
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    console.log('Request:', config)
    return config
  },
  error => {
    console.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    console.log('Response:', response)
    return response
  },
  error => {
    console.error('Response Error:', error)
    return Promise.reject(error)
  }
)

export const getRecentKeys = (dateRange: { start: number; end: number } | null = null) => {
  const params = dateRange ? { start: dateRange.start, end: dateRange.end } : {}
  return api.get('/keys/recent', { params }).then(res => res.data)
}

export const getHighScoreKeys = (dateRange: { start: number; end: number } | null = null) => {
  const params = dateRange ? { start: dateRange.start, end: dateRange.end } : {}
  return api.get('/keys/high-score', { params }).then(res => res.data)
}

export const getStatistics = (dateRange: { start: number; end: number } | null = null) => {
  const params = dateRange ? { start: dateRange.start, end: dateRange.end } : {}
  return api.get('/statistics', { params }).then(res => res.data)
} 
