<script setup lang="ts">
import { h } from 'vue'
import { NIcon } from 'naive-ui'

defineProps<{
  collapsed?: boolean
}>()
</script>

<template>
  <div class="app-logo" :class="{ collapsed }">
    <NIcon size="32" :color="'var(--apple-accent)'">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path fill="currentColor"
          d="M7 14c-1.1 0-2-.9-2-2s.9-2 2-2s2 .9 2 2s-.9 2-2 2m5-14l-6 6h4v3l6-6h-4z M11.7 17.7l-1.4-1.4L2 24.6l1.4 1.4l8.3-8.3m9.3-11.7l-6 6h4v3l6-6h-4z" />
      </svg>
    </NIcon>
    <span v-if="!collapsed" class="logo-text">密钥分析系统</span>
  </div>
</template>

<style scoped>
.app-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 12px;
  height: 64px;
  transition: all 0.2s ease;
  border-bottom: 1px solid var(--apple-border);
  background: linear-gradient(to right, var(--apple-accent), var(--apple-accent-dark));
  -webkit-background-clip: text;
  color: transparent;
}

.app-logo.collapsed {
  justify-content: center;
  padding: 0;
}

.logo-text {
  font-size: var(--apple-font-lg);
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  background: linear-gradient(to right, var(--apple-accent), var(--apple-accent-dark));
  -webkit-background-clip: text;
  color: transparent;
}
</style>
