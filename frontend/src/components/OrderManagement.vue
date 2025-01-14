<template>
  <div class="order-management">
    <n-card>
      <n-tabs type="line" animated>
        <n-tab-pane name="mask" tab="数据屏蔽">
          <n-form ref="maskFormRef" :model="maskForm" :rules="maskRules">
            <n-form-item label="查询条件" path="searchType">
              <n-radio-group v-model:value="maskForm.searchType">
                <n-radio-button value="orderId">订单编号</n-radio-button>
                <n-radio-button value="productId">商品识别号</n-radio-button>
              </n-radio-group>
            </n-form-item>
            <n-form-item label="ID列表" path="ids">
              <n-input v-model:value="maskForm.ids" type="textarea" placeholder="请输入ID，多个ID请用换行分隔" />
            </n-form-item>
            <n-space justify="end">
              <n-button type="primary" @click="handleMask" :loading="loading">
                确认屏蔽
              </n-button>
            </n-space>
          </n-form>
        </n-tab-pane>

        <n-tab-pane name="modify" tab="数据修改">
          <n-form ref="modifyFormRef" :model="modifyForm" :rules="modifyRules">
            <n-form-item label="查询条件" path="searchType">
              <n-radio-group v-model:value="modifyForm.searchType">
                <n-radio-button value="orderId">订单编号</n-radio-button>
                <n-radio-button value="productId">商品识别号</n-radio-button>
              </n-radio-group>
            </n-form-item>
            <n-form-item label="ID" path="id">
              <n-input v-model:value="modifyForm.id" placeholder="请输入ID" />
            </n-form-item>
            <n-form-item label="订单金额" path="amount">
              <n-input-number v-model:value="modifyForm.amount" placeholder="请输入新的订单金额" />
            </n-form-item>
            <n-form-item label="客户名称" path="customerName">
              <n-input v-model:value="modifyForm.customerName" placeholder="请输入新的客户名称" />
            </n-form-item>
            <n-form-item label="客户ID" path="customerId">
              <n-input v-model:value="modifyForm.customerId" placeholder="请输入新的客户ID" />
            </n-form-item>
            <n-form-item label="证件类型" path="idType">
              <n-select v-model:value="modifyForm.idType" :options="idTypeOptions" />
            </n-form-item>
            <n-space justify="end">
              <n-button type="primary" @click="handleModify" :loading="loading">
                确认修改
              </n-button>
            </n-space>
          </n-form>
        </n-tab-pane>
      </n-tabs>
    </n-card>

    <n-modal v-model:show="showResult" title="操作结果" preset="card">
      <n-descriptions bordered>
        <n-descriptions-item v-for="(value, key) in operationResult" :key="key" :label="key">
          {{ value }}
        </n-descriptions-item>
      </n-descriptions>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showResult = false">关闭</n-button>
          <n-button type="primary" @click="handleExport">导出结果</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import {
  NCard,
  NTabs,
  NTabPane,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NButton,
  NRadioGroup,
  NRadioButton,
  NSpace,
  NSelect,
  NModal,
  NDescriptions,
  NDescriptionsItem,
  useMessage,
  type FormInst,
  type FormRules
} from 'naive-ui'
import { maskOrders, modifyOrder } from '../services/api'

interface OperationResult {
  success: boolean
  message: string
  affectedRows: number
  details?: Record<string, unknown>
}

const message = useMessage()
const loading = ref(false)
const showResult = ref(false)
const operationResult = ref<OperationResult | null>(null)

const maskFormRef = ref<FormInst | null>(null)
const modifyFormRef = ref<FormInst | null>(null)

const maskForm = reactive({
  searchType: 'orderId' as const,
  ids: ''
})

const modifyForm = reactive({
  searchType: 'orderId' as const,
  id: '',
  amount: undefined as number | undefined,
  customerName: '',
  customerId: '',
  idType: undefined as string | undefined
})

const idTypeOptions = [
  { label: '身份证', value: 'ID_CARD' },
  { label: '护照', value: 'PASSPORT' },
  { label: '其他', value: 'OTHER' }
]

const maskRules: FormRules = {
  ids: {
    required: true,
    message: '请输入ID',
    trigger: 'blur'
  }
}

const modifyRules: FormRules = {
  id: {
    required: true,
    message: '请输入ID',
    trigger: 'blur'
  }
}

const handleMask = async () => {
  try {
    await maskFormRef.value?.validate()
    loading.value = true
    const ids = maskForm.ids.split('\n').filter(id => id.trim())
    if (ids.length === 0) {
      message.warning('请至少输入一个有效的ID')
      return
    }
    const result = await maskOrders({
      type: maskForm.searchType,
      ids
    })
    operationResult.value = result
    showResult.value = true
    message.success('屏蔽操作成功')
  } catch (error: unknown) {
    const err = error instanceof Error ? error : new Error(String(error))
    message.error('操作失败：' + err.message)
  } finally {
    loading.value = false
  }
}

const handleModify = async () => {
  try {
    await modifyFormRef.value?.validate()
    loading.value = true

    // Check if at least one field is modified
    const changes = {
      amount: modifyForm.amount,
      customerName: modifyForm.customerName,
      customerId: modifyForm.customerId,
      idType: modifyForm.idType
    }

    if (Object.values(changes).every(v => v === undefined)) {
      message.warning('请至少修改一个字段')
      return
    }

    const result = await modifyOrder({
      type: modifyForm.searchType,
      id: modifyForm.id,
      changes
    })
    operationResult.value = result
    showResult.value = true
    message.success('修改操作成功')
  } catch (error: unknown) {
    const err = error instanceof Error ? error : new Error(String(error))
    message.error('操作失败：' + err.message)
  } finally {
    loading.value = false
  }
}

const handleExport = () => {
  if (!operationResult.value) return
  const data = JSON.stringify(operationResult.value, null, 2)
  const blob = new Blob([data], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `operation-result-${Date.now()}.toString()`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.order-management {
  padding: 16px;
}
</style>
