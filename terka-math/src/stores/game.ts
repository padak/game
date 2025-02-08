import { defineStore } from 'pinia'
import { apiService, type Cell, type GameState } from '@/services/api'

interface State {
  grid: Cell[][]
  availableNumbers: number[]
  selectedNumber: number | null
  difficulty: 'easy' | 'medium' | 'hard'
  gridSize: number
  loading: boolean
  error: string | null
}

export const useGameStore = defineStore('game', {
  state: (): State => ({
    grid: [],
    availableNumbers: [],
    selectedNumber: null,
    difficulty: 'medium',
    gridSize: 8,
    loading: true,
    error: null
  }),

  getters: {
    isGameComplete: (state) => {
      if (!state.grid || state.grid.length === 0) return false;
      return state.grid.every(row => 
        row.every(cell => 
          cell?.isFixed || cell?.isOperator || cell?.isCorrect || cell?.value === null
        )
      )
    }
  },

  actions: {
    async initializeGame(difficulty: 'easy' | 'medium' | 'hard' = 'medium') {
      console.log('Initializing game with difficulty:', difficulty)
      this.loading = true
      this.error = null
      try {
        const gameState = await apiService.startNewGame(difficulty)
        console.log('Received game state in store:', gameState)
        this.updateGameState(gameState)
      } catch (error) {
        console.error('Error initializing game in store:', error)
        this.error = error instanceof Error ? error.message : 'Failed to start game'
        console.error('Failed to initialize game:', error)
      } finally {
        this.loading = false
        console.log('Game initialization complete. Grid:', this.grid)
      }
    },

    updateGameState(gameState: GameState) {
      console.log('Updating game state with:', gameState)
      this.grid = gameState.grid
      this.availableNumbers = gameState.numberBank
      this.difficulty = gameState.difficulty
      this.gridSize = this.grid.length
      console.log('State updated. Grid size:', this.gridSize)
    },

    selectNumber(num: number | null) {
      this.selectedNumber = num
    },

    async placeNumber(row: number, col: number) {
      if (this.selectedNumber === null) return
      
      this.loading = true
      this.error = null
      try {
        const result = await apiService.validateMove(row, col, this.selectedNumber)
        if (result.valid && result.grid && result.numberBank) {
          this.grid = result.grid
          this.availableNumbers = result.numberBank
          this.selectedNumber = null
        }
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to place number'
        console.error('Failed to place number:', error)
      } finally {
        this.loading = false
      }
    },

    async clearCell(row: number, col: number) {
      this.loading = true
      this.error = null
      try {
        const result = await apiService.clearCell(row, col)
        if (result.valid && result.grid && result.numberBank) {
          this.grid = result.grid
          this.availableNumbers = result.numberBank
        }
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Failed to clear cell'
        console.error('Failed to clear cell:', error)
      } finally {
        this.loading = false
      }
    }
  }
}) 