<template>
  <div class="about-page">
    <div class="about-content">
      <h2 class="about-title">关于密钥分析系统</h2>
      <p class="about-description">
        密钥分析系统是一个专业的密钥管理和分析工具，旨在帮助用户更好地管理和分析密钥使用情况。
      </p>

      <div class="feature-list">
        <div class="feature-item">
          <div class="i-mdi:shield-check text-2xl" />
          <h3>安全可靠</h3>
          <p>采用先进的加密技术，确保密钥数据的安全性</p>
        </div>
        <div class="feature-item">
          <div class="i-mdi:chart-box text-2xl" />
          <h3>数据分析</h3>
          <p>提供全面的数据分析功能，帮助优化密钥使用</p>
        </div>
        <div class="feature-item">
          <div class="i-mdi:account-group text-2xl" />
          <h3>多用户支持</h3>
          <p>支持多用户协同工作，权限管理灵活</p>
        </div>
      </div>

      <div class="version-info">
        <h3>系统信息</h3>
        <p>版本：1.0.0</p>
        <p>最后更新：2024-01-20</p>
      </div>

      <div class="contact-info">
        <h3>联系我们</h3>
        <p>如有问题或建议，请通过以下方式联系我们：</p>
        <ul>
          <li>邮箱：support@example.com</li>
          <li>电话：400-123-4567</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: 'AboutPage'
})
</script>

<style scoped>
.about-page {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.about-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.about-title {
  font-size: 2rem;
  font-weight: 600;
  color: var(--apple-text-primary);
  margin-bottom: 1rem;
}

.about-description {
  font-size: 1.125rem;
  color: var(--apple-text-secondary);
  line-height: 1.6;
}

.feature-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 2rem;
  background: var(--apple-bg-secondary);
  border-radius: 1rem;
  border: 1px solid var(--apple-border);
  transition: all 0.2s ease;
}

.feature-item:hover {
  transform: translateY(-4px);
  box-shadow: var(--apple-shadow);
}

.feature-item h3 {
  margin: 1rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--apple-text-primary);
}

.feature-item p {
  color: var(--apple-text-secondary);
  line-height: 1.5;
}

.version-info,
.contact-info {
  padding: 1.5rem;
  background: var(--apple-bg-secondary);
  border-radius: 1rem;
  border: 1px solid var(--apple-border);
}

.version-info h3,
.contact-info h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--apple-text-primary);
  margin-bottom: 1rem;
}

.version-info p,
.contact-info p {
  color: var(--apple-text-secondary);
  margin-bottom: 0.5rem;
}

.contact-info ul {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0;
}

.contact-info li {
  color: var(--apple-text-secondary);
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .about-page {
    padding: 1rem;
  }

  .feature-list {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .feature-item {
    padding: 1.5rem;
  }
}
</style>
