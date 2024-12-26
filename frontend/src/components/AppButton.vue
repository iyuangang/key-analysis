<template>
  <button class="app-button" :class="{
    'btn-primary': type === 'primary',
    'btn-secondary': type === 'secondary',
    'btn-danger': type === 'danger',
    'btn-text': type === 'text',
    'btn-icon': icon && !$slots.default,
    'btn-loading': loading,
    'btn-block': block,
    'btn-small': size === 'small',
    'btn-large': size === 'large',
  }" :disabled="disabled || loading" v-bind="$attrs">
    <div v-if="loading" class="i-mdi:loading btn-spinner" />
    <div v-else-if="icon" :class="icon" />
    <span v-if="$slots.default" class="btn-content">
      <slot></slot>
    </span>
  </button>
</template>

<script setup lang="ts">
interface Props {
  type?: 'primary' | 'secondary' | 'danger' | 'text'
  size?: 'small' | 'normal' | 'large'
  icon?: string
  loading?: boolean
  disabled?: boolean
  block?: boolean
}

withDefaults(defineProps<Props>(), {
  type: 'secondary',
  size: 'normal',
  loading: false,
  disabled: false,
  block: false,
})
</script>

<style scoped>
.app-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  line-height: 1.5;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  background: transparent;
  color: var(--apple-text-primary);
}

.app-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.app-button:active:not(:disabled) {
  transform: scale(0.98);
}

/* Primary Button */
.btn-primary {
  background: var(--apple-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--apple-primary-dark);
}

/* Secondary Button */
.btn-secondary {
  background: var(--apple-bg-secondary);
  border-color: var(--apple-border);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--apple-hover-bg);
}

/* Danger Button */
.btn-danger {
  background: var(--apple-red);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: var(--apple-red-dark);
}

/* Text Button */
.btn-text {
  padding: 0.5rem;
}

.btn-text:hover:not(:disabled) {
  background: var(--apple-hover-bg);
}

/* Icon Button */
.btn-icon {
  padding: 0.5rem;
  border-radius: 0.375rem;
}

/* Block Button */
.btn-block {
  width: 100%;
}

/* Size Variants */
.btn-small {
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
}

.btn-small.btn-icon {
  padding: 0.25rem;
}

.btn-large {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}

.btn-large.btn-icon {
  padding: 0.75rem;
}

/* Loading State */
.btn-loading {
  position: relative;
  pointer-events: none;
}

.btn-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

/* Dark Mode Adjustments */
:root[data-theme="dark"] .btn-secondary {
  background: var(--apple-bg-secondary-dark);
}
</style>
