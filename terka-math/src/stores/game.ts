import { defineStore } from 'pinia'

export interface Cell {
  value: number | null
  isFixed: boolean
  isOperator: boolean
  operator?: '+' | '-' | '*' | '/' | '='
  isResult: boolean
  isCorrect?: boolean  // New property to track if the cell is part of a correct equation
}

export interface GameState {
  grid: Cell[][]
  availableNumbers: number[]
  selectedNumber: number | null
  difficulty: 'easy' | 'medium' | 'hard'
  gridSize: number
}

export const useGameStore = defineStore('game', {
  state: (): GameState => ({
    grid: [],
    availableNumbers: [],
    selectedNumber: null,
    difficulty: 'medium',
    gridSize: 8
  }),

  getters: {
    isGameComplete: (state) => {
      return state.grid.every(row => 
        row.every(cell => 
          cell.isFixed || cell.isOperator || cell.isCorrect || cell.value === null
        )
      )
    }
  },

  actions: {
    validateEquations() {
      // Validate horizontal equations
      for (let row = 0; row < this.gridSize; row++) {
        for (let col = 0; col < this.gridSize - 4; col++) {
          const cells = this.grid[row].slice(col, col + 5)
          if (this.isValidEquation(cells)) {
            cells.forEach(cell => cell.isCorrect = true)
          }
        }
      }

      // Validate vertical equations
      for (let col = 0; col < this.gridSize; col++) {
        for (let row = 0; row < this.gridSize - 4; row++) {
          const cells = Array(5).fill(null)
            .map((_, i) => this.grid[row + i][col])
          if (this.isValidEquation(cells)) {
            cells.forEach(cell => cell.isCorrect = true)
          }
        }
      }
    },

    isValidEquation(cells: Cell[]): boolean {
      if (cells.length !== 5) return false
      
      const [num1, op, num2, eq, result] = cells
      if (!num1?.value || !num2?.value || !result?.value) return false
      if (!op?.operator || op.operator === '=' || !eq?.operator || eq.operator !== '=') return false

      switch (op.operator) {
        case '+': return num1.value + num2.value === result.value
        case '-': return num1.value - num2.value === result.value
        case '*': return num1.value * num2.value === result.value
        case '/': return num1.value / num2.value === result.value && Number.isInteger(num1.value / num2.value)
        default: return false
      }
    },

    initializeGame(difficulty: 'easy' | 'medium' | 'hard' = 'medium') {
      this.difficulty = difficulty
      this.gridSize = difficulty === 'easy' ? 6 : difficulty === 'medium' ? 8 : 10
      
      // Initialize empty grid
      this.grid = Array(this.gridSize).fill(null).map(() => 
        Array(this.gridSize).fill(null).map(() => ({
          value: null,
          isFixed: false,
          isOperator: false,
          isResult: false,
          isCorrect: false
        }))
      )

      // Horizontal equation: 2 + ? = 5
      this.grid[1][1] = { value: 2, isFixed: true, isOperator: false, isResult: false }
      this.grid[1][2] = { value: null, isFixed: false, isOperator: true, operator: '+', isResult: false }
      this.grid[1][3] = { value: null, isFixed: false, isOperator: false, isResult: false } // Player needs to put 3 here
      this.grid[1][4] = { value: null, isFixed: false, isOperator: true, operator: '=', isResult: false }
      this.grid[1][5] = { value: 5, isFixed: true, isOperator: false, isResult: true }

      // Vertical equation starting from the empty cell above: ? * 4 = ?
      this.grid[2][3] = { value: null, isFixed: false, isOperator: true, operator: '*', isResult: false }
      this.grid[3][3] = { value: 4, isFixed: true, isOperator: false, isResult: false }
      this.grid[4][3] = { value: null, isFixed: false, isOperator: true, operator: '=', isResult: false }
      this.grid[5][3] = { value: null, isFixed: false, isOperator: false, isResult: true } // Player needs to put 12 here

      // Initialize available numbers (including numbers needed for both equations)
      this.availableNumbers = [
        1, 1,
        2, 2,
        3, 3,  // For horizontal equation (2 + 3 = 5)
        4, 4,
        5, 5,
        6, 6,
        7, 7,
        8, 8,
        9, 9,
        12, 12  // For vertical equation (3 * 4 = 12)
      ].sort((a, b) => a - b)
    },

    selectNumber(num: number | null) {
      this.selectedNumber = num
    },

    placeNumber(row: number, col: number) {
      if (this.selectedNumber === null || !this.grid[row]?.[col]) return
      
      const cell = this.grid[row][col]
      if (cell.isFixed || cell.isOperator) return

      cell.value = this.selectedNumber
      
      // Remove the used number from available numbers
      const index = this.availableNumbers.indexOf(this.selectedNumber)
      if (index !== -1) {
        this.availableNumbers.splice(index, 1)
      }
      
      this.selectedNumber = null

      // Validate equations after placing a number
      this.validateEquations()
    },

    clearCell(row: number, col: number) {
      const cell = this.grid[row]?.[col]
      if (!cell || cell.isFixed || cell.isOperator) return
      
      // Add the number back to available numbers if it was used
      if (cell.value !== null) {
        this.availableNumbers.push(cell.value)
        // Sort numbers for better user experience
        this.availableNumbers.sort((a, b) => a - b)
      }
      
      cell.value = null
      cell.isCorrect = false
      
      // Revalidate equations after clearing a cell
      this.validateEquations()
    }
  }
}) 