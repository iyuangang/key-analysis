<template>
  <div class="analysis-container">
    <div class="filter-container">
      <n-space align="center">
        <n-radio-group v-model:value="dateRange" size="small">
          <n-radio-button value="today">今日</n-radio-button>
          <n-radio-button value="custom">自定义</n-radio-button>
          <n-radio-button value="all">全部</n-radio-button>
        </n-radio-group>
        <n-date-picker
          v-if="dateRange === 'custom'"
          v-model:value="customDateRange"
          type="daterange"
          :disabled="dateRange !== 'custom'"
          clearable
          size="small"
          :is-date-disabled="disableFutureDates"
        />
        <n-button 
          size="small" 
          type="primary"
          :loading="loading"
          @click="refreshData"
        >
          刷新
        </n-button>
      </n-space>
    </div>

    <n-grid :x-gap="24" :y-gap="24" :cols="4">
      <n-grid-item v-for="stat in summaryStats" :key="stat.title">
        <n-card class="stat-card">
          <div class="stat-title">{{ stat.title }}</div>
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-trend" :class="stat.trend">
            {{ stat.trendValue }}
            <n-icon size="14">
              <trend-up-outlined v-if="stat.trend === 'up'" />
              <trend-down-outlined v-else />
            </n-icon>
          </div>
        </n-card>
      </n-grid-item>
    </n-grid>

    <div class="charts-container">
      <div class="chart-wrapper">
        <div ref="scoreDistChart" class="chart"></div>
      </div>
      <div class="chart-wrapper">
        <div ref="correlationChart" class="chart"></div>
      </div>
      <div class="chart-wrapper">
        <div ref="trendChart" class="chart"></div>
      </div>
      <div class="chart-wrapper">
        <div ref="scoreTypesChart" class="chart"></div>
      </div>
    </div>

    <div class="tables-container">
      <DataTable 
        title="最近24小时生成的密钥" 
        :data="recentKeys" 
      />
      <DataTable 
        title="得分最高的密钥(>400分)" 
        :data="highScoreKeys" 
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import {
  ArrowUpOutlined as TrendUpOutlined,
  ArrowDownOutlined as TrendDownOutlined
} from '@vicons/antd'
import { 
  useMessage,
  NGrid,
  NGridItem,
  NCard,
  NIcon,
  NDataTable,
  NSpace,
  NRadioGroup,
  NRadioButton,
  NDatePicker,
  NButton
} from 'naive-ui'
import { getRecentKeys, getHighScoreKeys, getStatistics } from '../services/api'
import DataTable from './DataTable.vue'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'
import { debug } from '../utils/debug'

dayjs.extend(utc)
dayjs.extend(timezone)

// 设置默认时区
const TIMEZONE = 'Asia/Shanghai'

const message = useMessage()
const scoreDistChart = ref()
const correlationChart = ref()
const scoreTypesChart = ref()
const trendChart = ref()
const recentKeys = ref([])
const highScoreKeys = ref([])
const summaryStats = ref([
  {
    title: '平均得分',
    value: '0',
    trend: 'up',
    trendValue: '0%'
  },
  {
    title: '最高得分',
    value: '0',
    trend: 'up',
    trendValue: '0%'
  },
  {
    title: '生成数量',
    value: '0',
    trend: 'down',
    trendValue: '0%'
  },
  {
    title: '合格率',
    value: '0%',
    trend: 'up',
    trendValue: '0%'
  }
])

const dateRange = ref('today')
const customDateRange = ref<[number, number] | null>(null)
const loading = ref(false)

const actualDateRange = computed(() => {
  const now = dayjs().tz(TIMEZONE)
  const today = now.startOf('day')
  
  debug.log('Calculating date range:', {
    now: {
      timestamp: now.valueOf(),
      formatted: now.format('YYYY-MM-DD HH:mm:ss'),
      timezone: TIMEZONE
    },
    today: {
      timestamp: today.valueOf(),
      formatted: today.format('YYYY-MM-DD HH:mm:ss'),
      timezone: TIMEZONE
    }
  })
  
  switch (dateRange.value) {
    case 'today':
      return {
        start: today.valueOf(),
        end: now.valueOf()
      }
    case 'custom':
      if (customDateRange.value) {
        const [start, end] = customDateRange.value
        const startDate = dayjs(start).tz(TIMEZONE).startOf('day')
        const endDate = dayjs(end).tz(TIMEZONE).endOf('day')
        
        debug.log('Custom date range:', {
          input: {
            start,
            end
          },
          output: {
            start: {
              timestamp: startDate.valueOf(),
              formatted: startDate.format('YYYY-MM-DD HH:mm:ss')
            },
            end: {
              timestamp: endDate.valueOf(),
              formatted: endDate.format('YYYY-MM-DD HH:mm:ss')
            }
          }
        })
        
        return {
          start: startDate.valueOf(),
          end: endDate.valueOf()
        }
      }
      return null
    case 'all':
      return null
    default:
      return {
        start: today.valueOf(),
        end: now.valueOf()
      }
  }
})

