<template>
  <div class="dashboard-layout">
    <n-layout has-sider>
      <n-layout-sider
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
        <n-layout-header bordered>
          <div class="header-content">
            <div class="header-title">密钥分析系统</div>
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
        <n-layout-content content-style="padding: 24px;">
          <slot></slot>
        </n-layout-content>
      </n-layout>
    </n-layout>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  UserOutlined,
  DashboardOutlined
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
  NIcon
} from 'naive-ui'
import { auth } from '../services/auth'
import type { User } from '../services/auth'
import { h } from 'vue'
import { debug } from '../utils/debug'

const router = useRouter()
const collapsed = ref(false)
const currentUser = ref<User | null>(null)

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
}

.header-content {
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-title {
  font-size: 18px;
  font-weight: bold;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}
</style> 
