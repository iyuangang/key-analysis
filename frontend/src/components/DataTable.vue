<template>
  <n-card class="data-table">
    <template #header>
      <div class="table-header">
        <h3>{{ title }}</h3>
        <n-space>
          <n-button quaternary circle size="small">
            <template #icon>
              <n-icon><reload-outlined /></n-icon>
            </template>
          </n-button>
          <n-button quaternary circle size="small">
            <template #icon>
              <n-icon><more-outlined /></n-icon>
            </template>
          </n-button>
        </n-space>
      </div>
    </template>
    <n-data-table :columns="isMobile ? mobileColumns : columns" :data="data" :bordered="false" :single-line="false"
      :empty-text="data?.length ? '暂无数据' : '加载中...'" :pagination="pagination" size="small" class="custom-table"
      :row-props="rowProps" />
  </n-card>
</template>

<script setup lang="ts">
import { h, ref, onMounted, onUnmounted } from 'vue'
import { NCard, NDataTable, NButton, NSpace, NIcon, type DataTableColumns } from 'naive-ui'
import {
  ReloadOutlined,
  MoreOutlined
} from '@vicons/antd'

interface TableRow {
  created_at: string
  fingerprint: string
  score: number
  unique_letters_count: number
}

defineProps<{
  title?: string
  data?: TableRow[]
}>()

const isMobile = ref(false)

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

const pagination = {
  pageSize: 5,
  showSizePicker: false,
  showQuickJumper: false
}

const formatFingerprint = (fp: string) => {
  return fp.match(/.{1,4}/g)?.join(' ') || fp
}

const VerifiedIcon = () => h('svg', {
  viewBox: '0 0 16 16',
  width: '16',
  height: '16',
  fill: 'currentColor',
  style: {
    display: 'inline-block',
    userSelect: 'none',
    verticalAlign: 'text-bottom',
    overflow: 'visible'
  }
}, [
  h('path', {
    d: 'm9.585.52.929.68c.153.112.331.186.518.215l1.138.175a2.678 2.678 0 0 1 2.24 2.24l.174 1.139c.029.187.103.365.215.518l.68.928a2.677 2.677 0 0 1 0 3.17l-.68.928a1.174 1.174 0 0 0-.215.518l-.175 1.138a2.678 2.678 0 0 1-2.241 2.241l-1.138.175a1.17 1.17 0 0 0-.518.215l-.928.68a2.677 2.677 0 0 1-3.17 0l-.928-.68a1.174 1.174 0 0 0-.518-.215L3.83 14.41a2.678 2.678 0 0 1-2.24-2.24l-.175-1.138a1.17 1.17 0 0 0-.215-.518l-.68-.928a2.677 2.677 0 0 1 0-3.17l.68-.928c.112-.153.186-.331.215-.518l.175-1.14a2.678 2.678 0 0 1 2.24-2.24l1.139-.175c.187-.029.365-.103.518-.215l.928-.68a2.677 2.677 0 0 1 3.17 0ZM7.303 1.728l-.927.68a2.67 2.67 0 0 1-1.18.489l-1.137.174a1.179 1.179 0 0 0-.987.987l-.174 1.136a2.677 2.677 0 0 1-.489 1.18l-.68.928a1.18 1.18 0 0 0 0 1.394l.68.927c.256.348.424.753.489 1.18l.174 1.137c.078.509.478.909.987.987l1.136.174a2.67 2.67 0 0 1 1.18.489l.928.68c.414.305.979.305 1.394 0l.927-.68a2.67 2.67 0 0 1 1.18-.489l1.137-.174a1.18 1.18 0 0 0 .987-.987l.174-1.136a2.67 2.67 0 0 1 .489-1.18l.68-.928a1.176 1.176 0 0 0 0-1.394l-.68-.927a2.686 2.686 0 0 1-.489-1.18l-.174-1.137a1.179 1.179 0 0 0-.987-.987l-1.136-.174a2.677 2.677 0 0 1-1.18-.489l-.928-.68a1.176 1.176 0 0 0-1.394 0ZM11.28 6.78l-3.75 3.75a.75.75 0 0 1-1.06 0L4.72 8.78a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L7 8.94l3.22-3.22a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042Z'
  })
])