const disableFutureDates = (ts: number) => {
  return ts > dayjs().tz(TIMEZONE).valueOf()
}

const refreshData = async () => {
  if (loading.value) return
  loading.value = true
  try {
    const range = actualDateRange.value
    debug.log('Fetching data with range:', range)
    
    const [recentData, highScoreData, statsData] = await Promise.all([
      getRecentKeys(range),
      getHighScoreKeys(range),
      getStatistics(range)
    ])
    
    debug.log('Received data:', {
      recentData,
      highScoreData,
      statsData
    })

    // 检查数据是否有效
    if (!recentData || !Array.isArray(recentData)) {
      debug.warn('Invalid recent keys data:', recentData)
      recentKeys.value = []
    } else {
      recentKeys.value = recentData
    }
    
    if (!highScoreData || !Array.isArray(highScoreData)) {
      debug.warn('Invalid high score keys data:', highScoreData)
      highScoreKeys.value = []
    } else {
      highScoreKeys.value = highScoreData
    }
    
    if (statsData && typeof statsData === 'object') {
      debug.log('Processing stats data:', statsData)
      initCharts(statsData)
      updateSummaryStats(statsData)
    } else {
      debug.warn('Invalid statistics data:', statsData)
      message.warning('没有获取到统计数据')
    }
  } catch (error) {
    debug.error('Failed to fetch data:', error)
    message.error('获取数据失败，请检查网络连接')
  } finally {
    loading.value = false
  }
}

watch([dateRange, customDateRange], () => {
  refreshData()
})

let charts: echarts.ECharts[] = []

// 格式化显示名称
const typeNames: Record<string, string> = {
  repeat_letter_score: '重复字母',
  increasing_letter_score: '递增字母',
  decreasing_letter_score: '递减字母',
  magic_letter_score: '魔法字母',
  score: '总分',
  unique_letters_count: '唯一字母数'
}

const scoreTypes = [
  'repeat_letter_score',
  'increasing_letter_score',
  'decreasing_letter_score',
  'magic_letter_score'
]

onMounted(async () => {
  refreshData()
})

onUnmounted(() => {
  charts.forEach(chart => chart.dispose())
  // 移除resize监听器
  window.removeEventListener('resize', handleResize)
})

// 将resize处理函数提取出来
const handleResize = () => {
  charts.forEach(chart => chart.resize())
}

