<template>
  <div class="register-container">
    <n-card title="注册" class="register-card">
      <n-form
        ref="formRef"
        :model="formValue"
        :rules="rules"
      >
        <n-form-item path="username" label="用户名">
          <n-input 
            v-model:value="formValue.username" 
            placeholder="请输入用户名"
            :disabled="loading"
          />
        </n-form-item>
        <n-form-item path="email" label="邮箱">
          <n-input 
            v-model:value="formValue.email" 
            placeholder="请输入邮箱"
            :disabled="loading"
          />
        </n-form-item>
        <n-form-item path="password" label="密码">
          <n-input
            v-model:value="formValue.password"
            type="password"
            placeholder="请输入密码"
            :disabled="loading"
          />
        </n-form-item>
        <n-form-item path="confirmPassword" label="确认密码">
          <n-input
            v-model:value="formValue.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            :disabled="loading"
          />
        </n-form-item>
        <div class="action-buttons">
          <n-button
            type="primary"
            block
            :loading="loading"
            @click="handleSubmit"
          >
            注册
          </n-button>
          <n-button
            block
            @click="router.push('/login')"
            :disabled="loading"
          >
            返回登录
          </n-button>
        </div>
      </n-form>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { 
  NCard, 
  NForm, 
  NFormItem, 
  NInput, 
  NButton 
} from 'naive-ui'
import { auth } from '../services/auth'
import { debug } from '../utils/debug'

const router = useRouter()
const message = useMessage()
const loading = ref(false)
const formRef = ref<typeof NForm | null>(null)

const formValue = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: ['blur', 'input'] },
    { min: 3, message: '用户名至少3个字符', trigger: ['blur', 'input'] }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: ['blur', 'input'] },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: ['blur', 'input'] }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: ['blur', 'input'] },
    { min: 6, message: '密码至少6个字符', trigger: ['blur', 'input'] }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: ['blur', 'input'] },
    {
      validator: (rule: any, value: string) => value === formValue.value.password,
      message: '两次输入的密码不一致',
      trigger: ['blur', 'input']
    }
  ]
}

const handleSubmit = async () => {
  try {
    loading.value = true
    await formRef.value?.validate()
    
    debug.log('Register attempt:', { 
      username: formValue.value.username,
      email: formValue.value.email 
    })
    
    await auth.register({
      username: formValue.value.username,
      email: formValue.value.email,
      password: formValue.value.password
    })
    
    message.success('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    if (error instanceof Error) {
      const errorMsg = error.message
      if (errorMsg.includes('Username already registered')) {
        message.error('用户名已被注册')
      } else if (errorMsg.includes('Email already registered')) {
        message.error('邮箱已被注册')
      } else {
        message.error(errorMsg)
      }
    } else {
      message.error('注册失败，请重试')
    }
    debug.error('Register failed:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f2f5;
}

.register-card {
  width: 100%;
  max-width: 360px;
}

.register-card :deep(.n-card-header) {
  text-align: center;
  font-size: 24px;
  padding: 20px 0;
}

.action-buttons {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

:deep(.n-form-item) {
  margin-bottom: 24px;
}

:deep(.n-input) {
  width: 100%;
}
</style> 
