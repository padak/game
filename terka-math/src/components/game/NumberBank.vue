<template>
  <div class="number-bank">
    <div 
      v-for="(num, index) in gameStore.availableNumbers"
      :key="`num-${num}-${index}`"
      class="number"
      :class="{ 'selected': gameStore.selectedNumber === num }"
      @click="gameStore.selectNumber(num)"
    >
      {{ num }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { useGameStore } from '@/stores/game'

const gameStore = useGameStore()
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