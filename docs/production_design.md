# Math Crossword Game - Developer Description

This document outlines how to implement a **Math Crossword Game** that can be served locally on a computer for one or two players to connect and play. It incorporates the user's requirements:

1. **Supported Operations**: `+`, `-`, `*`, `/` (all integer results, no decimals, no negatives)  
2. **Difficulty Levels**: Differ by number of pre‐filled cells and equation complexity  
3. **Puzzle Generation**: Generated on‐the‐fly (randomly, no pre‐stored puzzles)  
4. **User Interaction**: Click-to-select from a number bank, then click-to-place into the crossword grid; immediate validation as soon as an equation is completed  
5. **Validation**:  
   - Only `X op Y = Z` style (exactly two operands and one result)  
   - If an equation is incomplete, partial correctness can be marked (the placed number might be green if it still fits).  
   - Once an equation is fully populated, if it's correct, show it in green; otherwise red.  
   - For interconnected equations, validate all affected equations when a shared cell is modified.
6. **Completion**: When the entire puzzle is correctly filled, show a "Congratulations!" popup.  
7. **No Scoreboard or Persistent State** (Version 1)  
8. **Up to Two Players**: Both can join the same game and see each other's moves in real time (shared state).  
9. **Technology**: Python/Flask backend plus Vue.js frontend for clean architecture and strong type support
10. **Layout**: The crossword should not rearrange dynamically (no reflowing while playing). A basic responsive approach is fine so it can fit on a mobile screen, but no puzzle "re‐generation" or reshuffling.

---

## High‐Level Overview

1. **Server**  
   - Serves a single shared puzzle state for all clients (up to two players).  
   - Generates a crossword puzzle in memory whenever a new game is requested.
   - Validates moves and maintains game state consistency.

2. **Frontend**  
   - Renders the crossword grid with clear visual distinction between:
     - Pre-filled numbers (non-interactive)
     - Operators (+, -, *, /, =)
     - Empty cells (interactive)
     - Shared cells (part of multiple equations)
   - Shows a "number bank" below with available numbers
   - Performs immediate arithmetic validation
   - Provides visual feedback for correct/incorrect equations

3. **Communication**  
   - Option A: **Simple** – Each move is posted to the server; the server returns validation results and updates puzzle state. Each player polls the server or refreshes state periodically.  
   - Option B: **Real Time** – A WebSocket or similar solution for immediate updates between players.

---

## Puzzle Generation

Since the puzzle must be generated on‐the‐fly, you need an algorithm that:

1. **Establishes a Grid Layout**  
   - Decide how many equations to include (based on difficulty). For instance:
     - **Easy**: 3–4 equations, several pre‐filled cells.  
     - **Medium**: 5–7 equations, fewer pre‐filled.  
     - **Hard**: 8+ equations, minimal pre‐filled.  
   - Each equation is of the form `A op B = C`.

2. **Ensures Integer‐Only Operations**  
   - All results `C` must be positive integers.  
   - No fractional results (so for division `A / B`, ensure `B` divides `A` evenly).  
   - Avoid negative outcomes.

3. **Shared Cells and Equation Interconnection**  
   - Equations can share cells to create crossword-style intersections
   - When cells are shared:
     - The number must satisfy both equations
     - Validation must check all affected equations
     - Visual feedback should reflect the state of all related equations
   - Example patterns:
     ```
     Horizontal: 2 + x = 5
     Vertical:   x * 4 = 12
     (where x = 3 satisfies both equations)
     ```
     ```
     Horizontal: a + b = 10
     Vertical:   b * 2 = 8
     (where a = 6, b = 4 satisfies both equations)
     ```

4. **Pre‐Fill Strategy**  
   - Pre-fill cells strategically to guide solution
   - Always include some fixed numbers to anchor equations
   - Consider difficulty when deciding what to pre-fill:
     - Easy: More pre-filled numbers, especially results
     - Medium: Some pre-filled numbers, mix of operands and results
     - Hard: Minimal pre-filled numbers, mainly operators

