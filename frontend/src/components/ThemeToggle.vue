<script setup lang="ts">
import { NButton, NIcon } from 'naive-ui'
import { useTheme } from '../composables/useTheme'

const { theme, systemDark, toggleTheme } = useTheme()
</script>

<template>
  <div class="theme-switch">
    <NButton quaternary circle class="theme-button" @click="toggleTheme">
      <template #icon>
        <NIcon>
          <i :class="theme === 'dark' || (theme === 'system' && systemDark) ? 'i-carbon-sun' : 'i-carbon-moon'" />
        </NIcon>
      </template>
    </NButton>
    <div class="theme-tooltip">
      {{ theme === 'dark' || (theme === 'system' && systemDark) ? '切换到亮色模式' : '切换到暗色模式' }}
    </div>
  </div>
</template>

<style scoped>
.theme-switch {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.theme-button {
  width: 36px !important;
  height: 36px !important;
  font-size: 20px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  border: 1px solid var(--apple-border) !important;
  background-color: var(--apple-bg-secondary) !important;
  color: var(--apple-text-primary) !important;
  transition: all 0.3s ease !important;
}

.theme-button:hover {
  background-color: var(--apple-hover-bg) !important;
  transform: scale(1.05);
}

.theme-button:active {
  transform: scale(0.95);
}

.theme-tooltip {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%) translateY(8px);
  padding: 6px 12px;
  background-color: var(--apple-bg-secondary);
  border: 1px solid var(--apple-border);
  border-radius: var(--apple-radius-md);
  font-size: var(--apple-font-xs);
  color: var(--apple-text-primary);
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s ease;
  box-shadow: var(--apple-shadow-sm);
  backdrop-filter: var(--apple-blur-effect);
  z-index: 2;
}

.theme-switch:hover .theme-tooltip {
  opacity: 1;
  visibility: visible;
  transform: translateX(-50%) translateY(4px);
}

/* 主题切换动画 */
@keyframes rotate {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

.theme-button:active i {
  animation: rotate 0.5s ease;
}
</style>
