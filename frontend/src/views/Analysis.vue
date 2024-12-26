<script setup lang="ts">
import { ref } from 'vue'
import { NCard, NSpace, NH1, NInput, NButton, NGrid, NGridItem, NStatistic, NDivider, NProgress } from 'naive-ui'

const key = ref('')
const loading = ref(false)
const analysisResult = ref<{
  repeat_letter_score: number
  increasing_letter_score: number
  decreasing_letter_score: number
  magic_letter_score: number
  unique_letters_count: number
  score: number
} | null>(null)

const handleAnalyze = async () => {
  if (!key.value.trim()) return

  loading.value = true
  try {
    // TODO: 实现密钥分析API调用
    // const result = await analyzeKey(key.value)
    // analysisResult.value = result

    // 模拟数据
    analysisResult.value = {
      repeat_letter_score: 85,
      increasing_letter_score: 75,
      decreasing_letter_score: 60,
      magic_letter_score: 90,
      unique_letters_count: 12,
      score: 420
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="analysis-container">
    <NSpace vertical size="large">
      <NH1>密钥分析</NH1>

      <NCard>
        <NSpace vertical>
          <div class="input-section">
            <NInput v-model:value="key" type="text" placeholder="请输入要分析的密钥" :disabled="loading"
              @keyup.enter="handleAnalyze" />
            <NButton type="primary" :loading="loading" :disabled="!key.trim()" @click="handleAnalyze">
              分析
            </NButton>
          </div>

          <NDivider v-if="analysisResult">分析结果</NDivider>

          <div v-if="analysisResult" class="result-section">
            <NGrid :cols="3" :x-gap="12" :y-gap="12">
              <NGridItem>
                <NCard>
                  <NStatistic label="综合评分" :value="analysisResult.score" :precision="0">
                    <template #suffix>
                      <NProgress type="line" :percentage="(analysisResult.score / 500) * 100" :show-indicator="false"
                        :height="4" :border-radius="4" :color="analysisResult.score >= 400 ? '#18a058' : '#f0a020'" />
                    </template>
                  </NStatistic>
                </NCard>
              </NGridItem>
              <NGridItem>
                <NCard>
                  <NStatistic label="重复字母分数" :value="analysisResult.repeat_letter_score" />
                </NCard>
              </NGridItem>
              <NGridItem>
                <NCard>
                  <NStatistic label="递增序列分数" :value="analysisResult.increasing_letter_score" />
                </NCard>
              </NGridItem>
              <NGridItem>
                <NCard>
                  <NStatistic label="递减序列分数" :value="analysisResult.decreasing_letter_score" />
                </NCard>
              </NGridItem>
              <NGridItem>
                <NCard>
                  <NStatistic label="特殊组合分数" :value="analysisResult.magic_letter_score" />
                </NCard>
              </NGridItem>
              <NGridItem>
                <NCard>
                  <NStatistic label="唯一字母数" :value="analysisResult.unique_letters_count" />
                </NCard>
              </NGridItem>
            </NGrid>
          </div>
        </NSpace>
      </NCard>
    </NSpace>
  </div>
</template>

<style scoped>
.analysis-container {
  max-width: 1200px;
  margin: 0 auto;
}

.input-section {
  display: flex;
  gap: 16px;
}

.input-section :deep(.n-input) {
  flex: 1;
}

.result-section {
  margin-top: 16px;
}

:deep(.n-statistic-label) {
  font-size: 14px;
  color: #4b5563;
}

:deep(.n-statistic-value) {
  font-size: 24px;
  font-weight: 500;
}
</style>
