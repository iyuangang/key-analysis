<template>
  <div class="dashboard-layout">
    <n-layout has-sider>
      <n-layout-sider v-if="!isMobile" bordered collapse-mode="width" :collapsed-width="64" :width="240"
        :collapsed="collapsed" show-trigger @collapse="collapsed = true" @expand="collapsed = false">
        <n-menu :collapsed="collapsed" :collapsed-width="64" :collapsed-icon-size="22" :options="menuOptions" />
      </n-layout-sider>
      <n-layout>
        <n-layout-header bordered class="header">
          <div class="header-content">
            <div class="header-left">
              <n-button v-if="isMobile" quaternary circle @click="showDrawer = true">
                <template #icon>
                  <n-icon><menu-outlined /></n-icon>
                </template>
              </n-button>
              <div class="header-title">密钥分析系统</div>
            </div>
            <div class="header-actions">
              <n-dropdown :options="userMenuOptions" @select="handleUserAction">
                <n-button text>
                  {{ currentUser?.username || '用户' }}
                  <template #icon>
                    <n-icon><user-outlined /></n-icon>
                  </template>
                </n-button>
              </n-dropdown>
            </div>
          </div>
        </n-layout-header>
        <n-layout-content class="main-content">
          <slot></slot>
        </n-layout-content>
      </n-layout>
    </n-layout>

    <!-- 移动端抽屉菜单 -->
    <n-drawer v-model:show="showDrawer" :width="280" placement="left">
      <n-drawer-content title="菜单" closable>
        <n-menu :options="menuOptions" :indent="18" @update:value="handleMenuSelect" />
      </n-drawer-content>
    </n-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeMount, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  UserOutlined,
  DashboardOutlined,
  MenuOutlined
} from '@vicons/antd'
import {
  AppstoreOutlined as ChartOutlined
} from '@vicons/antd'
import {
  NLayout,
  NLayoutSider,
  NLayoutHeader,
  NLayoutContent,
  NMenu,
  NButton,
  NDropdown,
  NIcon,
  NDrawer,
  NDrawerContent
} from 'naive-ui'
import { auth } from '../services/auth'
import type { User } from '../services/auth'
import { h } from 'vue'
import { debug } from '../utils/debug'

const router = useRouter()
const collapsed = ref(false)
const currentUser = ref<User | null>(null)
const isMobile = ref(false)
const showDrawer = ref(false)

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

function renderIcon(icon: any) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menuOptions = [
  {
    label: '数据分析',
    key: 'dashboard',
    icon: renderIcon(DashboardOutlined)
  }
]

const userMenuOptions = [
  {
    label: '退出登录',
    key: 'logout'
  }
]

const handleUserAction = async (key: string) => {
  if (key === 'logout') {
    await auth.logout()
    debug.log('Logout successful, redirecting to login')
    await router.replace('/login')
  }
}

const handleMenuSelect = (key: string) => {
  showDrawer.value = false
  router.push(`/${key}`)
}

onMounted(async () => {
  try {
    currentUser.value = await auth.getCurrentUser()
  } catch (error) {
    router.push('/login')
  }
})
</script>

<style scoped>
.dashboard-layout {
  height: 100vh;
  background-color: var(--apple-bg-primary);
}

.header {
  backdrop-filter: var(--apple-blur-effect);
  background-color: var(--apple-card-bg);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: var(--apple-transition);
  border-bottom: 1px solid var(--apple-border-color);
}

.header-content {
  padding: 0 var(--apple-spacing-lg);
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--apple-spacing-md);
}

.header-title {
  font-size: var(--apple-font-lg);
  font-weight: 600;
  background: var(--apple-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--apple-spacing-md);
}

.main-content {
  padding: var(--apple-spacing-lg);
  min-height: calc(100vh - 48px);
}

:deep(.n-button) {
  font-weight: 500;
  letter-spacing: -0.2px;
}

:deep(.n-layout-sider) {
  background-color: var(--apple-card-bg);
  backdrop-filter: var(--apple-blur-effect);
  border-right: 1px solid var(--apple-border-color);
}

:deep(.n-menu-item) {
  font-weight: 500;
  letter-spacing: -0.2px;
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
  border-bottom: 1px solid var(--apple-border-color);
}

:deep(.n-drawer-header__title) {
  font-size: var(--apple-font-lg);
  font-weight: 600;
  letter-spacing: -0.5px;
  color: var(--apple-text-primary);
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