const columns: DataTableColumns<TableRow> = [
  {
    title: '创建时间',
    key: 'created_at',
    width: 160,
    render(row: TableRow) {
      return h('span', {
        class: 'date-cell'
      }, row.created_at)
    }
  },
  {
    title: '指纹',
    key: 'fingerprint',
    width: 300,
    render(row: TableRow) {
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
      return h('div', {
        style: {
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          height: '24px',
          margin: '0',
          padding: '0'
        }
      }, [
        h('div', {
          style: {
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '16px',
            height: '16px',
            color: isDark ? '#3fb950' : '#1a7f37',
            transition: 'color 0.2s'
          }
        }, [
          h(VerifiedIcon)
        ]),
        h('code', {
          style: {
            display: 'inline-block',
            fontFamily: 'ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace',
            fontSize: 'var(--apple-font-base)',
            color: isDark ? '#e6edf3' : '#24292f',
            letterSpacing: '0.3px',
            background: isDark ? '#30363d' : '#f6f8fa',
            padding: '0.2em 0.4em',
            borderRadius: '6px',
            transition: 'background-color 0.2s',
            lineHeight: '20px',
            whiteSpace: 'nowrap',
            verticalAlign: 'middle'
          }
        }, formatFingerprint(row.fingerprint))
      ])
    }
  },
  {
    title: '得分',
    key: 'score',
    width: 100,
    render(row: TableRow) {
      const score = Number(row.score)
      return h(
        'span',
        {
          class: ['score-value', score > 400 ? 'high-score' : score > 200 ? 'medium-score' : 'low-score']
        },
        score
      )
    }
  },
  {
    title: '唯一字母数',
    key: 'unique_letters_count',
    width: 120,
    render(row: TableRow) {
      return h('span', {
        class: 'letters-count'
      }, row.unique_letters_count)
    }
  }
] as const

const mobileColumns: DataTableColumns<TableRow> = [
  {
    title: '指纹',
    key: 'fingerprint',
    width: 180,
    render(row: TableRow) {
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
      return h('div', {
        style: {
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          height: '24px',
          margin: '0',
          padding: '0'
        }
      }, [
        h('div', {
          style: {
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '16px',
            height: '16px',
            color: isDark ? '#3fb950' : '#1a7f37',
            transition: 'color 0.2s'
          }
        }, [
          h(VerifiedIcon)
        ]),
        h('code', {
          style: {
            display: 'inline-block',
            fontFamily: 'ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace',
            fontSize: 'var(--apple-font-base)',
            color: isDark ? '#e6edf3' : '#24292f',
            letterSpacing: '0.3px',
            background: isDark ? '#30363d' : '#f6f8fa',
            padding: '0.2em 0.4em',
            borderRadius: '6px',
            transition: 'background-color 0.2s',
            lineHeight: '20px',
            whiteSpace: 'nowrap',
            verticalAlign: 'middle'
          }
        }, formatFingerprint(row.fingerprint))
      ])
    }
  },
  {
    title: '得分',
    key: 'score',
    width: 80,
    render(row: TableRow) {
      const score = Number(row.score)
      return h(
        'span',
        {
          class: ['score-value', score > 400 ? 'high-score' : score > 200 ? 'medium-score' : 'low-score']
        },
        score
      )
    }
  }
] as const

const rowProps = () => {
  return {
    style: 'height: 40px;'
  }
}

defineExpose({
  columns,
  mobileColumns
})
</script>

<style scoped>
.data-table {
  background: var(--apple-card-bg);
  backdrop-filter: var(--apple-blur-effect);
  border-radius: var(--apple-radius-lg);
  border: 1px solid var(--apple-border-color);
  transition: var(--apple-transition);
  overflow: hidden;
}

.data-table:hover {
  transform: translateY(-2px);
  box-shadow: var(--apple-shadow);
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--apple-spacing-xs) var(--apple-spacing-sm);
}

