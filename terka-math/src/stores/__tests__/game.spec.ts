import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useGameStore } from '../game'
import { apiService, type Cell, type GameState } from '@/services/api'

vi.mock('@/services/api', () => ({
  apiService: {
    startNewGame: vi.fn(),
    validateMove: vi.fn(),
    clearCell: vi.fn(),
    getGameState: vi.fn()
  }
}))

describe('Game Store', () => {
  let store: ReturnType<typeof useGameStore>

  beforeEach(() => {
    store = useGameStore()
  })

  describe('initializeGame', () => {
    it('should initialize a new game with default difficulty', async () => {
      const mockGameState: GameState = {
        gameId: '123',
        grid: [[{
          value: 1,
          isFixed: true,
          isOperator: false,
          isResult: false,
          isCorrect: false,
          isIncorrect: false
        }]],
        numberBank: [1, 2, 3],
        difficulty: 'medium'
      }

      vi.mocked(apiService.startNewGame).mockResolvedValueOnce(mockGameState)

      await store.initializeGame()

      expect(apiService.startNewGame).toHaveBeenCalledWith('medium')
      expect(store.grid).toEqual(mockGameState.grid)
      expect(store.availableNumbers).toEqual(mockGameState.numberBank)
      expect(store.difficulty).toBe('medium')
      expect(store.loading).toBe(false)
      expect(store.error).toBeNull()
    })

    it('should handle errors during initialization', async () => {
      const error = new Error('API Error')
      vi.mocked(apiService.startNewGame).mockRejectedValueOnce(error)

      await store.initializeGame()

      expect(store.error).toBe('API Error')
      expect(store.loading).toBe(false)
    })
  })

  describe('placeNumber', () => {
    it('should place a number successfully', async () => {
      const mockResult = {
        valid: true,
        grid: [[{
          value: 5,
          isFixed: false,
          isOperator: false,
          isResult: false,
          isCorrect: true,
          isIncorrect: false
        }]],
        numberBank: [1, 2, 3]
      }

      store.selectedNumber = 5
      vi.mocked(apiService.validateMove).mockResolvedValueOnce(mockResult)

      await store.placeNumber(0, 0)

      expect(apiService.validateMove).toHaveBeenCalledWith(0, 0, 5)
      expect(store.grid).toEqual(mockResult.grid)
      expect(store.availableNumbers).toEqual(mockResult.numberBank)
      expect(store.selectedNumber).toBeNull()
      expect(store.loading).toBe(false)
      expect(store.error).toBeNull()
    })

    it('should not make API call if no number is selected', async () => {
      store.selectedNumber = null
      await store.placeNumber(0, 0)

      expect(apiService.validateMove).not.toHaveBeenCalled()
    })

    it('should handle errors when placing number', async () => {
      const error = new Error('Invalid move')
      store.selectedNumber = 5
      vi.mocked(apiService.validateMove).mockRejectedValueOnce(error)

      await store.placeNumber(0, 0)

      expect(store.error).toBe('Invalid move')
      expect(store.loading).toBe(false)
    })
  })

  describe('clearCell', () => {
    it('should clear a cell successfully', async () => {
      const mockResult = {
        valid: true,
        grid: [[{
          value: null,
          isFixed: false,
          isOperator: false,
          isResult: false,
          isCorrect: false,
          isIncorrect: false
        }]],
        numberBank: [1, 2, 3, 5]
      }

      vi.mocked(apiService.clearCell).mockResolvedValueOnce(mockResult)

      await store.clearCell(0, 0)

      expect(apiService.clearCell).toHaveBeenCalledWith(0, 0)
      expect(store.grid).toEqual(mockResult.grid)
      expect(store.availableNumbers).toEqual(mockResult.numberBank)
      expect(store.loading).toBe(false)
      expect(store.error).toBeNull()
    })

    it('should handle errors when clearing cell', async () => {
      const error = new Error('Cannot clear cell')
      vi.mocked(apiService.clearCell).mockRejectedValueOnce(error)

      await store.clearCell(0, 0)

      expect(store.error).toBe('Cannot clear cell')
      expect(store.loading).toBe(false)
    })
  })

  describe('isGameComplete', () => {
    it('should return true when all cells are complete or valid', () => {
      store.grid = [
        [
          {
            value: 1,
            isFixed: true,
            isOperator: false,
            isResult: false,
            isCorrect: false,
            isIncorrect: false
          },
          {
            value: null,
            isFixed: false,
            isOperator: true,
            operator: '+',
            isResult: false,
            isCorrect: false,
            isIncorrect: false
          },
          {
            value: 2,
            isFixed: false,
            isOperator: false,
            isResult: false,
            isCorrect: true,
            isIncorrect: false
          }
        ]
      ]

      expect(store.isGameComplete).toBe(true)
    })

    it('should return false when some cells are incomplete or invalid', () => {
      store.grid = [
        [
          {
            value: 1,
            isFixed: true,
            isOperator: false,
            isResult: false,
            isCorrect: false,
            isIncorrect: false
          },
          {
            value: null,
            isFixed: false,
            isOperator: true,
            operator: '+',
            isResult: false,
            isCorrect: false,
            isIncorrect: false
          },
          {
            value: 2,
            isFixed: false,
            isOperator: false,
            isResult: false,
            isCorrect: false,
            isIncorrect: false
          }
        ]
      ]

      expect(store.isGameComplete).toBe(false)
    })
  })
}) 