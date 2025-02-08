<template>
  <div class="number-bank">
    <div 
      v-for="(number, index) in gameStore.availableNumbers" 
      :key="`${number}-${index}`"
      class="number"
      :class="{ 'selected': gameStore.selectedNumber === number }"
      @click="handleNumberClick(number)"
    >
      {{ number }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { useGameStore } from '@/stores/game'

const gameStore = useGameStore()

const handleNumberClick = (number: number) => {
  if (gameStore.selectedNumber === number) {
    gameStore.selectNumber(null)
  } else {
    gameStore.selectNumber(number)
  }
}
</script>

<style scoped>
.number-bank {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  padding: 20px;
  background: white;
  border: 2px solid #ccc;
  border-radius: 8px;
  margin: 20px;
  flex-wrap: wrap;
  max-width: 400px;
}

.number {
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2em;
  background: #f0f0f0;
  border-radius: 4px;
  cursor: pointer;
  user-select: none;
  transition: all 0.2s;
}

.number:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}

.number.selected {
  background: #2c3e50;
  color: white;
  transform: translateY(-2px);
}
</style> 