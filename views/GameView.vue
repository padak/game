<template>
  <main class="game-view">
    <h1>Math Crossword</h1>
    <div class="difficulty-selector">
      <button 
        v-for="level in ['easy', 'medium', 'hard']" 
        :key="level"
        @click="selectDifficulty(level)"
        :class="{ active: currentDifficulty === level }"
      >
        {{ level }}
      </button>
    </div>
    <GameGrid />
    <NumberBank />
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import GameGrid from '@/components/game/GameGrid.vue'
import NumberBank from '@/components/game/NumberBank.vue'

const currentDifficulty = ref('medium')

const selectDifficulty = (level: string) => {
  currentDifficulty.value = level
  // TODO: Implement new game generation
}
</script>

<style scoped>
.game-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 20px;
}

.difficulty-selector {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

button {
  padding: 8px 16px;
  border: 2px solid #2c3e50;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  text-transform: capitalize;
}

button.active {
  background: #2c3e50;
  color: white;
}

button:hover {
  background: #34495e;
  color: white;
}
</style> 