const initCharts = (statsData: any) => {
  try {
    // 数据验证
    if (!statsData || typeof statsData !== 'object') {
      console.warn('Invalid score distribution data')
      message.warning('当前时间范围内没有数据')
      return
    }

    // 检查是否有实际数据
    if (!statsData.score_distribution || statsData.score_distribution.total_count === 0) {
      message.warning('所选时间范围内没有数据')
      return
    }

    debug.log('Initializing charts with data:', {
      distribution: statsData.score_distribution,
      correlation: statsData.correlation_matrix,
      trends: statsData.trends
    })

    // 验证必要的数据结构
    if (!statsData.score_distribution.bins || !statsData.score_distribution.histogram) {
      debug.warn('Missing required score distribution data')
      message.warning('统计数据格式不正确')
      return
    }

    // 得分分布图
    const scoreChart = echarts.init(scoreDistChart.value)
    const scoreStats = statsData.score_distribution
    const binWidth = scoreStats.bins[1] - scoreStats.bins[0]
    
    scoreChart.setOption({
      title: {
        text: '得分分布',
        subtext: `总样本数: ${scoreStats.total_count} | 合格数: ${scoreStats.qualified_count}`,
        left: 'center',
        top: 10,
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      grid: {
        top: '15%',
        left: '10%',
        right: '5%',
        bottom: '15%'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: function(params: any) {
          const value = params[0].value
          const start = Math.round(scoreStats.bins[params[0].dataIndex])
          const end = Math.round(start + binWidth)
          const total = scoreStats.total_count
          return [
            `分数区间: ${start} - ${end}`,
            `数量: ${value}`,
            `占比: ${(value / total * 100).toFixed(1)}%`,
            '-------------------',
            `平均值: ${scoreStats.mean.toFixed(1)}`,
            `中位数: ${scoreStats.median.toFixed(1)}`,
            `标准差: ${scoreStats.std.toFixed(1)}`,
            `Q1: ${scoreStats.q1.toFixed(1)}`,
            `Q3: ${scoreStats.q3.toFixed(1)}`
          ].join('<br/>')
        }
      },
      xAxis: {
        type: 'category',
        data: statsData.score_distribution.bins.slice(0, -1).map((v: number) => Math.round(v)),
        name: '得分',
        nameLocation: 'middle',
        nameGap: 30,
        axisLabel: {
          interval: 4,
          formatter: (value: number) => {
            return value.toString()
          }
        }
      },
      yAxis: {
        type: 'value',
        name: '数量',
        nameLocation: 'middle',
        nameGap: 40,
        minInterval: 1,
        splitLine: {
          show: true,
          lineStyle: {
            type: 'dashed'
          }
        }
      },
      series: [{
        data: statsData.score_distribution.histogram,
        type: 'bar',
        name: '数量',
        itemStyle: {
          color: '#91cc75'
        },
        barWidth: '90%',
        emphasis: {
          itemStyle: {
            color: '#5fb44d'
          }
        }
      }],
      markLine: {
        symbol: ['none', 'none'],
        label: {
          formatter: '{b}',
          position: 'middle',
          fontSize: 12,
          color: '#666'
        },
        data: [
          {
            name: '平均值',
            xAxis: Math.round(scoreStats.mean),
            lineStyle: { 
              color: '#ee6666',
              width: 2
            }
          },
          {
            name: '中位数',
            xAxis: Math.round(scoreStats.median),
            lineStyle: { 
              color: '#5470c6',
              width: 2
            }
          },
          {
            name: 'Q1',
            xAxis: Math.round(scoreStats.q1),
            lineStyle: { 
              color: '#91cc75',
              type: 'dashed',
              width: 1.5
            }
          },
          {
            name: 'Q3',
            xAxis: Math.round(scoreStats.q3),
            lineStyle: { 
              color: '#91cc75',
              type: 'dashed',
              width: 1.5
            }
          },
          {
            name: '标准差',
            xAxis: Math.round(scoreStats.mean + scoreStats.std),
            lineStyle: { 
              color: '#909399',
              type: 'dashed',
              width: 1.5
            }
          }
        ]
      },
      toolbox: {
        feature: {
          dataZoom: {
            yAxisIndex: 'none'
          },
          restore: {},
          saveAsImage: {}
        },
        right: 10,
        top: 10
      }
    })

    // 相关性热力图
    const corrChart = echarts.init(correlationChart.value)
    const corrData = statsData.correlation_matrix
    const features = Object.keys(corrData)
    const data = []
    features.forEach((row, i) => {
      features.forEach((col, j) => {
        const value = Number(corrData[row][col].toFixed(2))
        data.push([i, j, value])
      })
    })

    corrChart.setOption({
      title: {
        text: '指标相关性',
        left: 'center',
        top: 10,
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      tooltip: {
        position: 'top',
        formatter: (params: any) => {
          const value = params.data[2]
          const sourceName = typeNames[features[params.data[0]]] || features[params.data[0]]
          const targetName = typeNames[features[params.data[1]]] || features[params.data[1]]
          const formattedValue = value > 0 ? `+${value.toFixed(2)}` : value.toFixed(2)
          return `${sourceName} vs ${targetName}<br/>相关系数: ${formattedValue}`
        }
      },
      grid: {
        top: '15%',
        left: '15%',
        right: '5%',
        bottom: '20%'
      },
      xAxis: {
        type: 'category',
        data: features.map(f => typeNames[f] || f),
        axisLabel: {
          rotate: 45,
          interval: 0,
          fontSize: 12
        }
      },
      yAxis: {
        type: 'category',
        data: features.map(f => typeNames[f] || f),
        axisLabel: {
          fontSize: 12
        }
      },
      visualMap: {
        min: -1,
        max: 1,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: '0%',
        text: ['正相关', '负相关'],
        realtime: true,
        inRange: {
          color: [
            '#4575b4',    // 深蓝（强负相关）
            '#74add1',    // 中蓝（中负相关）
            '#abd9e9',    // 浅蓝（弱负相关）
            '#ffffff',    // 白色（无相关）
            '#fee090',    // 浅黄（弱正相关）
            '#f46d43',    // 橙色（中正相关）
            '#d73027'     // 红色（强正相关）
          ]
        }
      },
      series: [{
        name: '相关性',
        type: 'heatmap',
        data: data,
        label: {
          show: true,
          formatter: (params: any) => {
            const value = params.data[2]
            return value > 0 ? `+${value.toFixed(2)}` : value.toFixed(2)
          },
          fontSize: 11
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }]
    })

    // 得分类型箱线图
    const boxplotChart = echarts.init(scoreTypesChart.value)
    const boxData = scoreTypes.map(type => {
      const stats = statsData.score_types_stats[type]
      return {
        name: typeNames[type],
        value: [
          stats['min'],
          stats['25%'],
          stats['50%'],
          stats['75%'],
          stats['max']
        ]
      }
    })

    boxplotChart.setOption({
      title: {
        text: '各类型得分分布',
        left: 'center',
        top: 10,
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      tooltip: {
        trigger: 'item',
        axisPointer: {
          type: 'shadow'
        },
        formatter: function (params: any) {
          if (!params.data || !Array.isArray(params.data.value)) {
            return ''
          }
          const data = params.data.value.map(v => (v || 0).toFixed(2))
          return [
            `${params.data.name}`,
            `最小值: ${data[0]}`,
            `Q1: ${data[1]}`,
            `中位数: ${data[2]}`,
            `Q3: ${data[3]}`,
            `最大值: ${data[4]}`
          ].join('<br/>')
        }
      },
      grid: {
        top: '15%',
        left: '10%',
        right: '10%',
        bottom: '15%'
      },
      xAxis: {
        type: 'category',
        data: boxData.map(item => item.name),
        axisLabel: {
          rotate: 45,
          interval: 0
        },
        boundaryGap: true,
        nameGap: 30,
        splitArea: {
          show: false
        },
        axisLine: {
          show: true
        },
        splitLine: {
          show: false
        }
      },
      yAxis: {
        type: 'value',
        name: '得分',
        splitArea: {
          show: true
        }
      },
      series: [{
        name: '得分分布',
        type: 'boxplot',
        data: boxData.map(item => item.value),
        tooltip: {
          formatter: function (params: any) {
            if (!params.data || !Array.isArray(params.data)) {
              return ''
            }
            const data = params.data.map(v => (v || 0).toFixed(2))
            return [
              `${params.name}`,
              `最小值: ${data[0]}`,
              `Q1: ${data[1]}`,
              `中位数: ${data[2]}`,
              `Q3: ${data[3]}`,
              `最大值: ${data[4]}`
            ].join('<br/>')
          }
        },
        itemStyle: {
          borderWidth: 2,
          borderColor: '#1890ff'
        },
        emphasis: {
          itemStyle: {
            borderWidth: 3,
            borderColor: '#40a9ff'
          }
        }
      }]
    })

    // 得分趋势图
    const trendChartInstance = echarts.init(trendChart.value)
    const timeFormat = statsData.trends.time_format || 'YYYY-MM-DD HH:mm'
    
    // 处理趋势数据
    const validTrendData = generateTrendData(statsData)
    
    trendChartInstance.setOption({
      title: {
        text: '得分趋势',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        formatter: function(params: any) {
          const time = params[0].axisValue
          return [
            `时间: ${dayjs(time).format(timeFormat)}`,
            ...params.map((param: any) => 
              `${param.seriesName}: ${param.value[1]}`
            )
          ].join('<br/>')
        }
      },
      xAxis: {
        type: 'time',
        axisLabel: {
          formatter: function(value: number) {
            return dayjs(value).format(timeFormat)
          }
        },
        splitLine: {
          show: false
        }
      },
      legend: {
        data: ['平均得分', '最高得分', '生成数量'],
        bottom: 10
      },
      grid: {
        top: '15%',
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true
      },
      yAxis: [
        {
          type: 'value',
          name: '得分',
          position: 'left',
          min: 0,
          max: function(value: any) {
            return Math.ceil(value.max * 1.1)
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: '#91cc75'
            }
          },
          axisLabel: {
            color: '#91cc75',
            fontSize: 12
          }
        },
        {
          type: 'value',
          name: '数量',
          position: 'right',
          min: 0,
          max: function(value: any) {
            return Math.ceil(value.max * 1.1)
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: '#5470c6'
            }
          },
          axisLabel: {
            color: '#5470c6',
            fontSize: 12
          }
        }
      ],
      series: [
        {
          name: '平均得分',
          type: 'line',
          smooth: true,
          data: validTrendData.avgScores.map((item: any) => [
            new Date(item.time).getTime(),
            item.value
          ]),
          itemStyle: { color: '#91cc75' },
          emphasis: {
            focus: 'series'
          }
        },
        {
          name: '最高得分',
          type: 'line',
          smooth: true,
          data: validTrendData.maxScores.map((item: any) => [
            new Date(item.time).getTime(),
            item.value
          ]),
          itemStyle: { color: '#ee6666' },
          emphasis: {
            focus: 'series'
          }
        },
        {
          name: '生成数量',
          type: 'bar',
          yAxisIndex: 1,
          data: validTrendData.counts.map((item: any) => [
            new Date(item.time).getTime(),
            item.value
          ]),
          itemStyle: { color: '#5470c6' },
          emphasis: {
            focus: 'series'
          }
        }
      ]
    })

    // 更新统计卡片
    updateSummaryStats(statsData)

    // 更图表列表
    charts = [scoreChart, corrChart, boxplotChart, trendChartInstance]

    // 添加resize监听器
    window.addEventListener('resize', handleResize)

    // 在关键点添加数据检查和日志
    debug.log('Summary Stats:', statsData.summary_stats)
    debug.log('Trends Data:', statsData.trends)
    
    // 数据验证
    if (!statsData.trends?.avg_scores?.length) {
      console.warn('No trend data available')
    }
  } catch (error) {
    console.error('Chart initialization failed:', error)
    message.error('图表初始化失败')
  }
}

const updateSummaryStats = (statsData: any) => {
  debug.log('Updating summary stats:', statsData.summary_stats)
  const stats = statsData.summary_stats.score
  summaryStats.value = [
    {
      title: '平均得分',
      value: stats.mean.toFixed(1),
      trend: stats.mean_trend > 0 ? 'up' : 'down',
      trendValue: `${Math.abs(stats.mean_trend * 100).toFixed(1)}%`
    },
    {
      title: '最高得分',
      value: stats.max.toFixed(1),
      trend: stats.max_trend > 0 ? 'up' : 'down',
      trendValue: `${Math.abs(stats.max_trend * 100).toFixed(1)}%`
    },
    {
      title: '生成数量',
      value: stats.count,
      trend: stats.count_trend > 0 ? 'up' : 'down',
      trendValue: `${Math.abs(stats.count_trend * 100).toFixed(1)}%`
    },
    {
      title: '合格率',
      value: `${(stats.qualified_rate * 100).toFixed(1)}%`,
      trend: stats.qualified_trend > 0 ? 'up' : 'down',
      trendValue: `${Math.abs(stats.qualified_trend * 100).toFixed(1)}%`
    }
  ]
}

const generateTrendData = (statsData: any) => {
  debug.log('Generating trend data:', statsData.trends)
  return {
    avgScores: statsData.trends?.avg_scores || [],
    maxScores: statsData.trends?.max_scores || [],
    counts: statsData.trends?.counts || []
  }
}

// 添加错误边界处理
const handleError = (error: any) => {
  console.error('Component Error:', error)
  message.error('组件发生错误')
}
</script>

<style scoped>
.analysis-container {
  padding: 20px;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin: 24px 0;
}

.chart-wrapper {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.3s ease;
}

.chart-wrapper:hover {
  transform: translateY(-2px);
}

.chart {
  height: 400px;
}

.tables-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.stat-title {
  color: var(--n-text-color-3);
  font-size: 14px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  margin: 10px 0;
  color: var(--n-text-color);
}

.stat-trend {
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-trend.up {
  color: var(--n-success-color);
}

.stat-trend.down {
  color: var(--n-error-color);
}

@media (max-width: 1200px) {
  .charts-container,
  .tables-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  :deep(.n-grid) {
    --n-cols: 1 !important;
  }
}

.filter-container {
  margin-bottom: 24px;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
}
</style> 
