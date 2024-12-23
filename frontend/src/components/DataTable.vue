<template>
  <n-card class="data-table">
    <template #header>
      <h3>{{ title }}</h3>
    </template>
    <n-data-table
      :columns="columns"
      :data="data"
      :bordered="false"
      :single-line="false"
    />
  </n-card>
</template>

<script setup lang="ts">
import { h } from 'vue'
import { NCard, NDataTable, type DataTableColumns } from 'naive-ui'

defineProps({
  title: String,
  data: Array
})

const columns: DataTableColumns = [
  {
    title: '创建时间',
    key: 'created_at'
  },
  {
    title: '指纹',
    key: 'fingerprint'
  },
  {
    title: '得分',
    key: 'score',
    render(row) {
      return h(
        'span',
        {
          style: {
            color: row.score > 400 ? 'var(--n-success-color)' : 'inherit'
          }
        },
        row.score
      )
    }
  },
  {
    title: '唯一字母数',
    key: 'unique_letters_count'
  }
]
</script>

<style scoped>
.data-table {
  background: #fff;
}

h3 {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
}
</style> 
