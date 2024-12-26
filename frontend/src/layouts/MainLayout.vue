<script setup lang="ts">
import { h, ref, computed, onMounted, onBeforeMount, onUnmounted } from 'vue'
import { NLayout, NLayoutSider, NLayoutHeader, NLayoutContent, NMenu, NIcon, NAvatar, NDropdown, NSpace, NDrawer, NDrawerContent, NButton } from 'naive-ui'
import { useRouter, useRoute } from 'vue-router'
import { auth } from '../services/auth'
import type { User } from '../types/user'
import AppLogo from '../components/AppLogo.vue'
import { useTheme } from '../composables/useTheme'

const router = useRouter()
const route = useRoute()
const collapsed = ref(false)
const currentUser = ref<User | null>(null)
const isMobile = ref(false)
const showDrawer = ref(false)
const { theme, systemDark, toggleTheme } = useTheme()

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
  if (isMobile.value) {
    collapsed.value = true
  }
}

onBeforeMount(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

const activeKey = computed(() => route.name?.toString())

onMounted(async () => {
  try {
    currentUser.value = await auth.getCurrentUser()
  } catch (error) {
    console.error('Failed to fetch user:', error)
  }
})

const renderIcon = (iconName: string) => {
  return () => h(NIcon, null, { default: () => h('i', { class: iconName }) })
}

const menuOptions = [
  {
    label: '仪表盘',
    key: 'dashboard',
    icon: renderIcon('i-ion-dashboard-outline')
  },
  {
    label: '密钥分析',
    key: 'analysis',
    icon: renderIcon('i-ion-key-outline')
  },
  {
    label: '统计报告',
    key: 'statistics',
    icon: renderIcon('i-ion-stats-chart-outline')
  },
  {
    label: '个人中心',
    key: 'user',
    icon: renderIcon('i-ion-person-outline')
  },
  {
    label: '关于系统',
    key: 'about',
    icon: renderIcon('i-ion-information-circle-outline')
  }
]

const userDropdownOptions = [
  {
    label: '个人中心',
    key: 'profile',
    icon: renderIcon('i-ion-person-outline')
  },
  {
    label: '系统设置',
    key: 'settings',
    icon: renderIcon('i-ion-settings-outline')
  },
  {
    type: 'divider',
    key: 'd1'
  },
  {
    label: '退出登录',
    key: 'logout',
    icon: renderIcon('i-ion-log-out-outline')
  }
]

const handleMenuClick = (key: string) => {
  router.push({ name: key })
  if (isMobile.value) {
    showDrawer.value = false
  }
}

const handleUserAction = (key: string) => {
  if (key === 'logout') {
    auth.logout()
    router.push('/login')
  } else if (key === 'profile') {
    router.push({ name: 'user' })
  }
}

const handleThemeToggle = () => {
  console.log('Current theme:', theme.value)
  console.log('System dark:', systemDark.value)
  toggleTheme()
  console.log('New theme:', theme.value)
}
</script>

<template>
  <div class="main-layout">
    <NLayout has-sider>
      <NLayoutSider v-if="!isMobile" bordered collapse-mode="width" :collapsed="collapsed" :collapsed-width="64"
        :width="240" :native-scrollbar="false" class="main-sider" show-trigger @collapse="collapsed = true"
        @expand="collapsed = false">
        <AppLogo :collapsed="collapsed" />
        <NMenu :value="activeKey" :collapsed="collapsed" :collapsed-width="64" :collapsed-icon-size="22"
          :options="menuOptions" :inverted="true" @update:value="handleMenuClick" />
      </NLayoutSider>

      <NLayout>
        <NLayoutHeader bordered class="main-header">
          <div class="header-content">
            <div class="header-left">
              <NButton v-if="isMobile" quaternary circle @click="showDrawer = true">
                <template #icon>
                  <NIcon>
                    <i class="i-ion-menu-outline" />
                  </NIcon>
                </template>
              </NButton>
              <h2>{{ route.meta.title || '密钥分析系统' }}</h2>
            </div>
            <div class="header-right">
              <NButton quaternary circle class="theme-button" @click="handleThemeToggle">
                <template #icon>
                  <NIcon>
                    <i
                      :class="theme === 'dark' || (theme === 'system' && systemDark) ? 'i-ion-sunny-outline' : 'i-ion-moon-outline'" />
                  </NIcon>
                </template>
              </NButton>
              <NDropdown :options="userDropdownOptions" @select="handleUserAction" trigger="click">
                <NSpace align="center" class="user-info">
                  <NAvatar round size="small">
                    <i class="i-ion-person" />
                  </NAvatar>
                  <span class="username">{{ currentUser?.username }}</span>
                </NSpace>
              </NDropdown>
            </div>
          </div>
        </NLayoutHeader>

        <NLayoutContent class="main-content">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </NLayoutContent>
      </NLayout>
    </NLayout>

    <!-- 移动端抽屉菜单 -->
    <NDrawer v-model:show="showDrawer" :width="280" placement="left">
      <NDrawerContent title="菜单" closable>
        <AppLogo :collapsed="false" />
        <NMenu :options="menuOptions" :indent="18" @update:value="handleMenuClick" />
      </NDrawerContent>
    </NDrawer>
  </div>
</template>

<style scoped>
.main-layout {
  height: 100vh;
  background-color: var(--apple-bg-primary);
}

.main-sider {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--apple-sidebar-bg);
  backdrop-filter: var(--apple-blur-effect);
  border-right: 1px solid var(--apple-border);
}

