import { ref } from 'vue'
import type { User } from '../types/user'
import { auth } from '../services/auth'

export function useAuth() {
  const currentUser = ref<User | null>(null)
  const isAuthenticated = ref(false)

  const login = async (credentials: { username: string; password: string }) => {
    try {
      const token = await auth.login(credentials)
      if (!token) {
        throw new Error('登录失败：未获取到访问令牌')
      }
      isAuthenticated.value = true
      return token
    } catch (error) {
      if (error instanceof Error) {
        throw error
      }
      throw new Error('登录失败，请检查用户名和密码')
    }
  }

  const logout = async () => {
    try {
      await auth.logout()
      currentUser.value = null
      isAuthenticated.value = false
    } catch (error) {
      if (error instanceof Error) {
        throw error
      }
      throw new Error('登出失败')
    }
  }

  const getCurrentUser = async () => {
    try {
      if (!currentUser.value) {
        currentUser.value = await auth.getCurrentUser()
      }
      return currentUser.value
    } catch (error) {
      if (error instanceof Error) {
        throw error
      }
      throw new Error('获取用户信息失败')
    }
  }

  return {
    currentUser,
    isAuthenticated,
    login,
    logout,
    getCurrentUser
  }
} 
