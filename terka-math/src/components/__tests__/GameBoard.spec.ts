import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import GameBoard from '../GameBoard.vue'
import { useGameStore } from '@/stores/game'

describe('GameBoard', () => {
  const createWrapper = () => {
    return mount(GameBoard, {
      global: {
        plugins: [createTestingPinia({
          createSpy: vi.fn,
          initialState: {
            game: {
              grid: [
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
              ],
              availableNumbers: [1, 2, 3],
              selectedNumber: null,
              loading: false,
              error: null
            }
          }
        })]
      }
    })
  }

  it('should mount successfully', () => {
    const wrapper = createWrapper()
    expect(wrapper.exists()).toBe(true)
  })

  it('should display loading overlay when loading', async () => {
    const wrapper = createWrapper()
    const store = useGameStore()
    store.loading = true

    await wrapper.vm.$nextTick()
    expect(wrapper.find('.loading-overlay').exists()).toBe(true)
  })

  it('should display error message when there is an error', async () => {
    const wrapper = createWrapper()
    const store = useGameStore()
    store.error = 'Test error'

    await wrapper.vm.$nextTick()
    const errorMessage = wrapper.find('.error-message')
    expect(errorMessage.exists()).toBe(true)
    expect(errorMessage.text()).toContain('Test error')
  })

  it('should render grid cells correctly', () => {
    const wrapper = createWrapper()
    const cells = wrapper.findAll('.cell')
    
    expect(cells.length).toBe(3)
    expect(cells[0].text()).toBe('1')
    expect(cells[1].text()).toBe('+')
    expect(cells[2].text()).toBe('2')
  })

  it('should apply correct CSS classes to cells', () => {
    const wrapper = createWrapper()
    const cells = wrapper.findAll('.cell')
    
    expect(cells[0].classes()).toContain('fixed')
    expect(cells[1].classes()).toContain('operator')
    expect(cells[2].classes()).toContain('correct')
  })

  it('should render number bank buttons', () => {
    const wrapper = createWrapper()
    const buttons = wrapper.findAll('.number-bank button')
    
    expect(buttons.length).toBe(3)
    expect(buttons[0].text()).toBe('1')
    expect(buttons[1].text()).toBe('2')
    expect(buttons[2].text()).toBe('3')
  })

  it('should call selectNumber when clicking number bank button', async () => {
    const wrapper = createWrapper()
    const store = useGameStore()
    const button = wrapper.findAll('.number-bank button')[0]
    
    await button.trigger('click')
    expect(store.selectNumber).toHaveBeenCalledWith(1)
  })

  it('should call placeNumber when clicking empty cell with selected number', async () => {
    const wrapper = createWrapper()
    const store = useGameStore()
    store.selectedNumber = 5
    store.grid[0][1] = {
      value: null,
      isFixed: false,
      isOperator: false,
      isResult: false,
      isCorrect: false,
      isIncorrect: false
    }
    
    const emptyCell = wrapper.findAll('.cell')[1]
    await emptyCell.trigger('click')
    
    expect(store.placeNumber).toHaveBeenCalledWith(0, 1)
  })

  it('should call clearCell when clicking filled non-fixed cell', async () => {
    const wrapper = createWrapper()
    const store = useGameStore()
    
    const filledCell = wrapper.findAll('.cell')[2]
    await filledCell.trigger('click')
    
    expect(store.clearCell).toHaveBeenCalledWith(0, 2)
  })

  it('should not call any action when clicking fixed or operator cells', async () => {
    const wrapper = createWrapper()
    const store = useGameStore()
    
    const fixedCell = wrapper.findAll('.cell')[0]
    const operatorCell = wrapper.findAll('.cell')[1]
    
    await fixedCell.trigger('click')
    await operatorCell.trigger('click')
    
    expect(store.placeNumber).not.toHaveBeenCalled()
    expect(store.clearCell).not.toHaveBeenCalled()
  })

  it('should initialize game on mount', () => {
    const wrapper = createWrapper()
    const store = useGameStore()
    
    expect(store.initializeGame).toHaveBeenCalledOnce()
  })

  it('should handle difficulty selection', async () => {
    const wrapper = createWrapper()
    const store = useGameStore()
    const buttons = wrapper.findAll('.controls button')
    const easyButton = buttons[0]
    
    await easyButton.trigger('click')
    expect(store.initializeGame).toHaveBeenCalledWith('easy')
  })
}) 