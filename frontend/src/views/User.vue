<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NSpace, NH1, NDescriptions, NDescriptionsItem, NDataTable } from 'naive-ui'
import { auth } from '../services/auth'
import type { User } from '../types/user'

const user = ref<User | null>(null)
const analysisHistory = ref([])
const loading = ref(true)

const columns = [
  {
    title: '分析时间',
    key: 'created_at',
    sorter: true
  },
  {
    title: '密钥指纹',
    key: 'fingerprint'
  },
  {
    title: '综合评分',
    key: 'score',
    sorter: true
  },
  {
    title: '重复字母分数',
    key: 'repeat_letter_score'
  },
  {
    title: '递增序列分数',
    key: 'increasing_letter_score'
  },
  {
    title: '递减序列分数',
    key: 'decreasing_letter_score'
  }
]

onMounted(async () => {
  try {
    user.value = await auth.getCurrentUser()
    // TODO: 实现获取分析历史的API调用
    // analysisHistory.value = await fetchAnalysisHistory()
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="user-container">
    <NSpace vertical size="large">
      <NH1>用户中心</NH1>

      <NCard title="个人信息" :loading="loading">
        <NDescriptions v-if="user" bordered>
          <NDescriptionsItem label="用户名">
            {{ user.username }}
          </NDescriptionsItem>
          <NDescriptionsItem label="注册时间">
            {{ user.created_at }}
          </NDescriptionsItem>
          <NDescriptionsItem label="上次登录">
            {{ user.last_login }}
          </NDescriptionsItem>
        </NDescriptions>
      </NCard>

      <NCard title="分析历史" :loading="loading">
        <NDataTable :columns="columns" :data="analysisHistory" :pagination="{
          pageSize: 10
        }" />
      </NCard>
    </NSpace>
  </div>
</template>

<style scoped>
.user-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>
