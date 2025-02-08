import { defineStore } from 'pinia'

interface Cell {
  row: number
  col: number
  value: number | null
  type: 'operand' | 'operator' | 'result'
  prefilled: boolean
}

interface GameState {
  grid: Cell[][]
  numberBank: number[]
  difficulty: 'easy' | 'medium' | 'hard'
  selectedNumber: number | null
}

export const useGameStore = defineStore('game', {
  state: (): GameState => ({
    grid: [],
    numberBank: [],
    difficulty: 'medium',
    selectedNumber: null
  }),

  actions: {
    async newGame(difficulty: 'easy' | 'medium' | 'hard') {
      this.difficulty = difficulty
      // TODO: Call backend API to generate new game
    },

    selectNumber(number: number) {
      this.selectedNumber = number
    },

    placeNumber(row: number, col: number) {
      if (this.selectedNumber === null) return
      // TODO: Implement number placement and validation
    }
  }
}) 