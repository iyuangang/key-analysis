<template>
  <div class="main-layout" :class="{ 'sidebar-open': isSidebarOpen }">
    <AppSidebar class="sidebar" />
    <div class="main-content">
      <header class="header">
        <div class="header-left">
          <AppButton v-if="isMobile" icon="i-mdi:menu" type="text" @click="toggleSidebar" />
          <h1 class="page-title">{{ $route.meta.title || '首页' }}</h1>
        </div>
        <div class="header-right">
          <AppButton icon="i-mdi:theme-light-dark" type="text" @click="toggleTheme" />
          <AppButton icon="i-mdi:logout" type="text" @click="handleLogout" />
        </div>
      </header>
      <main class="content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
    <div class="sidebar-overlay" @click="toggleSidebar"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme'
import { useAuth } from '@/composables/useAuth'
import AppSidebar from '@/components/AppSidebar.vue'
import AppButton from '@/components/AppButton.vue'

const router = useRouter()
const { toggleTheme } = useTheme()
const { logout } = useAuth()

const isMobile = ref(false)
const isSidebarOpen = ref(false)

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
  if (!isMobile.value) {
    isSidebarOpen.value = false
  }
}

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

const handleLogout = async () => {
  await logout()
  router.push('/login')
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
  background: var(--apple-bg-primary);
  position: relative;
  overflow-x: hidden;
}

.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 240px;
  z-index: var(--apple-z-fixed);
  background: var(--apple-bg-secondary);
  border-right: 1px solid var(--apple-border);
  transition: transform var(--apple-transition);
}

.main-content {
  flex: 1;
  margin-left: 240px;
  min-width: 0;
  transition: margin-left var(--apple-transition);
}

.header {
  position: sticky;
  top: 0;
  z-index: var(--apple-z-sticky);
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 var(--apple-spacing-lg);
  background: var(--apple-bg-primary);
  border-bottom: 1px solid var(--apple-border);
  backdrop-filter: var(--apple-blur-md);
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--apple-spacing-md);
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--apple-spacing-sm);
}

.page-title {
  font-size: var(--apple-font-xl);
  font-weight: 600;
  color: var(--apple-text-primary);
  margin: 0;
}

.content {
  padding: var(--apple-spacing-lg);
}

.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: calc(var(--apple-z-fixed) - 1);
  opacity: 0;
  visibility: hidden;
  transition: all var(--apple-transition);
  pointer-events: none;
}

/* Responsive Design */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }

  .main-content {
    margin-left: 0;
  }

  .header {
    padding: 0 var(--apple-spacing-md);
  }

  .content {
    padding: var(--apple-spacing-md);
  }

  .main-layout.sidebar-open .sidebar {
    transform: translateX(0);
  }

  .main-layout.sidebar-open .sidebar-overlay {
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
  }
}
</style>
