import { defineConfig, presetAttributify, presetIcons, presetUno, presetWebFonts } from 'unocss'

export default defineConfig({
  presets: [
    presetUno(),
    presetAttributify(),
    presetIcons({
      scale: 1.2,
      extraProperties: {
        'display': 'inline-block',
        'vertical-align': 'middle',
      },
    }),
    presetWebFonts({
      fonts: {
        sans: 'Inter:400,500,600,700',
      },
    }),
  ],
  theme: {
    colors: {
      primary: 'var(--apple-text-primary)',
      secondary: 'var(--apple-text-secondary)',
      border: 'var(--apple-border)',
      hover: 'var(--apple-hover-bg)',
    },
  },
}) 
