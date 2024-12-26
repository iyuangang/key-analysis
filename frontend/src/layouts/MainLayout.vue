<script setup lang="ts">
import AppNav from '../components/AppNav.vue'
</script>

<template>
  <div class="layout">
    <header class="header">
      <AppNav />
    </header>
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  position: sticky;
  top: 0;
  z-index: 100;
}

.main {
  flex: 1;
  padding: 24px;
  background-color: #f5f5f5;
}
</style>
