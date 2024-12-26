<script setup lang="ts">
import { ref, h } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NMenu, NIcon, NButton } from 'naive-ui'
import type { MenuOption, MenuGroupOption, MenuDividerOption } from 'naive-ui'
import AppLogo from './AppLogo.vue'
import ThemeToggle from './ThemeToggle.vue'
import { useAuth } from '../composables/useAuth'

const router = useRouter()
const route = useRoute()
const auth = useAuth()
const collapsed = ref(false)

type MenuItem = MenuOption | MenuGroupOption | MenuDividerOption

const menuOptions: MenuItem[] = [
  {
    label: '仪表盘',
    key: 'dashboard',
    icon: renderIcon('i-carbon-dashboard')
  },
  {
    label: '密钥分析',
    key: 'analysis',
    icon: renderIcon('i-carbon-password')
  },
  {
    label: '统计数据',
    key: 'statistics',
    icon: renderIcon('i-carbon-chart-line')
  },
  {
    label: '个人中心',
    key: 'user',
    icon: renderIcon('i-carbon-user-profile')
  }
]

function renderIcon(icon: string) {
  return () => h(NIcon, null, { default: () => h('i', { class: icon }) })
}

const handleMenuClick = (key: string) => {
  router.push(`/${key}`)
}

const toggleCollapse = () => {
  collapsed.value = !collapsed.value
}

const handleLogout = async () => {
  try {
    await auth.logout()
    router.push('/login')
  } catch (error) {
    console.error('Logout failed:', error)
  }
}
</script>

<template>
  <div class="sidebar" :class="{ collapsed }">
    <div class="sidebar-header">
      <AppLogo :collapsed="collapsed" />
      <NButton quaternary circle class="collapse-button" @click="toggleCollapse">
        <template #icon>
          <NIcon>
            <i :class="collapsed ? 'i-carbon-chevron-right' : 'i-carbon-chevron-left'" />
          </NIcon>
        </template>
      </NButton>
    </div>

    <div class="menu-wrapper">
      <NMenu :value="route.path.split('/')[1] || 'dashboard'" :collapsed="collapsed" :collapsed-width="64"
        :collapsed-icon-size="22" :options="menuOptions" @update:value="handleMenuClick" />
    </div>

    <div class="sidebar-footer">
      <div class="footer-actions">
        <ThemeToggle />
        <NButton quaternary circle class="logout-button" @click="handleLogout">
          <template #icon>
            <NIcon>
              <i class="i-carbon-logout" />
            </NIcon>
          </template>
        </NButton>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  height: 100vh;
  width: 240px;
  background-color: var(--apple-bg-secondary);
  border-right: 1px solid var(--apple-border);
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  position: relative;
  backdrop-filter: var(--apple-blur-effect);
}

.sidebar.collapsed {
  width: 64px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-right: 12px;
  border-bottom: 1px solid var(--apple-border);
}

.collapse-button {
  width: 32px !important;
  height: 32px !important;
  color: var(--apple-text-primary) !important;
  transition: all 0.3s ease !important;
}

.collapse-button:hover {
  color: var(--apple-accent) !important;
  background-color: var(--apple-hover-bg) !important;
}

.menu-wrapper {
  flex: 1;
  padding: 12px 0;
  overflow-y: auto;
}

.menu-wrapper :deep(.n-menu) {
  background-color: transparent;
}

.menu-wrapper :deep(.n-menu-item) {
  height: 40px;
  margin: 4px 8px;
  padding: 0 12px;
  border-radius: var(--apple-radius-md);
}

.menu-wrapper :deep(.n-menu-item-content) {
  color: var(--apple-text-primary);
  font-weight: 500;
}

.menu-wrapper :deep(.n-menu-item-content--selected) {
  color: var(--apple-accent) !important;
  background-color: var(--apple-accent-transparent) !important;
  font-weight: 600;
}

.menu-wrapper :deep(.n-menu-item-content:hover) {
  color: var(--apple-accent);
}

.menu-wrapper :deep(.n-menu-item-content__icon) {
  font-size: 18px;
  color: inherit;
}

.sidebar-footer {
  border-top: 1px solid var(--apple-border);
  padding: 12px;
}

.footer-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.logout-button {
  width: 36px !important;
  height: 36px !important;
  color: var(--apple-text-primary) !important;
  transition: all 0.3s ease !important;
}

.logout-button:hover {
  color: var(--apple-danger) !important;
  background-color: var(--apple-hover-bg) !important;
}

/* 自定义滚动条样式 */
.menu-wrapper {
  scrollbar-width: thin;
  scrollbar-color: var(--apple-scrollbar) transparent;
}

.menu-wrapper::-webkit-scrollbar {
  width: 6px;
}

.menu-wrapper::-webkit-scrollbar-track {
  background: transparent;
}

.menu-wrapper::-webkit-scrollbar-thumb {
  background-color: var(--apple-scrollbar);
  border-radius: 3px;
}

.menu-wrapper::-webkit-scrollbar-thumb:hover {
  background-color: var(--apple-scrollbar-hover);
}
</style>
