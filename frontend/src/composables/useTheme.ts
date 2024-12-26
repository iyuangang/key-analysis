import { ref, onMounted, watch } from 'vue'
import type { ThemeMode, ThemeVariables } from '../types/theme'

const THEME_KEY = 'theme'
const SYSTEM_DARK_MEDIA = '(prefers-color-scheme: dark)'

export function useTheme() {
  const theme = ref<ThemeMode>(localStorage.getItem(THEME_KEY) as ThemeMode || 'system')
  const systemDark = ref(false)

  // 监听系统主题变化
  const setupSystemThemeListener = () => {
    const mediaQuery = window.matchMedia(SYSTEM_DARK_MEDIA)
    systemDark.value = mediaQuery.matches

    // 使用新的 API 监听变化
    const handler = (e: MediaQueryListEvent) => {
      systemDark.value = e.matches
      if (theme.value === 'system') {
        applyTheme(systemDark.value ? 'dark' : 'light')
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

      // 更新 CSS 变量
      const suffix = mode === 'dark' ? '-dark' : '-light'
      root.style.setProperty('--apple-bg-primary', `var(--apple-bg-primary${suffix})`)
      root.style.setProperty('--apple-bg-secondary', `var(--apple-bg-secondary${suffix})`)
      root.style.setProperty('--apple-text-primary', `var(--apple-text-primary${suffix})`)
      root.style.setProperty('--apple-text-secondary', `var(--apple-text-secondary${suffix})`)
      root.style.setProperty('--apple-border', `var(--apple-border${suffix})`)
      root.style.setProperty('--apple-card-bg', `var(--apple-card-bg${suffix})`)
      root.style.setProperty('--apple-hover-bg', `var(--apple-hover-bg${suffix})`)
      root.style.setProperty('--apple-sidebar-bg', `var(--apple-sidebar-bg${suffix})`)
      root.style.setProperty('--apple-shadow', `var(--apple-shadow${mode === 'dark' ? '-dark' : ''}-md)`)
    })
  }

  // 切换主题
  const toggleTheme = () => {
    const currentMode = getCurrentMode()
    const newMode: ThemeMode = currentMode === 'dark' ? 'light' : 'dark'
    theme.value = newMode
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
    return cleanup
  })

  return {
    theme,
    systemDark,
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

