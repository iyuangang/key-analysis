<template>
  <div class="login-container">
    <n-card title="登录" class="login-card">
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
        <n-form-item path="password" label="密码">
          <n-input
            v-model:value="formValue.password"
            type="password"
            placeholder="请输入密码"
            :disabled="loading"
            @keyup.enter="handleSubmit"
          />
        </n-form-item>
        <div class="action-buttons">
          <n-button
            type="primary"
            block
            :loading="loading"
            @click="handleSubmit"
          >
            登录
          </n-button>
          <n-button
            block
            @click="router.push('/register')"
            :disabled="loading"
          >
            注册账号
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
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: ['blur', 'input'] }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: ['blur', 'input'] }
  ]
}

const handleSubmit = async () => {
  try {
    loading.value = true
    debug.log('Login attempt:', { username: formValue.value.username })
    
    const token = await auth.login(formValue.value)
    if (!token) {
      throw new Error('登录失败：未获取到访问令牌')
    }
    
    message.success('登录成功')
    router.push('/dashboard')
  } catch (error) {
    debug.error('Login failed:', error)
    if (error instanceof Error) {
      message.error(error.message)
    } else {
      message.error('登录失败，请检查用户名和密码')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f2f5;
}

.login-card {
  width: 100%;
  max-width: 360px;
}

.login-card :deep(.n-card-header) {
  text-align: center;
  font-size: 24px;
  padding: 20px 0;
}

.action-buttons {
  margin-top: 24px;
}

:deep(.n-form-item) {
  margin-bottom: 24px;
}

:deep(.n-input) {
  width: 100%;
}
</style> 
