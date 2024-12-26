<script setup lang="ts">
import { NCard, NSpace, NH1, NText, NDivider } from 'naive-ui'

const features = [
  {
    title: '密钥分析',
    description: '分析密钥的重复字母、递增序列、递减序列和特殊组合'
  },
  {
    title: '实时评分',
    description: '对密钥进行综合评分，阈值400分为高分密钥'
  },
  {
    title: '数据可视化',
    description: '直观展示密钥分析结果和统计数据'
  }
]
</script>

<template>
  <div class="about-container">
    <NSpace vertical size="large">
      <NH1>关于密钥分析系统</NH1>

      <NCard>
        <NText>
          密钥分析系统是一个专业的密钥质量评估平台，通过多维度分析帮助用户评估和优化密钥质量。
          系统采用先进的评分算法，从重复字母、字母序列、特殊组合等多个维度进行分析。
        </NText>
      </NCard>

      <NDivider>核心功能</NDivider>

      <NSpace>
        <NCard v-for="feature in features" :key="feature.title" style="width: 300px">
          <template #header>
            <strong>{{ feature.title }}</strong>
          </template>
          {{ feature.description }}
        </NCard>
      </NSpace>
    </NSpace>
  </div>
</template>

<style scoped>
.about-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>
