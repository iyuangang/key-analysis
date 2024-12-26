<template>
  <AuthLayout>
    <NCard class="register-card" title="注册账号" :bordered="false">
      <NForm ref="formRef" :model="formValue" @submit.prevent="handleSubmit">
        <NFormItem label="用户名" path="username">
          <NInput v-model:value="formValue.username" placeholder="请输入用户名" />
        </NFormItem>
        <NFormItem label="邮箱" path="email">
          <NInput v-model:value="formValue.email" placeholder="请输入邮箱" />
        </NFormItem>
        <NFormItem label="密码" path="password">
          <NInput v-model:value="formValue.password" type="password" placeholder="请输入密码" show-password-on="click" />
        </NFormItem>
        <NFormItem label="确认密码" path="confirmPassword">
          <NInput v-model:value="formValue.confirmPassword" type="password" placeholder="请再次输入密码"
            show-password-on="click" />
        </NFormItem>
        <div class="action-row">
          <NButton type="primary" attr-type="submit" :loading="loading" block>
            {{ loading ? '注册中...' : '注册' }}
          </NButton>
          <NButton quaternary block @click="router.push('/login')">
            返回登录
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
  email: '',
  password: '',
  confirmPassword: ''
})

const handleSubmit = async () => {
  if (formValue.value.password !== formValue.value.confirmPassword) {
    message.error('两次输入的密码不一致')
    return
  }

  try {
    loading.value = true
    await auth.register(formValue.value)
    message.success('注册成功')
    router.push('/login')
  } catch (error: unknown) {
    if (error instanceof Error) {
      message.error('注册失败: ' + error.message)
    } else {
      message.error('注册失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-card {
  width: 100%;
  max-width: 400px;
  margin: 0 20px;
  background-color: var(--apple-bg-secondary) !important;
  border-radius: var(--apple-radius-lg) !important;
  box-shadow: var(--apple-shadow-lg) !important;
  backdrop-filter: var(--apple-blur-effect);
}

.register-card :deep(.n-card-header) {
  font-size: var(--apple-font-xl);
  font-weight: 600;
  color: var(--apple-text-primary);
  text-align: center;
  padding-bottom: 24px;
}

.register-card :deep(.n-card__content) {
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
