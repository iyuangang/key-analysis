import { ref, onMounted, onUnmounted } from 'vue'

type Theme = 'light' | 'dark' | 'system'

const THEME_KEY = 'apple-theme-preference'

export function useTheme() {
  // 从本地存储读取主题设置
  const savedTheme = localStorage.getItem(THEME_KEY)
  const theme = ref<Theme>(savedTheme as Theme || 'system')

  // 检测系统主题
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  const systemDark = ref(mediaQuery.matches)

  // 应用主题到文档
  const applyTheme = (isDark: boolean) => {
    console.log('Applying theme:', isDark ? 'dark' : 'light')

    // 设置主题属性
    document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light')

    // 更新CSS变量
    const root = document.documentElement
    if (isDark) {
      root.style.setProperty('--apple-bg-primary', 'var(--apple-bg-primary-dark)')
      root.style.setProperty('--apple-bg-secondary', 'var(--apple-bg-secondary-dark)')
      root.style.setProperty('--apple-text-primary', 'var(--apple-text-primary-dark)')
      root.style.setProperty('--apple-text-secondary', 'var(--apple-text-secondary-dark)')
      root.style.setProperty('--apple-border', 'var(--apple-border-dark)')
      root.style.setProperty('--apple-card-bg', 'var(--apple-card-bg-dark)')
      root.style.setProperty('--apple-hover-bg', 'var(--apple-hover-bg-dark)')
      root.style.setProperty('--apple-sidebar-bg', 'var(--apple-sidebar-bg-dark)')
      root.style.setProperty('--apple-shadow', 'var(--apple-shadow-dark-md)')
    } else {
      root.style.setProperty('--apple-bg-primary', 'var(--apple-bg-primary-light)')
      root.style.setProperty('--apple-bg-secondary', 'var(--apple-bg-secondary-light)')
      root.style.setProperty('--apple-text-primary', 'var(--apple-text-primary-light)')
      root.style.setProperty('--apple-text-secondary', 'var(--apple-text-secondary-light)')
      root.style.setProperty('--apple-border', 'var(--apple-border-light)')
      root.style.setProperty('--apple-card-bg', 'var(--apple-card-bg-light)')
      root.style.setProperty('--apple-hover-bg', 'var(--apple-hover-bg-light)')
      root.style.setProperty('--apple-sidebar-bg', 'var(--apple-sidebar-bg-light)')
      root.style.setProperty('--apple-shadow', 'var(--apple-shadow-md)')
    }
  }

  // 处理系统主题变化
  const handleSystemThemeChange = (e: MediaQueryListEvent) => {
    console.log('System theme changed:', e.matches ? 'dark' : 'light')
    systemDark.value = e.matches
    if (theme.value === 'system') {
      applyTheme(e.matches)
    }
  }

  // 更新主题
  const updateTheme = (newTheme: Theme) => {
    console.log('Updating theme to:', newTheme)
    theme.value = newTheme
    localStorage.setItem(THEME_KEY, newTheme)

    if (newTheme === 'system') {
      applyTheme(systemDark.value)
    } else {
      applyTheme(newTheme === 'dark')
    }
  }

  // 切换主题
  const toggleTheme = () => {
    console.log('Toggling theme from:', theme.value)
    if (theme.value === 'system') {
      updateTheme(systemDark.value ? 'light' : 'dark')
    } else {
      updateTheme(theme.value === 'light' ? 'dark' : 'light')
    }
  }

  // 初始化
  onMounted(() => {
    console.log('Theme system initializing')
    console.log('Current theme:', theme.value)
    console.log('System dark mode:', systemDark.value)

    // 添加系统主题变化监听
    mediaQuery.addEventListener('change', handleSystemThemeChange)

    // 应用初始主题
    if (theme.value === 'system') {
      applyTheme(systemDark.value)
    } else {
      applyTheme(theme.value === 'dark')
    }
  })

  // 清理
  onUnmounted(() => {
    mediaQuery.removeEventListener('change', handleSystemThemeChange)
  })

  return {
    theme,
    systemDark,
    updateTheme,
    toggleTheme
  }
}

