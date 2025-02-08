/**
 * API service for communicating with the backend.
 */

// Use environment variable for API URL, fallback to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://0.0.0.0:5001/api'

console.log('API_BASE_URL:', API_BASE_URL) // Debug log

export interface GameState {
  gameId: string
  grid: Cell[][]
  numberBank: number[]
  difficulty: 'easy' | 'medium' | 'hard'
}

export interface Cell {
  value: number | null
  isOperator: boolean
  operator?: '+' | '-' | '*' | '=' | null
  isFixed: boolean
  isResult: boolean
  isCorrect?: boolean
  isIncorrect?: boolean
  isEmpty?: boolean
  inEquation?: boolean
}

export interface MoveResult {
  valid: boolean
  error?: string
  grid?: Cell[][]
  numberBank?: number[]
  affectedEquations?: Array<{
    start: { row: number; col: number }
    orientation: 'horizontal' | 'vertical'
    isValid: boolean
  }>
}

class ApiService {
  private gameId: string | null = null

  /**
   * Start a new game with the specified difficulty.
   */
  async startNewGame(difficulty: 'easy' | 'medium' | 'hard'): Promise<GameState> {
    try {
      console.log('Starting new game with difficulty:', difficulty) // Debug log
      const response = await fetch(`${API_BASE_URL}/newGame?difficulty=${difficulty}`)
      console.log('New game response status:', response.status) // Debug log
      
      if (!response.ok) {
        const error = await response.json()
        console.error('Server error:', error) // Debug log
        throw new Error(error.error || 'Failed to start new game')
      }
      
      const gameState = await response.json()
      console.log('Received game state:', gameState) // Debug log
      this.gameId = gameState.gameId
      return gameState
    } catch (error) {
      console.error('Error in startNewGame:', error) // Debug log
      if (error instanceof Error) {
        throw new Error(`Network error: ${error.message}. Please check if the server is running and accessible.`)
      }
      throw error
    }
  }

  /**
   * Validate and apply a move.
   */
  async validateMove(row: number, col: number, value: number): Promise<MoveResult> {
    if (!this.gameId) {
      throw new Error('No active game')
    }

    const response = await fetch(`${API_BASE_URL}/validateMove`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        gameId: this.gameId,
        row,
        col,
        value
      })
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Failed to validate move')
    }

    return response.json()
  }

  /**
   * Clear a cell in the grid.
   */
  async clearCell(row: number, col: number): Promise<MoveResult> {
    if (!this.gameId) {
      throw new Error('No active game')
    }

    const response = await fetch(`${API_BASE_URL}/clearCell`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        gameId: this.gameId,
        row,
        col
      })
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Failed to clear cell')
    }

    return response.json()
  }

  /**
   * Get the current game state.
   */
  async getGameState(): Promise<GameState> {
    if (!this.gameId) {
      throw new Error('No active game')
    }

    const response = await fetch(`${API_BASE_URL}/gameState?gameId=${this.gameId}`)
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Failed to get game state')
    }

    return response.json()
  }
}

// Export a singleton instance
export const apiService = new ApiService() 