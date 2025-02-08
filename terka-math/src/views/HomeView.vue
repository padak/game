<script setup lang="ts">
import GameGrid from '../components/game/GameGrid.vue'
import NumberBank from '../components/game/NumberBank.vue'
</script>

<template>
  <main>
    <div class="game-container">
      <GameGrid />
      <NumberBank />
    </div>
  </main>
</template>

<style scoped>
.game-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
