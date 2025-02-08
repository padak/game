<template>
  <main>
    <div class="game-container">
      <GameGrid />
      <NumberBank />
    </div>
  </main>
</template>

<script setup lang="ts">
import GameGrid from '@/components/game/GameGrid.vue'
import NumberBank from '@/components/game/NumberBank.vue'
</script>

<style scoped>
.game-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
</style> 