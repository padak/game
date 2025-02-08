<template>
  <div class="game-grid">
    <div v-if="gameStore.loading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>Loading...</p>
    </div>

    <div v-if="gameStore.error" class="error-message">
      {{ gameStore.error }}
      <button @click="gameStore.initializeGame()">Try Again</button>
    </div>

    <div v-if="gameStore.grid && gameStore.grid.length > 0" class="grid" :class="{ 'loading': gameStore.loading }">
      <div v-for="(row, rowIndex) in gameStore.grid" :key="rowIndex" class="row">
        <div
          v-for="(cell, colIndex) in row"
          :key="colIndex"
          class="cell"
          :class="{
            'operator': cell?.isOperator,
            'fixed': cell?.isFixed,
            'result': cell?.isResult,
            'correct': cell?.isCorrect,
            'incorrect': cell?.isIncorrect,
            'selected': isSelected(rowIndex, colIndex),
            'empty': cell?.isEmpty
          }"
          @click="handleCellClick(rowIndex, colIndex)"
        >
          <template v-if="cell?.isOperator">
            {{ cell.operator }}
          </template>
          <template v-else>
            {{ cell?.value || cell?.operator || '' }}
          </template>
        </div>
      </div>
    </div>

    <div class="controls">
      <button @click="() => gameStore.initializeGame('easy')">Easy</button>
      <button @click="() => gameStore.initializeGame('medium')">Medium</button>
      <button @click="() => gameStore.initializeGame('hard')">Hard</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useGameStore } from '@/stores/game'
import { onMounted } from 'vue'

const gameStore = useGameStore()

onMounted(() => {
  gameStore.initializeGame()
})

function handleCellClick(row: number, col: number) {
  const cell = gameStore.grid[row][col]
  if (!cell || cell.isOperator || cell.isFixed) return

  if (cell.value === null) {
    if (gameStore.selectedNumber !== null) {
      gameStore.placeNumber(row, col)
    }
  } else {
    gameStore.clearCell(row, col)
  }
}

function isSelected(row: number, col: number): boolean {
  const cell = gameStore.grid[row][col]
  return cell && !cell.isOperator && !cell.isFixed && cell.value === gameStore.selectedNumber
}
</script>

<style scoped>
.game-grid {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-message {
  background: #ffebee;
  color: #c62828;
  padding: 1rem;
  margin: 1rem;
  border-radius: 4px;
  text-align: center;
}

.error-message button {
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  background: #c62828;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.grid {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 1rem;
  background: #f0f0f0;
  border-radius: 8px;
}

.grid.loading {
  opacity: 0.5;
  pointer-events: none;
}

.row {
  display: flex;
  gap: 2px;
}

.cell {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 1px solid #ddd;
  font-size: 1.2rem;
  cursor: pointer;
  user-select: none;
}

.cell:hover {
  background: #f0f0f0;
}

.cell.operator {
  background: #e0e0e0;
  font-weight: bold;
}

.cell.result {
  background: #e8f0fe;
}

.cell.fixed {
  color: #2c3e50;
  font-weight: bold;
}

.cell.correct {
  background: #e8f5e9;
  color: #2e7d32;
}

.cell.correct.operator {
  background: #c8e6c9;
}

.cell.incorrect {
  background: #ffebee;
  color: #c62828;
}

.cell.incorrect.operator {
  background: #ffcdd2;
}

.cell.selected {
  border-color: #1a73e8;
  border-width: 2px;
}

.cell.empty {
  background: #fff3cd;  /* Light yellow background for empty cells */
  cursor: pointer;
}

.controls {
  display: flex;
  gap: 1rem;
}

.controls button {
  padding: 0.5rem 1rem;
  border: 1px solid #1a73e8;
  border-radius: 4px;
  background: white;
  color: #1a73e8;
  cursor: pointer;
  transition: all 0.2s;
}

.controls button:hover {
  background: #e8f0fe;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style> 