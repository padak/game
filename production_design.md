# Math Crossword Game - Developer Description

This document outlines how to implement a **Math Crossword Game** that can be served locally on a computer for one or two players to connect and play. It incorporates the user’s requirements:

1. **Supported Operations**: `+`, `-`, `*`, `/` (all integer results, no decimals, no negatives)  
2. **Difficulty Levels**: Differ by number of pre‐filled cells and equation complexity  
3. **Puzzle Generation**: Generated on‐the‐fly (randomly, no pre‐stored puzzles)  
4. **User Interaction**: Drag‐and‐drop or click‐and‐place from a number bank into the crossword grid; immediate validation as soon as an equation is completed  
5. **Validation**:  
   - Only `X op Y = Z` style (exactly two operands and one result)  
   - If an equation is incomplete, partial correctness can be marked (the placed number might be green if it still fits).  
   - Once an equation is fully populated, if it’s correct, show it in green; otherwise red.  
6. **Completion**: When the entire puzzle is correctly filled, show a “Congratulations!” popup.  
7. **No Scoreboard or Persistent State** (Version 1)  
8. **Up to Two Players**: Both can join the same game and see each other’s moves in real time (shared state).  
9. **Technology**: Developer’s choice, but a Node/Express backend plus a web‐based frontend is a simple approach.  
10. **Layout**: The crossword should not rearrange dynamically (no reflowing while playing). A basic responsive approach is fine so it can fit on a mobile screen, but no puzzle “re‐generation” or reshuffling.

---

## High‐Level Overview

1. **Server**  
   - Serves a single shared puzzle state for all clients (up to two players).  
   - Generates a crossword puzzle in memory whenever a new game is requested.

2. **Frontend**  
   - Renders the crossword grid (a set of squares for numbers and operators).  
   - Shows a “number bank” below (or side by side), from which players can pick or drag numbers.  
   - Performs immediate arithmetic checks (or sends data to the server for validation).

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

3. **Shared Cells for the Crossword**  
   - Make sure the puzzle is shaped so that certain operand cells or result cells can be shared between two equations (like crossword intersections).  
   - Example pattern (simplified):
     ```
     10 - x = 8
          x + y = 15
              y * 2 = 30
     ```

4. **Pre‐Fill Some Cells**  
   - Depending on difficulty, fill in some of the numbers or results to guide the player.

5. **Generate the “Number Bank”**  
   - Gather all the unique values that appear in the puzzle (operands, results).  
   - Possibly add a few “decoy” numbers to make it trickier.  
   - Shuffle them so the player can’t immediately guess which belongs where.

### Example Pseudocode for Generating a Puzzle

```js
function generatePuzzle(difficulty) {
  const grid = createEmptyGrid();   // Some fixed or random dimension
  const equations = [];

  // 1. Decide how many equations for this difficulty
  const eqCount = (difficulty === 'easy') ? 4 : (difficulty === 'hard') ? 8 : 6;

  // 2. Fill equations
  //    For each equation, pick random operators and integers with constraints.
  //    Place them in the grid in a way that they can intersect.

  for (let i = 0; i < eqCount; i++) {
    const operator = pickRandomOperator(); // +, -, *, or /
    const [A, B, C] = generateValidTriple(operator);
    equations.push({A, operator, B, C});
    placeEquationInGrid(grid, A, operator, B, C);
  }

  // 3. Pre-fill some cells (depends on difficulty)
  preFillSomeCells(grid, difficulty);

  // 4. Generate number bank
  const allNums = collectAllNumbers(grid);
  const decoys = generateDecoysIfNeeded();
  const numberBank = shuffle([...allNums, ...decoys]);

  return {
    grid,
    equations,
    numberBank
  };
}
```
This algorithm can be as simple or complex as you need. For a small prototype, you could place equations linearly without complex intersections. For a more genuine “crossword” style, you’d incorporate logic to place them in crossing rows/columns.

## Data Model

A common approach is to send/receive puzzle data as JSON. For example:

```json
{
  "grid": [
    // Each cell could be { row: number, col: number, contentType: 'operand'|'operator'|'result'|'empty', value?: number|null, prefilled?: boolean }
  ],
  "numberBank": [ 2, 3, 5, 7, 14, ... ],
  "equations": [
    { "row": 0, "col": 0, "orientation": "horizontal", "A": 10, "operator": "-", "B": 2, "C": 8 },
    ...
  ]
}
```
Frontend Implementation
	1.	Grid Rendering
	•	Use a table or CSS grid.
	•	Mark pre-filled cells as read‐only.
	•	Mark empty cells as droppable or clickable placeholders.
	2.	Number Bank
	•	Show the list of available numbers.
	•	The user either:
	1.	Clicks a number in the bank, then clicks an empty cell to place it.
	2.	Drags a number from the bank to the grid cell.
	3.	Validation Flow
	•	Immediate Check: When an operand or result cell is filled, check if that equation is fully populated:
	•	If yes, compute A op B:
	•	If C is correct, color them green.
	•	Else, color the newly placed cell red (or color the entire equation red).
	•	If partial, keep placeholders (the placed cell might remain neutral or green if it doesn’t invalidate the partial equation).
	4.	Two‐Player Updates
	•	Each time a player places a number, an update is sent to the server.
	•	The server shares the updated puzzle state with all connected clients.
	•	With basic polling, each player can poll every second or so, or on an event.
	•	With WebSockets, you can push changes in real time.
	5.	Completion
	•	If all equations are correct, trigger a “Congratulations!” pop‐up.
	•	Possibly disable further interactions or provide a “New Game” button.


## Technology & Setup

