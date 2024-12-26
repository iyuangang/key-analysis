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
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: saturate(180%) blur(20px);
  border-radius: 14px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.data-table:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 0;
}

h3 {
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  background: linear-gradient(135deg, #1a1a1a 0%, #434343 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}

:deep(.custom-table) {
  --n-th-color: rgba(0, 0, 0, 0.02);
  --n-th-text-color: #86868b;
  --n-td-color: transparent;
  --n-td-text-color: #1d1d1f;
}

:deep(.n-data-table-th) {
  font-size: 13px;
  font-weight: 500;
  letter-spacing: -0.2px;
  padding: 12px !important;
}

:deep(.n-data-table-td) {
  font-size: 14px;
  letter-spacing: -0.2px;
  padding: 12px !important;
}

:deep(.n-button) {
  width: 32px;
  height: 32px;
  border-radius: 16px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.n-button:hover) {
  background-color: rgba(0, 0, 0, 0.06);
}

:deep(.n-button:active) {
  transform: scale(0.92);
}

:deep(.score-value) {
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 6px;
  background-color: rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

:deep(.score-value.high-score) {
  color: #1d9d74;
  background-color: rgba(29, 157, 116, 0.1);
}

@media (max-width: 768px) {
  h3 {
    font-size: 15px;
  }

  :deep(.n-data-table-th) {
    font-size: 12px;
    padding: 8px !important;
  }

  :deep(.n-data-table-td) {
    font-size: 13px;
    padding: 8px !important;
  }

  :deep(.n-button) {
    width: 28px;
    height: 28px;
  }
}
</style> 
