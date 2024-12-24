import axios from 'axios'
import { currentConfig } from '../config'
import { debug } from '../utils/debug'
import router from '../router'

export const api = axios.create({
  baseURL: currentConfig.api.baseURL
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    debug.log('Request:', config)
    return config
  },
  error => {
    debug.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    debug.log('Response:', response)
    debug.log('Response data structure:', {
      hasData: !!response.data,
      dataType: typeof response.data,
      data: response.data
    })
    return response.data
  },
  error => {
    debug.error('API Error:', {
      status: error.response?.status,
      data: error.response?.data,
      config: error.config,
      stack: error.stack
    })

    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('isAuthenticated')
      window.location.href = '/login'
    } else if (error.response?.status === 500) {
      localStorage.removeItem('token')
      localStorage.removeItem('isAuthenticated')
      window.location.href = '/login'
    }

    if (error.response?.data?.detail) {
      return Promise.reject(new Error(error.response.data.detail))
    }

    return Promise.reject(error)
  }
)

export const getRecentKeys = (dateRange: { start: number; end: number } | null = null) => {
  const params = dateRange ? { start: dateRange.start, end: dateRange.end } : {}
  return api.get('/keys/recent', { params })
}

export const getHighScoreKeys = (dateRange: { start: number; end: number } | null = null) => {
  const params = dateRange ? { start: dateRange.start, end: dateRange.end } : {}
  return api.get('/keys/high-score', { params })
}

export const getStatistics = (dateRange: { start: number; end: number } | null = null) => {
  const params = dateRange ? { start: dateRange.start, end: dateRange.end } : {}
  return api.get('/statistics', { params })
} 
