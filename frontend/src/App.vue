<template>
  <n-config-provider :inline-theme="false">
    <n-message-provider tag="div">
      <n-layout>
        <n-layout-header bordered>
          <div class="header-content">
            <h1>密钥分析系统</h1>
          </div>
        </n-layout-header>
        <n-layout-content>
          <KeyAnalysis />
        </n-layout-content>
      </n-layout>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { 
  NConfigProvider, 
  NMessageProvider, 
  NLayout, 
  NLayoutHeader,
  NLayoutContent
} from 'naive-ui'
import KeyAnalysis from './components/KeyAnalysis.vue'
</script>

<style>
.header-content {
  padding: 0 20px;
  height: 64px;
  display: flex;
  align-items: center;
}

.header-content h1 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--n-text-color);
}

:root {
  --n-layout-padding: 20px;
}
</style> 
