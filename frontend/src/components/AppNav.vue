<script setup lang="ts">
import { h, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NMenu, NIcon } from 'naive-ui'
import { auth } from '../services/auth'

const router = useRouter()
const route = useRoute()

const activeKey = computed(() => route.name?.toString())

const renderIcon = (iconName: string) => {
  return () => h(NIcon, null, { default: () => h('i', { class: iconName }) })
}

const isAuthenticated = computed(() => auth.isAuthenticated())

const menuOptions = computed(() => {
  const baseOptions = [
    {
      label: '仪表盘',
      key: 'dashboard',
      icon: renderIcon('i-ion-dashboard-outline')
    },
    {
      label: '关于',
      key: 'about',
      icon: renderIcon('i-ion-information-circle-outline')
    }
  ]

  if (isAuthenticated.value) {
    baseOptions.push(
      {
        label: '个人中心',
        key: 'user',
        icon: renderIcon('i-ion-person-outline')
      },
      {
        label: '退出登录',
        key: 'logout',
        icon: renderIcon('i-ion-log-out-outline')
      }
    )
  } else {
    baseOptions.push({
      label: '登录',
      key: 'login',
      icon: renderIcon('i-ion-log-in-outline')
    })
  }

  return baseOptions
})

const handleMenuClick = (key: string) => {
  if (key === 'logout') {
    auth.logout()
    router.push('/login')
  } else {
    router.push({ name: key })
  }
}
</script>

<template>
  <NMenu :value="activeKey" mode="horizontal" :options="menuOptions" @update:value="handleMenuClick" />
</template>

<style scoped>
:deep(.n-menu.n-menu--horizontal) {
  justify-content: center;
  padding: 0 24px;
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}
</style>
