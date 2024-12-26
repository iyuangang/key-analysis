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
    <n-data-table
      :columns="isMobile ? mobileColumns : columns"
      :data="data"
      :bordered="false"
      :single-line="false"
      :empty-text="data?.length ? '暂无数据' : '加载中...'"
      :pagination="pagination"
      size="small"
      class="custom-table"
    />
  </n-card>
</template>

<script setup lang="ts">
import { h, ref, onMounted, onUnmounted } from 'vue'
import { NCard, NDataTable, NButton, NSpace, NIcon, type DataTableColumns } from 'naive-ui'
import { 
  ReloadOutlined,
  MoreOutlined
} from '@vicons/antd'

defineProps({
  title: String,
  data: Array
})

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

const columns: DataTableColumns = [
  {
    title: '创建时间',
    key: 'created_at',
    width: 160
  },
  {
    title: '指纹',
    key: 'fingerprint',
    width: 180,
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: '得分',
    key: 'score',
    width: 100,
    render(row) {
      const score = Number(row.score)
      return h(
        'span',
        {
          class: ['score-value', score > 400 ? 'high-score' : '']
        },
        score
      )
    }
  },
  {
    title: '唯一字母数',
    key: 'unique_letters_count',
    width: 120
  }
]

const mobileColumns: DataTableColumns = [
  {
    title: '指纹',
    key: 'fingerprint',
    width: 120,
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: '得分',
    key: 'score',
    width: 80,
    render(row) {
      const score = Number(row.score)
      return h(
        'span',
        {
          class: ['score-value', score > 400 ? 'high-score' : '']
        },
        score
      )
    }
  }
]
</script>

<style scoped>
.data-table {
  background: var(--apple-card-bg);
  backdrop-filter: var(--apple-blur-effect);
  border-radius: var(--apple-radius-lg);
  border: 1px solid var(--apple-border-color);
  transition: var(--apple-transition);
}

.data-table:hover {
  transform: translateY(-2px);
  box-shadow: var(--apple-shadow);
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--apple-spacing-xs) 0;
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
}

:deep(.n-data-table-th) {
  font-size: var(--apple-font-sm);
  font-weight: 500;
  letter-spacing: -0.2px;
  padding: var(--apple-spacing-sm) !important;
}

:deep(.n-data-table-td) {
  font-size: var(--apple-font-base);
  letter-spacing: -0.2px;
  padding: var(--apple-spacing-sm) !important;
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

:deep(.score-value) {
  font-weight: 500;
  padding: var(--apple-spacing-xs) var(--apple-spacing-sm);
  border-radius: var(--apple-radius-sm);
  background-color: rgba(0, 0, 0, 0.05);
  transition: var(--apple-transition);
}

:deep(.score-value.high-score) {
  color: #1d9d74;
  background-color: rgba(29, 157, 116, 0.1);
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
}
</style> 
