<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NSpace, NH1, NGrid, NGridItem, NDataTable, NDatePicker, NStatistic } from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'

interface AnalysisRecord {
  id: number
  created_at: string
  fingerprint: string
  score: number
  repeat_letter_score: number
  increasing_letter_score: number
  decreasing_letter_score: number
  magic_letter_score: number
  unique_letters_count: number
}

const loading = ref(true)
const dateRange = ref<[number, number] | null>(null)
const statistics = ref({
  total_analysis: 0,
  high_score_count: 0,
  average_score: 0,
  today_analysis: 0
})

const recentRecords = ref<AnalysisRecord[]>([])

const columns: DataTableColumns<AnalysisRecord> = [
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
  },
  {
    title: '特殊组合分数',
    key: 'magic_letter_score'
  },
  {
    title: '唯一字母数',
    key: 'unique_letters_count'
  }
]

const fetchStatistics = async () => {
  // TODO: 实现获取统计数据的API调用
  // const data = await getStatistics(dateRange.value)

  // 模拟数据
  statistics.value = {
    total_analysis: 1234,
    high_score_count: 256,
    average_score: 385,
    today_analysis: 42
  }
}

const fetchRecentRecords = async () => {
  // TODO: 实现获取最近记录的API调用
  // const data = await getRecentRecords()

  // 模拟数据
  recentRecords.value = [
    {
      id: 1,
      created_at: '2024-01-20 10:30:00',
      fingerprint: 'abc123',
      score: 420,
      repeat_letter_score: 85,
      increasing_letter_score: 75,
      decreasing_letter_score: 60,
      magic_letter_score: 90,
      unique_letters_count: 12
    }
    // ... 更多记录
  ]
}

const handleDateRangeChange = async (value: [number, number] | null) => {
  dateRange.value = value
  await fetchStatistics()
}

onMounted(async () => {
  try {
    await Promise.all([
      fetchStatistics(),
      fetchRecentRecords()
    ])
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="statistics-container">
    <NSpace vertical size="large">
      <div class="statistics-header">
        <NH1>统计报告</NH1>
        <NDatePicker type="daterange" :value="dateRange" @update:value="handleDateRangeChange" clearable />
      </div>

      <NGrid :cols="4" :x-gap="12" :y-gap="12">
        <NGridItem>
          <NCard>
            <NStatistic label="总分析次数" :value="statistics.total_analysis" :loading="loading" />
          </NCard>
        </NGridItem>
        <NGridItem>
          <NCard>
            <NStatistic label="高分密钥数" :value="statistics.high_score_count" :loading="loading" />
          </NCard>
        </NGridItem>
        <NGridItem>
          <NCard>
            <NStatistic label="平均分数" :value="statistics.average_score" :loading="loading" />
          </NCard>
        </NGridItem>
        <NGridItem>
          <NCard>
            <NStatistic label="今日分析" :value="statistics.today_analysis" :loading="loading" />
          </NCard>
        </NGridItem>
      </NGrid>

      <NCard title="最近分析记录">
        <NDataTable :loading="loading" :columns="columns" :data="recentRecords" :pagination="{
          pageSize: 10
        }" :scroll-x="1200" />
      </NCard>
    </NSpace>
  </div>
</template>

<style scoped>
.statistics-container {
  max-width: 1200px;
  margin: 0 auto;
}

.statistics-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