Backend
	•	Node.js + Express:
	•	Route: GET /api/newGame?difficulty=easy|medium|hard
	•	Generates a puzzle, stores it in memory with an ID, returns puzzle data.
	•	Route: POST /api/move
	•	Receives a cell update from a client, validates or updates the puzzle state.
	•	Returns updated puzzle state or partial validation results.
	•	If you prefer a smaller footprint, you could also use Python (Flask) or any other simple web framework. Because the game runs on a local machine, you only need minimal server code.

Frontend
	•	React is a common choice, but Vue, Svelte, or plain HTML/JS are also valid.
	•	On the local network, users connect via http://YOUR_LOCAL_IP:PORT.

Real‐Time Updates (Optional)
	•	WebSockets (Socket.IO or native websockets) for immediate multi‐player updates.
	•	Alternatively, simpler approach is short‐interval polling.

## Edge Cases & Notes
	1.	Division By Zero: Exclude or handle carefully during puzzle generation.
	2.	All Positive, Whole Numbers: Filter out negative or fractional results.
	3.	Dragging to Wrong Spot: If the user drags a number that completely invalidates a partial equation, mark it red.
	4.	Decoy Numbers: A few extra numbers in the bank can add challenge.
	5.	No Dynamic Resizing: Keep the grid static once the puzzle is generated. Use a responsive design that scales to screen size without re‐shaping the puzzle.

## Extended Summary

Below is an expanded set of steps you can follow to finalize and deploy the Math Crossword Game. These steps build on the high‐level overview but add a bit more detail to guide a smooth development process.

1. **Generate a Random Puzzle**  
   - **Step 1**: Decide on a crossword layout strategy:
     - **Simple approach**: Place each equation (A op B = C) in a separate row or column with a few overlaps to create the “crossword” feel.
     - **Complex approach**: Use a small backtracking algorithm to enforce more interwoven equations.  
   - **Step 2**: For each equation:
     1. Pick a random operator (`+`, `-`, `*`, `/`).  
     2. Generate integer operands (A, B) that produce a valid result (C) with no negatives or decimals.  
     3. Insert them into the grid, ensuring some cells overlap with existing equations if possible.  
   - **Step 3**: Add or remove prefilled cells depending on the difficulty. For “Hard,” keep them minimal; for “Easy,” fill many values.

2. **Pre‐Fill Cells and Build the Number Bank**  
   - Gather all the integer values (operands and results) in the puzzle.  
   - Insert extra “decoy” numbers if desired for challenge.  
   - Mark certain cells as “prefilled” (the user cannot change these).  
   - Shuffle the final list of numbers to create the number bank.

3. **Render the Puzzle**  
   - Use a static, grid‐based layout. Each cell has:
     - A unique identifier (row/column).  
     - An initial “read‐only” or “empty” state.  
   - Pre‐filled cells show their numbers immediately.  
   - Empty cells are placeholders that can accept a number from the bank.

4. **User Interaction & Validation**  
   - **Drag‐and‐Drop** or **Click‐to-Select**:
     1. User chooses (or drags) a number from the bank.  
     2. User places it in an empty cell.  
   - **Immediate Validation**:
     - Check if all three parts of the related equation (`A op B = C`) are populated.  
       - If so, evaluate the equation.  
       - If correct, highlight it in green; if incorrect, highlight in red (or just highlight the incorrect cell in red).  
     - If only one or two parts are filled, you can still mark a partially correct placement in green (e.g., `X + ? = 5` can remain valid if `X` is still potentially correct).

5. **Completion Check**  
   - After every placement:
     - Evaluate all equations.  
     - If every equation is correct, display a “Congratulations” popup.  
   - Optionally provide a “Reset Puzzle” button or a “New Puzzle” button.

6. **Two‐Player Synchronization**  
   - Either use a quick‐poll approach (e.g., every 1–2 seconds the client asks the server for the latest puzzle state) **or** set up a WebSocket connection:
     1. Each move is sent to the server.  
     2. The server updates the shared puzzle state in memory.  
     3. The server pushes the updated state to both players.  
   - This ensures both players see each other’s moves in near real time.

7. **Deployment / Local Hosting**  
   - **Backend**: A Node.js/Express or Python/Flask server that:
     - Has an endpoint like `/api/newGame?difficulty=easy|medium|hard` to generate a puzzle.  
     - Receives moves in `/api/move`.  
     - Stores the puzzle in memory with some unique game ID.  
   - **Frontend**: A simple HTML/JS or React/Vue app:
     - Renders the grid and number bank.  
     - Sends user actions to the server.  
     - Listens for puzzle updates.  
   - **Local Access**:  
     - Run the server on your computer (`http://localhost:3000` for example).  
     - Players on the same network can connect via `http://YOUR_LOCAL_IP:3000`.

8. **Possible Enhancements**  
   - **Scoring**: Add a timer or track incorrect attempts.  
   - **Animations**: Animate the drag‐and‐drop or the coloring of cells.  
   - **Hints**: Optionally allow a limited number of hints or partial reveals.  
   - **Puzzle Variation**: Over time, add more complicated layouts or different puzzle sizes.

---

## Putting It All Together

By following these steps, you will have:

1. A **randomly generated crossword** with valid integer arithmetic.  
2. **Immediate feedback** for correct/incorrect cell entries.  
3. **Two‐player capability**, so both can collaborate (or compete) on the same puzzle.  
4. A lightweight **local deployment** where the puzzle is accessible on your network without needing a production server.

Feel free to experiment with how “crossword‐like” you make the puzzle. Even a simpler layout (like a small table of equations) can be fun and rewarding while you fine‐tune the logic. Once it’s stable, you can expand to more intricate puzzle shapes and add additional features for an even richer game experience.