<template>
  <div class="dashboard-layout">
    <n-layout has-sider>
      <n-layout-sider
        v-if="!isMobile"
        bordered
        collapse-mode="width"
        :collapsed-width="64"
        :width="240"
        :collapsed="collapsed"
        show-trigger
        @collapse="collapsed = true"
        @expand="collapsed = false"
      >
        <n-menu
          :collapsed="collapsed"
          :collapsed-width="64"
          :collapsed-icon-size="22"
          :options="menuOptions"
        />
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
        <n-menu
          :options="menuOptions"
          :indent="18"
          @update:value="handleMenuSelect"
        />
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
  background-color: #f5f5f7;
}

.header {
  backdrop-filter: saturate(180%) blur(20px);
  background-color: rgba(255, 255, 255, 0.72);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: background-color 0.3s;
}

.header-content {
  padding: 0 24px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-title {
  font-size: 17px;
  font-weight: 600;
  background: linear-gradient(135deg, #1a1a1a 0%, #434343 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.main-content {
  padding: 24px;
  min-height: calc(100vh - 48px);
}

:deep(.n-button) {
  font-weight: 500;
}

:deep(.n-layout-sider) {
  background-color: rgba(255, 255, 255, 0.72);
  backdrop-filter: saturate(180%) blur(20px);
  border-right: 1px solid rgba(0, 0, 0, 0.1);
}

:deep(.n-menu-item) {
  font-weight: 500;
  letter-spacing: -0.2px;
}

:deep(.n-drawer) {
  background-color: rgba(255, 255, 255, 0.72);
  backdrop-filter: saturate(180%) blur(20px);
}

@media (max-width: 768px) {
  .header-content {
    padding: 0 16px;
  }

  .main-content {
    padding: 16px;
  }

  :deep(.n-drawer-content) {
    padding: 16px;
  }

  :deep(.n-drawer-header) {
    padding: 16px;
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
