<template>
  <div class="login-container">
    <div class="particles-container">
      <div v-for="i in 50" :key="i" class="particle"></div>
    </div>
    <div class="login-content">
      <div class="login-header">
        <div class="logo-container">
          <div class="logo-circle">
            <n-icon size="32" class="logo-icon">
              <KeyOutlined />
            </n-icon>
          </div>
        </div>
        <h1 class="title">密钥分析系统</h1>
        <p class="subtitle">Key Analysis System</p>
      </div>
      <n-card class="login-card" :bordered="false">
        <div class="card-content">
          <n-form
            ref="formRef"
            :model="formValue"
            :rules="rules"
            label-placement="left"
            label-width="0"
            size="large"
          >
            <n-form-item path="username">
              <n-input 
                v-model:value="formValue.username" 
                placeholder="用户名"
                :disabled="loading"
                class="input-with-hover"
              >
                <template #prefix>
                  <n-icon><UserOutlined /></n-icon>
                </template>
              </n-input>
            </n-form-item>
            <n-form-item path="password">
              <n-input
                v-model:value="formValue.password"
                type="password"
                placeholder="密码"
                :disabled="loading"
                @keyup.enter="handleSubmit"
                show-password-on="click"
                class="input-with-hover"
              >
                <template #prefix>
                  <n-icon><LockOutlined /></n-icon>
                </template>
              </n-input>
            </n-form-item>
            <div class="action-buttons">
              <n-button
                type="primary"
                block
                size="large"
                :loading="loading"
                @click="handleSubmit"
                class="login-button"
              >
                <template #icon>
                  <n-icon><LoginOutlined /></n-icon>
                </template>
                {{ loading ? '登录中...' : '登录' }}
              </n-button>
              <n-button
                block
                size="large"
                ghost
                @click="router.push('/register')"
                :disabled="loading"
                class="register-button"
              >
                <template #icon>
                  <n-icon><UserAddOutlined /></n-icon>
                </template>
                注册账号
              </n-button>
            </div>
          </n-form>
        </div>
      </n-card>
      <div class="login-footer">
        <p>© {{ new Date().getFullYear() }} Key Analysis System. All rights reserved.</p>
      </div>
    </div>
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
  NButton,
  NIcon
} from 'naive-ui'
import { 
  UserOutlined, 
  LockOutlined, 
  LoginOutlined, 
  UserAddOutlined,
  KeyOutlined
} from '@vicons/antd'
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
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1c2a 0%, #2d1b3d 100%);
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.particles-container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
}

.particle {
  position: absolute;
  width: 3px;
  height: 3px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  animation: float 20s infinite linear;
}

@keyframes float {
  0% {
    transform: translateY(100vh) scale(0);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100vh) scale(1);
    opacity: 0;
  }
}

.particle:nth-child(odd) {
  animation-duration: 15s;
  width: 2px;
  height: 2px;
}

.particle:nth-child(3n) {
  animation-duration: 25s;
  width: 4px;
  height: 4px;
}

.particle:nth-child(3n+1) {
  animation-delay: -5s;
}

.particle:nth-child(3n+2) {
  animation-delay: -10s;
}

.particle:nth-child(5n) {
  animation-duration: 30s;
}

.login-content {
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: fadeIn 0.8s ease-out;
  position: relative;
  z-index: 1;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
  color: white;
}

.logo-container {
  margin-bottom: 20px;
}

.logo-circle {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
  animation: pulse 2s infinite;
}

.logo-icon {
  color: white;
  font-size: 32px;
  animation: rotate 10s linear infinite;
}

.title {
  font-size: 32px;
  font-weight: 600;
  margin: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.subtitle {
  font-size: 16px;
  margin: 8px 0 0;
  opacity: 0.9;
  letter-spacing: 1px;
  color: rgba(255, 255, 255, 0.7);
}

.login-card {
  width: 100%;
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  overflow: hidden;
}

.login-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.2);
}

.card-content {
  padding: 32px;
  position: relative;
}

.card-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.2) 50%, 
    transparent 100%
  );
}

.action-buttons {
  margin-top: 32px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.login-button {
  height: 48px;
  font-size: 16px;
  font-weight: 500;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.login-button::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  transform: rotate(45deg);
  animation: shine 3s infinite;
}

.login-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.register-button {
  height: 48px;
  font-size: 16px;
  color: #667eea;
  border-color: rgba(102, 126, 234, 0.5);
  background: transparent;
  backdrop-filter: blur(5px);
}

.register-button:hover {
  border-color: #667eea;
  color: #764ba2;
  background: rgba(255, 255, 255, 0.1);
}

.login-footer {
  margin-top: 32px;
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

:deep(.n-form-item) {
  margin-bottom: 24px;
}

:deep(.n-input) {
  height: 48px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

:deep(.n-input:hover),
:deep(.n-input:focus) {
  border-color: rgba(102, 126, 234, 0.5);
  background: rgba(255, 255, 255, 0.1);
}

:deep(.n-input__input-el) {
  font-size: 15px;
  color: rgba(255, 255, 255, 0.9);
}

:deep(.n-input__placeholder) {
  color: rgba(255, 255, 255, 0.5);
}

:deep(.n-input__prefix) {
  margin-right: 12px;
  color: rgba(255, 255, 255, 0.5);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
  }
  50% {
    box-shadow: 0 4px 30px rgba(102, 126, 234, 0.5);
  }
  100% {
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes shine {
  0% {
    left: -50%;
  }
  100% {
    left: 150%;
  }
}

@media (max-width: 480px) {
  .login-content {
    max-width: 100%;
  }
  
  .title {
    font-size: 28px;
  }
  
  .subtitle {
    font-size: 14px;
  }
  
  .card-content {
    padding: 24px;
  }
  
  .logo-circle {
    width: 64px;
    height: 64px;
  }
  
  .logo-icon {
    font-size: 24px;
  }
}
</style> 
