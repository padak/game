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
            'is-operator': cell.isOperator,
            'is-result': cell.isResult,
            'is-fixed': cell.isFixed,
            'is-empty': cell.isEmpty,
            'is-correct': cell.isCorrect,
            'is-incorrect': cell.isIncorrect,
            'equation-cell': cell.inEquation,
            'interactive': !cell.isOperator && !cell.isFixed && cell.inEquation,
            'selected': isSelected(rowIndex, colIndex)
          }"
          @click="handleCellClick(rowIndex, colIndex)"
        >
          {{ cell.isOperator ? cell.operator : cell.value }}
        </div>
      </div>
    </div>

    <div class="controls">
      <button 
        v-for="level in ['easy', 'medium', 'hard'] as const" 
        :key="level"
        :class="{ active: gameStore.difficulty === level }"
        @click="gameStore.initializeGame(level)"
      >
        {{ level.toUpperCase() }}
      </button>
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
  padding: 2rem;
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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
  user-select: none;
  transition: all 0.2s ease;
}

.cell.equation-cell {
  border: 2px solid #1976d2;
}

.cell.interactive {
  cursor: pointer;
}

.cell.interactive:hover {
  background: #f5f5f5;
  transform: scale(1.05);
}

.cell.is-operator {
  background: #e3f2fd;
  font-weight: bold;
  color: #1976d2;
}

.cell.is-result {
  background: #e8f5e9;
  color: #2e7d32;
}

.cell.is-fixed {
  background: #f5f5f5;
  color: #424242;
  font-weight: bold;
}

.cell.is-empty {
  color: #9e9e9e;
}

.cell.is-correct {
  background: #e8f5e9;
  color: #2e7d32;
}

.cell.is-incorrect {
  background: #ffebee;
  color: #c62828;
}

.cell.selected {
  transform: scale(1.05);
  box-shadow: 0 0 0 2px #1976d2;
}

.controls {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.controls button {
  padding: 0.5rem 1rem;
  border: 2px solid #1a73e8;
  border-radius: 4px;
  background: white;
  color: #1a73e8;
  cursor: pointer;
  transition: all 0.2s;
  text-transform: capitalize;
  font-weight: bold;
}

.controls button:hover {
  background: #e8f0fe;
  transform: translateY(-2px);
}

.controls button.active {
  background: #1a73e8;
  color: white;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style> 