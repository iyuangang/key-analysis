<template>
  <header class="app-header">
    <div class="header-left">
      <button v-if="isMobile" class="menu-btn" @click="$emit('toggle-sidebar')">
        <div class="i-mdi:menu" />
      </button>
      <h1 class="page-title">{{ props.title }}</h1>
      <slot name="breadcrumb"></slot>
    </div>
    <div class="header-right">
      <slot name="actions"></slot>
      <div class="header-actions">
        <button class="action-btn" @click="toggleTheme"
          :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'">
          <div class="i-mdi:weather-sunny" v-if="isDark" />
          <div class="i-mdi:weather-night" v-else />
        </button>
        <div class="user-menu" @click="showUserDropdown = !showUserDropdown" ref="userMenuRef">
          <img :src="props.userAvatar" alt="User Avatar" class="user-avatar" />
          <span v-if="!isMobile" class="username">{{ props.username }}</span>
          <div class="i-mdi:chevron-down" :class="{ 'rotate-180': showUserDropdown }" />

          <!-- User Dropdown Menu -->
          <div v-show="showUserDropdown" class="dropdown-menu">
            <router-link to="/profile" class="dropdown-item">
              <div class="i-mdi:account" />
              <span>个人资料</span>
            </router-link>
            <router-link to="/settings" class="dropdown-item">
              <div class="i-mdi:cog" />
              <span>设置</span>
            </router-link>
            <div class="divider"></div>
            <button class="dropdown-item text-red" @click="handleLogout">
              <div class="i-mdi:logout" />
              <span>退出登录</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useTheme } from '@/composables/useTheme'
import { useRouter } from 'vue-router'
import { auth } from '@/services/auth'

const props = defineProps<{
  title: string
  username: string
  userAvatar: string
  isMobile: boolean
}>()

defineEmits<{
  (e: 'toggle-sidebar'): void
}>()

const router = useRouter()
const { isDark, toggleTheme } = useTheme()
const showUserDropdown = ref(false)
const userMenuRef = ref<HTMLElement | null>(null)

// 处理点击外部关闭下拉菜单
const handleClickOutside = (event: MouseEvent) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target as Node)) {
    showUserDropdown.value = false
  }
}

// 处理退出登录
const handleLogout = async () => {
  try {
    await auth.logout()
    router.push('/login')
  } catch (error) {
    console.error('Logout failed:', error)
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: var(--apple-bg-secondary);
  border-bottom: 1px solid var(--apple-border);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--apple-text-primary);
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.5rem;
  border-radius: 0.375rem;
  background: transparent;
  border: none;
  cursor: pointer;
  color: var(--apple-text-secondary);
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: var(--apple-hover-bg);
  color: var(--apple-text-primary);
}

.user-menu {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-menu:hover {
  background: var(--apple-hover-bg);
}

.user-avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  object-fit: cover;
  color: var(--apple-text-secondary);
}

.user-avatar :deep(.avatar-bg) {
  fill: currentColor;
}

.user-avatar :deep(.avatar-fg) {
  fill: var(--apple-bg-primary);
}

.username {
  font-weight: 500;
  color: var(--apple-text-primary);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  min-width: 200px;
  background: var(--apple-card-bg);
  border: 1px solid var(--apple-border);
  border-radius: 0.5rem;
  box-shadow: var(--apple-shadow);
  z-index: 100;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: var(--apple-text-primary);
  text-decoration: none;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background: var(--apple-hover-bg);
}

.dropdown-item.text-red {
  color: var(--apple-red);
}

.divider {
  height: 1px;
  background: var(--apple-border);
  margin: 0.5rem 0;
}

.rotate-180 {
  transform: rotate(180deg);
}

.menu-btn {
  padding: 0.5rem;
  margin-right: 0.5rem;
  border-radius: 0.375rem;
  background: transparent;
  border: none;
  cursor: pointer;
  color: var(--apple-text-secondary);
  transition: all 0.2s ease;
}

.menu-btn:hover {
  background: var(--apple-hover-bg);
  color: var(--apple-text-primary);
}

@media (max-width: 768px) {
  .app-header {
    padding: 0.75rem 1rem;
  }

  .page-title {
    font-size: 1.25rem;
  }

  .header-actions {
    gap: 0.25rem;
  }

  .action-btn,
  .menu-btn {
    padding: 0.375rem;
  }

  .user-menu {
    padding: 0.375rem;
  }
}
</style>
