import { beforeEach, afterEach, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'

// Mock fetch globally
global.fetch = vi.fn()

// Setup Pinia for testing
beforeEach(() => {
  setActivePinia(createPinia())
})

// Reset all mocks after each test
afterEach(() => {
  vi.clearAllMocks()
}) 