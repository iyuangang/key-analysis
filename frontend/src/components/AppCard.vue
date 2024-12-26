<template>
  <div class="app-card" :class="{ hoverable }">
    <div v-if="$slots.header" class="card-header">
      <slot name="header"></slot>
    </div>
    <div class="card-body">
      <slot></slot>
    </div>
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  hoverable?: boolean
}>()
</script>

<style scoped>
.app-card {
  background: var(--apple-card-bg);
  border: 1px solid var(--apple-border);
  border-radius: 1rem;
  overflow: hidden;
  transition: all 0.2s ease;
}

.app-card.hoverable:hover {
  transform: translateY(-2px);
  box-shadow: var(--apple-shadow);
}

.card-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--apple-border);
  background: var(--apple-bg-secondary);
}

.card-body {
  padding: 1.5rem;
}

.card-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--apple-border);
  background: var(--apple-bg-secondary);
}

@media (max-width: 768px) {

  .card-header,
  .card-footer {
    padding: 0.75rem 1rem;
  }

  .card-body {
    padding: 1rem;
  }
}
</style>
