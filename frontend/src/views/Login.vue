<template>
  <div class="login-container">
    <div class="login-content">
      <div class="login-header">
        <div class="logo-container">
          <div class="logo-circle">
            <div class="logo-inner">
              <n-icon size="32" class="logo-icon">
                <key-outlined />
              </n-icon>
            </div>
          </div>
        </div>
        <h1 class="title">密钥分析系统</h1>
        <p class="subtitle">Key Analysis System</p>
      </div>

      <n-card class="login-card">
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
              class="login-input"
            >
              <template #prefix>
                <n-icon><user-outlined /></n-icon>
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
              class="login-input"
            >
              <template #prefix>
                <n-icon><lock-outlined /></n-icon>
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
              {{ loading ? '登录中...' : '登录' }}
            </n-button>
            <n-button
              block
              size="large"
              quaternary
              @click="router.push('/register')"
              :disabled="loading"
              class="register-button"
            >
              注册账号
            </n-button>
          </div>
        </n-form>
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
  background-color: #f5f5f7;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.login-content {
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: fadeIn 0.8s ease-out;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-container {
  margin-bottom: 24px;
}

.logo-circle {
  width: 80px;
  height: 80px;
  margin: 0 auto;
  position: relative;
}

.logo-inner {
  width: 100%;
  height: 100%;
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: linear-gradient(135deg, #1a1a1a 0%, #434343 100%);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.logo-icon {
  color: white;
  font-size: 32px;
}

.title {
  font-size: 32px;
  font-weight: 600;
  margin: 0;
  background: linear-gradient(135deg, #1a1a1a 0%, #434343 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 15px;
  margin: 8px 0 0;
  color: #86868b;
  letter-spacing: -0.2px;
}

.login-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: saturate(180%) blur(20px);
  border-radius: 14px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.login-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.login-input {
  --n-border-radius: 12px;
  --n-height: 44px;
  --n-padding-left: 44px;
  --n-font-size: 15px;
  --n-border: 1px solid rgba(0, 0, 0, 0.1);
  --n-border-hover: 1px solid rgba(0, 0, 0, 0.2);
  --n-border-focus: 1px solid #1a1a1a;
  --n-placeholder-color: #86868b;
  --n-text-color: #1d1d1f;
  --n-icon-size: 18px;
  --n-loading-color: #1a1a1a;
  --n-clear-color: #86868b;
  --n-clear-size: 16px;
  --n-loading-size: 16px;
}

.action-buttons {
  margin-top: 32px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.login-button {
  --n-height: 50px;
  --n-font-size: 17px;
  --n-border-radius: 12px;
  --n-color: #1a1a1a;
  --n-color-hover: #2c2c2c;
  --n-color-pressed: #000000;
  --n-text-color: #ffffff;
  font-weight: 500;
  letter-spacing: -0.2px;
}

.register-button {
  --n-height: 50px;
  --n-font-size: 17px;
  --n-border-radius: 12px;
  --n-text-color: #1a1a1a;
  --n-text-color-hover: #2c2c2c;
  --n-text-color-pressed: #000000;
  font-weight: 500;
  letter-spacing: -0.2px;
}

.login-footer {
  margin-top: 32px;
  text-align: center;
}

.login-footer p {
  font-size: 13px;
  color: #86868b;
  letter-spacing: -0.2px;
  margin: 0;
}

@media (max-width: 768px) {
  .login-container {
    padding: 16px;
  }

  .login-content {
    max-width: 100%;
  }

  .logo-circle {
    width: 64px;
    height: 64px;
  }

  .logo-icon {
    font-size: 24px;
  }

  .title {
    font-size: 28px;
  }

  .subtitle {
    font-size: 14px;
  }

  .login-input {
    --n-height: 40px;
    --n-font-size: 14px;
    --n-padding-left: 40px;
  }

  .login-button,
  .register-button {
    --n-height: 44px;
    --n-font-size: 15px;
  }

  .action-buttons {
    margin-top: 24px;
    gap: 8px;
  }

  .login-footer {
    margin-top: 24px;
  }

  .login-footer p {
    font-size: 12px;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 
