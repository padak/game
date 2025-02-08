<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <h1>Math Crossword</h1>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.wrapper {
  text-align: center;
  padding: 2rem;
}

h1 {
  font-size: 2.5rem;
  color: #2c3e50;
}
</style>