5. **Number Bank Generation**  
   - Include all required numbers for valid solutions
   - Add some decoy numbers for challenge
   - Sort numbers for better user experience
   - Support multiple instances of the same number if needed
   - Remove numbers from bank when used
   - Return numbers to bank when cells are cleared

### Example Pseudocode for Generating a Puzzle

```js
function generatePuzzle(difficulty) {
  const grid = createEmptyGrid();   // Fixed size (8x8 maximum)
  const equations = [];
  const usedCells = new Set();

  // 1. Decide equation count based on difficulty
  const eqCount = (difficulty === 'easy') ? 4 : (difficulty === 'hard') ? 8 : 6;

  // 2. Generate and place equations
  for (let i = 0; i < eqCount; i++) {
    const operator = pickRandomOperator();
    const orientation = pickOrientation();
    const position = findValidPosition(grid, orientation, usedCells);
    
    // Generate numbers ensuring shared cell consistency
    const [A, B, C] = generateValidTriple(operator, position, grid);
    
    // Place equation in grid
    placeEquation(grid, position, orientation, A, operator, B, C);
    equations.push({ position, orientation, A, operator, B, C });
    
    // Mark used cells
    markUsedCells(usedCells, position, orientation);
  }

  // 3. Pre-fill cells based on difficulty
  preFillCells(grid, difficulty);

  // 4. Generate number bank
  const numberBank = generateNumberBank(grid, difficulty);

  return { grid, equations, numberBank };
}
```

## Data Model

The game state is managed using TypeScript interfaces:

```typescript
interface Cell {
  value: number | null
  isFixed: boolean
  isOperator: boolean
  operator?: '+' | '-' | '*' | '/' | '='
  isResult: boolean
  isCorrect?: boolean
  isIncorrect?: boolean
}

interface GameState {
  grid: Cell[][]
  availableNumbers: number[]
  selectedNumber: number | null
  difficulty: 'easy' | 'medium' | 'hard'
  gridSize: number
}
```

## Frontend Implementation

1. **Grid Component**
   - Renders the game grid using CSS Grid
   - Handles cell click events
   - Shows validation state through CSS classes
   - Supports mobile touch interactions

2. **Number Bank Component**
   - Displays available numbers
   - Handles number selection
   - Shows selected state
   - Updates as numbers are used/returned

3. **Game Logic**
   - Click-to-select-then-click-to-place interaction:
     1. User clicks number in bank (highlights selection)
     2. User clicks empty cell to place number
     3. Number disappears from bank
     4. Equations are validated
   - Validation flow:
     1. Check if equation is complete
     2. Validate all affected equations
     3. Update visual feedback
     4. Check for game completion

4. **Visual Feedback**
   - Green: Correct equations
   - Red: Incorrect equations
   - Neutral: Incomplete equations
   - Highlighted: Selected number
   - Disabled: Fixed/operator cells

## Edge Cases & Validation Rules

1. **Shared Cell Updates**
   - When updating a shared cell:
     1. Validate all equations containing the cell
     2. Show appropriate feedback for each equation
     3. Handle cases where a number satisfies one equation but not others

2. **Partial Equation Validation**
   - For incomplete equations:
     1. Check if current numbers could still form valid equation
     2. Show neutral state if equation is still potentially valid
     3. Show red if equation cannot be valid with current numbers

3. **Number Bank Management**
   - Track multiple instances of same number
   - Remove numbers when placed
   - Return numbers when cells are cleared
   - Sort numbers for consistency

4. **Mobile Considerations**
   - Touch-friendly hit areas
   - Responsive grid sizing
   - Clear visual feedback for touch interactions

## Implementation Phases

1. **Phase 1: Single Player (Current)**
   - Core game mechanics
   - Equation validation
   - Mobile-friendly UI
   - Number bank management

2. **Phase 2: Multiplayer (Future)**
   - Real-time state sync
   - Player presence
   - Move validation
   - Shared game state

---

This design document serves as the source of truth for implementation decisions and should be updated as the project evolves.