.main-header {
  height: 48px;
  padding: 0;
  background-color: var(--apple-card-bg);
  backdrop-filter: var(--apple-blur-effect);
  border-bottom: 1px solid var(--apple-border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  height: 100%;
  padding: 0 var(--apple-spacing-lg);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--apple-spacing-md);
}

.header-left h2 {
  margin: 0;
  font-size: var(--apple-font-lg);
  font-weight: 600;
  letter-spacing: var(--apple-letter-spacing);
  color: var(--apple-text-primary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--apple-spacing-md);
}

.user-info {
  padding: var(--apple-spacing-xs) var(--apple-spacing-sm);
  border-radius: var(--apple-radius-md);
  transition: var(--apple-transition);
  cursor: pointer;
}

.user-info:hover {
  background-color: var(--apple-hover-bg);
}

.username {
  font-size: var(--apple-font-sm);
  font-weight: 500;
  color: var(--apple-text-primary);
}

.main-content {
  padding: var(--apple-spacing-lg);
  background-color: var(--apple-bg-primary);
  min-height: calc(100vh - 48px);
  overflow-y: auto;
}

:deep(.n-menu) {
  --n-item-height: 44px;
  --n-font-size: var(--apple-font-sm);
  font-weight: 500;
  background-color: transparent;
}

:deep(.n-menu-item) {
  color: var(--apple-text-primary) !important;
}

:deep(.n-menu-item:hover),
:deep(.n-menu-item--selected) {
  background-color: var(--apple-hover-bg) !important;
}

:deep(.n-button) {
  font-weight: 500;
  letter-spacing: var(--apple-letter-spacing);
}

:deep(.n-button:not(.n-button--disabled):hover) {
  background-color: var(--apple-hover-bg);
}

:deep(.n-drawer) {
  background-color: var(--apple-card-bg);
  backdrop-filter: var(--apple-blur-effect);
}

:deep(.n-drawer-content) {
  background-color: var(--apple-card-bg);
  backdrop-filter: var(--apple-blur-effect);
}

:deep(.n-drawer-header) {
  border-bottom: 1px solid var(--apple-border);
}

:deep(.n-drawer-header__title) {
  font-size: var(--apple-font-lg);
  font-weight: 600;
  letter-spacing: var(--apple-letter-spacing);
  color: var(--apple-text-primary);
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 var(--apple-spacing-md);
  }

  .main-content {
    padding: var(--apple-spacing-md);
  }

  :deep(.n-drawer-content) {
    padding: var(--apple-spacing-md);
  }

  :deep(.n-drawer-header) {
    padding: var(--apple-spacing-md);
  }

  :deep(.n-drawer-body) {
    padding: 0;
  }
}

/* 动画效果 */
:deep(.n-button:not(.n-button--disabled):active) {
  transform: scale(0.96);
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

.theme-icon {
  font-size: 20px;
  color: var(--apple-text-primary);
  transition: all 0.3s ease;
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

.theme-button:active .theme-icon {
  animation: rotate 0.5s ease;
}
</style>
