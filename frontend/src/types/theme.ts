export type ThemeMode = 'light' | 'dark' | 'system'

export interface ThemeVariables {
  // 背景色
  'bg-primary': string
  'bg-secondary': string
  'hover-bg': string

  // 文字颜色
  'text-primary': string
  'text-secondary': string

  // 边框
  'border': string

  // 强调色
  'accent': string
  'accent-dark': string
  'accent-transparent': string

  // 功能色
  'danger': string

  // 效果
  'shadow-sm': string
  'shadow-lg': string
  'blur-effect': string
  'scrollbar': string
  'scrollbar-hover': string

  // 圆角
  'radius-sm': string
  'radius-md': string
  'radius-lg': string

  // 字体大小
  'font-xs': string
  'font-sm': string
  'font-md': string
  'font-lg': string
  'font-xl': string
} 
