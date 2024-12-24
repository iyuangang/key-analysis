import { api } from './api'
import { debug } from '../utils/debug'

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
}

export interface User {
  username: string
  email?: string
  full_name?: string
}

export const auth = {
  async register(data: RegisterData) {
    const response = await api.post('/auth/register', data)
    return response.data
  },

  async login(credentials: LoginCredentials) {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    const response = await api.post('/token', formData)
    debug.log('Login response:', response)

    if (!response || !response.access_token) {
      throw new Error('Invalid response from server')
    }

    const { access_token } = response

    // 保存 token
    localStorage.setItem('token', access_token)
    localStorage.setItem('isAuthenticated', 'true')

    return access_token
  },

  async logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('isAuthenticated')
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get('/users/me')
    return response.data
  },

  getToken() {
    return localStorage.getItem('token')
  },

  isAuthenticated() {
    return localStorage.getItem('isAuthenticated') === 'true'
  }
} 
