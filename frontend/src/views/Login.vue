<template>
  <AuthLayout>
    <NCard class="login-card" title="登录" :bordered="false">
      <NForm ref="formRef" :model="formValue" @submit.prevent="handleSubmit">
        <NFormItem label="用户名" path="username">
          <NInput v-model:value="formValue.username" placeholder="请输入用户名" />
        </NFormItem>
        <NFormItem label="密码" path="password">
          <NInput v-model:value="formValue.password" type="password" placeholder="请输入密码" show-password-on="click" />
        </NFormItem>
        <div class="action-row">
          <NButton type="primary" attr-type="submit" :loading="loading" block>
            {{ loading ? '登录中...' : '登录' }}
          </NButton>
          <NButton quaternary block @click="router.push('/register')">
            注册账号
          </NButton>
        </div>
      </NForm>
    </NCard>
  </AuthLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NForm, NFormItem, NInput, NButton, useMessage } from 'naive-ui'
import { useAuth } from '../composables/useAuth'
import AuthLayout from '../layouts/AuthLayout.vue'

const router = useRouter()
const message = useMessage()
const auth = useAuth()

const formRef = ref()
const loading = ref(false)
const formValue = ref({
  username: '',
  password: ''
})

const handleSubmit = async () => {
  try {
    loading.value = true
    await auth.login(formValue.value)
    message.success('登录成功')
    router.push('/dashboard')
  } catch (error: unknown) {
    if (error instanceof Error) {
      message.error('登录失败: ' + error.message)
    } else {
      message.error('登录失败，请检查用户名和密码')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-card {
  width: 100%;
  max-width: 400px;
  margin: 0 20px;
  background-color: var(--apple-bg-secondary) !important;
  border-radius: var(--apple-radius-lg) !important;
  box-shadow: var(--apple-shadow-lg) !important;
  backdrop-filter: var(--apple-blur-effect);
}

.login-card :deep(.n-card-header) {
  font-size: var(--apple-font-xl);
  font-weight: 600;
  color: var(--apple-text-primary);
  text-align: center;
  padding-bottom: 24px;
}

.login-card :deep(.n-card__content) {
  padding: 0 24px 24px;
}

.action-row {
  margin-top: 32px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 适配暗色主题的输入框样式 */
:deep(.n-input) {
  background-color: var(--apple-bg-primary) !important;
}

:deep(.n-input .n-input__input-el) {
  color: var(--apple-text-primary) !important;
}

:deep(.n-form-item-label) {
  color: var(--apple-text-primary) !important;
}
</style>
