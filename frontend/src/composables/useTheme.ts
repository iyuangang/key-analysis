import { ref, onMounted, watch } from 'vue'
import type { ThemeMode, ThemeVariables } from '../types/theme'

const THEME_KEY = 'theme'
const SYSTEM_DARK_MEDIA = '(prefers-color-scheme: dark)'

// 预定义的主题变量映射
const themeVariables = {
  light: {
    'bg-primary': 'var(--apple-bg-primary-light)',
    'bg-secondary': 'var(--apple-bg-secondary-light)',
    'text-primary': 'var(--apple-text-primary-light)',
    'text-secondary': 'var(--apple-text-secondary-light)',
    'border': 'var(--apple-border-light)',
    'card-bg': 'var(--apple-card-bg-light)',
    'hover-bg': 'var(--apple-hover-bg-light)',
    'sidebar-bg': 'var(--apple-sidebar-bg-light)',
    'shadow': 'var(--apple-shadow-md)'
  },
  dark: {
    'bg-primary': 'var(--apple-bg-primary-dark)',
    'bg-secondary': 'var(--apple-bg-secondary-dark)',
    'text-primary': 'var(--apple-text-primary-dark)',
    'text-secondary': 'var(--apple-text-secondary-dark)',
    'border': 'var(--apple-border-dark)',
    'card-bg': 'var(--apple-card-bg-dark)',
    'hover-bg': 'var(--apple-hover-bg-dark)',
    'sidebar-bg': 'var(--apple-sidebar-bg-dark)',
    'shadow': 'var(--apple-shadow-dark-md)'
  }
}

export function useTheme() {
  const theme = ref<ThemeMode>(localStorage.getItem(THEME_KEY) as ThemeMode || 'system')
  const systemDark = ref(false)
  const isDark = ref(false)

  // 监听系统主题变化
  const setupSystemThemeListener = () => {
    const mediaQuery = window.matchMedia(SYSTEM_DARK_MEDIA)
    systemDark.value = mediaQuery.matches

    const handler = (e: MediaQueryListEvent) => {
      systemDark.value = e.matches
      if (theme.value === 'system') {
        isDark.value = e.matches
        applyTheme(e.matches ? 'dark' : 'light')
      }
    }

    mediaQuery.addEventListener('change', handler)
    return () => mediaQuery.removeEventListener('change', handler)
  }

  // 应用主题到 DOM
  const applyTheme = (mode: 'light' | 'dark') => {
    requestAnimationFrame(() => {
      const root = document.documentElement
      root.setAttribute('data-theme', mode)

      // 批量更新 CSS 变量
      const variables = themeVariables[mode]
      Object.entries(variables).forEach(([key, value]) => {
        root.style.setProperty(`--apple-${key}`, value)
      })

      // 更新暗色模式状态
      isDark.value = mode === 'dark'
    })
  }

  // 切换主题
  const toggleTheme = () => {
    const currentMode = getCurrentMode()
    const newMode: ThemeMode = currentMode === 'dark' ? 'light' : 'dark'
    theme.value = newMode
    isDark.value = newMode === 'dark'
    localStorage.setItem(THEME_KEY, newMode)
  }

  // 获取当前实际的主题模式
  const getCurrentMode = (): 'light' | 'dark' => {
    return theme.value === 'system'
      ? systemDark.value ? 'dark' : 'light'
      : theme.value
  }

  // 监听主题变化
  watch(
    () => [theme.value, systemDark.value],
    () => {
      const mode = getCurrentMode()
      applyTheme(mode)
    },
    { immediate: true }
  )

  // 初始化
  onMounted(() => {
    const cleanup = setupSystemThemeListener()
    isDark.value = getCurrentMode() === 'dark'
    return cleanup
  })

  return {
    theme,
    systemDark,
    isDark,
    toggleTheme,
    getCurrentMode
  }
}

// 开发环境下添加调试工具
if (import.meta.env.DEV) {
  const themeDebug = {
    getCurrentTheme: () => localStorage.getItem(THEME_KEY),
    setTheme: (mode: ThemeMode) => {
      localStorage.setItem(THEME_KEY, mode)
      window.location.reload()
    },
    clearTheme: () => {
      localStorage.removeItem(THEME_KEY)
      window.location.reload()
    }
  }

  // @ts-ignore
  window.__THEME_DEBUG__ = themeDebug
}

