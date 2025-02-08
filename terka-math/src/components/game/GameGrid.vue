<template>
  <div class="game-grid">
    <div class="grid">
      <div v-for="(row, rowIndex) in gameStore.grid" :key="rowIndex" class="row">
        <div 
          v-for="(cell, colIndex) in row" 
          :key="colIndex"
          class="cell"
          :class="{
            'is-operator': cell.isOperator,
            'is-result': cell.isResult,
            'is-fixed': cell.isFixed,
            'is-empty': cell.value === null && !cell.isOperator,
            'is-correct': cell.isCorrect
          }"
          @click="handleCellClick(rowIndex, colIndex)"
        >
          {{ cell.isOperator ? cell.operator : cell.value }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useGameStore } from '@/stores/game'

const gameStore = useGameStore()

onMounted(() => {
  gameStore.initializeGame()
})

const handleCellClick = (row: number, col: number) => {
  const cell = gameStore.grid[row][col]
  if (cell.isFixed || cell.isOperator) return
  
  if (cell.value === null) {
    gameStore.placeNumber(row, col)
  } else {
    gameStore.clearCell(row, col)
  }
}
</script>

<style scoped>
.game-grid {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.grid {
  display: flex;
  flex-direction: column;
  gap: 2px;
  background: #ccc;
  padding: 2px;
  border-radius: 8px;
}

.row {
  display: flex;
  gap: 2px;
}

.cell {
  width: 40px;
  height: 40px;
  background: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2em;
  cursor: pointer;
  user-select: none;
  transition: all 0.2s;
}

.cell:hover {
  background: #f0f0f0;
}

.cell.is-operator {
  background: #e0e0e0;
  font-weight: bold;
}

.cell.is-result {
  background: #f0f0f0;
}

.cell.is-fixed {
  color: #2c3e50;
  font-weight: bold;
}

.cell.is-empty {
  color: #666;
}

.cell.is-correct {
  background: #e8f5e9;
  color: #2e7d32;
}

.cell.is-correct.is-operator {
  background: #c8e6c9;
}
</style> 