h3 {
  margin: 0;
  font-size: var(--apple-font-lg);
  font-weight: 600;
  background: var(--apple-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}

:deep(.custom-table) {
  --n-th-color: rgba(0, 0, 0, 0.02);
  --n-th-text-color: var(--apple-text-secondary);
  --n-td-color: transparent;
  --n-td-text-color: var(--apple-text-primary);
  --n-border-color: var(--apple-border-color);
}

:deep(.n-data-table-th) {
  font-size: var(--apple-font-sm);
  font-weight: 600;
  letter-spacing: -0.2px;
  padding: var(--apple-spacing-sm) !important;
  background: rgba(0, 0, 0, 0.02);
  border-bottom: 2px solid var(--apple-border-color) !important;
}

:deep(.n-data-table-td) {
  padding: 8px var(--apple-spacing-sm) !important;
  line-height: 20px !important;
  height: 40px !important;
  vertical-align: middle !important;
}

:deep(.n-data-table tr:hover td) {
  background-color: rgba(0, 0, 0, 0.02) !important;
}

:deep(.n-button) {
  width: 32px;
  height: 32px;
  border-radius: var(--apple-radius-full);
  transition: var(--apple-transition);
}

:deep(.n-button:hover) {
  background-color: rgba(0, 0, 0, 0.06);
}

:deep(.n-button:active) {
  transform: scale(0.92);
}

.date-cell {
  color: var(--apple-text-secondary);
  font-size: var(--apple-font-sm);
}

.fingerprint-cell {
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px;
  height: 24px;
  padding: 0;
  margin: 0;
  vertical-align: middle;
}

.icon-wrapper {
  width: 16px;
  height: 16px;
  color: #1a7f37;
  transition: var(--apple-transition);
}

.fingerprint-code {
  font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
  font-size: var(--apple-font-base);
  color: #24292f;
  letter-spacing: 0.3px;
  background: #f6f8fa;
  padding: 0.2em 0.4em;
  border-radius: 6px;
  transition: background-color 0.2s;
  line-height: 20px;
  white-space: nowrap;
}

:root[data-theme="dark"] {
  .fingerprint-code {
    color: #e6edf3;
    background: #30363d;
  }

  .icon-wrapper {
    color: #3fb950;
  }
}

.fingerprint-cell:hover {
  .icon-wrapper {
    color: #1f682d;
  }

  .fingerprint-code {
    background: #eaeef2;
  }
}

:root[data-theme="dark"] .fingerprint-cell:hover {
  .icon-wrapper {
    color: #57ca67;
  }

  .fingerprint-code {
    background: #2d333b;
  }
}

:deep(.score-value) {
  font-weight: 500;
  padding: var(--apple-spacing-xs) var(--apple-spacing-sm);
  border-radius: var(--apple-radius-sm);
  font-size: var(--apple-font-sm);
  transition: var(--apple-transition);
}

:deep(.score-value.high-score) {
  color: #1d9d74;
  background-color: rgba(29, 157, 116, 0.1);
}

:deep(.score-value.medium-score) {
  color: #d97706;
  background-color: rgba(217, 119, 6, 0.1);
}

:deep(.score-value.low-score) {
  color: #dc2626;
  background-color: rgba(220, 38, 38, 0.1);
}

.letters-count {
  font-family: var(--apple-font-mono);
  font-size: var(--apple-font-sm);
  color: var(--apple-text-secondary);
  padding: var(--apple-spacing-xs) var(--apple-spacing-sm);
  background-color: rgba(0, 0, 0, 0.03);
  border-radius: var(--apple-radius-sm);
}

@media (max-width: 768px) {
  h3 {
    font-size: var(--apple-font-md);
  }

  :deep(.n-data-table-th) {
    font-size: var(--apple-font-xs);
    padding: var(--apple-spacing-xs) !important;
  }

  :deep(.n-data-table-td) {
    font-size: var(--apple-font-sm);
    padding: var(--apple-spacing-xs) !important;
  }

  :deep(.n-button) {
    width: 28px;
    height: 28px;
  }

  .fingerprint-code {
    font-size: var(--apple-font-sm);
  }
}

:deep(.n-data-table-td--last) {
  .fingerprint-cell {
    justify-content: flex-start;
  }
}
</style>
