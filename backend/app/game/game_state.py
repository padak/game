"""
Game state management for Math Crossword Game.
Handles active games and move validation.
"""

from typing import Dict, Optional, List
from dataclasses import dataclass
import uuid
import time
import logging

@dataclass
class Move:
    row: int
    col: int
    value: int

class GameState:
    def __init__(self, grid, equations, number_bank, difficulty):
        self.id = str(uuid.uuid4())
        self.grid = grid
        self.equations = equations
        self.number_bank = list(number_bank)  # Make a copy
        self.difficulty = difficulty
        self.created_at = time.time()
        self.last_activity = time.time()
        self.moves: List[Move] = []

    def validate_move(self, move: Move) -> Dict:
        """Validate a move and update game state if valid."""
        logging.info(f"Validating move: row={move.row}, col={move.col}, value={move.value}")
        
        # Check if position is valid
        if not (0 <= move.row < len(self.grid) and 0 <= move.col < len(self.grid[0])):
            logging.error("Invalid position")
            return {
                'valid': False,
                'error': 'Invalid position'
            }

        # Check if cell exists and is available
        cell = self.grid[move.row][move.col]
        if not cell:
            logging.error("Cell does not exist")
            return {
                'valid': False,
                'error': 'Cell does not exist'
            }
        
        if cell.get('isOperator') or cell.get('isFixed', False):
            logging.error("Cell is not available for moves")
            return {
                'valid': False,
                'error': 'Cell is not available for moves'
            }
        
        if not cell.get('inEquation', False):
            logging.error("Cell is not part of an equation")
            return {
                'valid': False,
                'error': 'Cell is not part of an equation'
            }

        # Check if number is in number bank
        if move.value not in self.number_bank:
            logging.error("Number is not available in number bank")
            return {
                'valid': False,
                'error': 'Number is not available in number bank'
            }

        # Apply the move
        cell['value'] = move.value
        cell['isEmpty'] = False
        self.number_bank.remove(move.value)
        self.moves.append(move)
        self.last_activity = time.time()

        # Validate affected equations
        affected_equations = self._validate_equations(move)
        
        # Log validation results
        logging.info(f"Move validation successful. Affected equations: {affected_equations}")

        return {
            'valid': True,
            'grid': self.grid,
            'numberBank': self.number_bank,
            'affectedEquations': affected_equations
        }

    def clear_cell(self, row: int, col: int) -> Dict:
        """Clear a cell and return its value to the number bank."""
        logging.info(f"Clearing cell: row={row}, col={col}")
        
        # Check if position is valid
        if not (0 <= row < len(self.grid) and 0 <= col < len(self.grid[0])):
            logging.error("Invalid position")
            return {
                'valid': False,
                'error': 'Invalid position'
            }

        cell = self.grid[row][col]
        if not cell:
            logging.error("Cell does not exist")
            return {
                'valid': False,
                'error': 'Cell does not exist'
            }
        
        if cell.get('isOperator') or cell.get('isFixed', False):
            logging.error("Cell cannot be cleared")
            return {
                'valid': False,
                'error': 'Cell cannot be cleared'
            }

        value = cell.get('value')
        if value is not None:
            cell['value'] = None
            cell['isEmpty'] = True
            cell['isCorrect'] = False
            cell['isIncorrect'] = False
            self.number_bank.append(value)
            self.number_bank.sort()  # Keep bank sorted
            self.last_activity = time.time()

            # Validate affected equations
            affected_equations = self._validate_equations(Move(row, col, None))
            
            logging.info(f"Cell cleared successfully. Value {value} returned to number bank")

            return {
                'valid': True,
                'grid': self.grid,
                'numberBank': self.number_bank,
                'affectedEquations': affected_equations
            }

        logging.error("Cell is already empty")
        return {
            'valid': False,
            'error': 'Cell is already empty'
        }

    def _validate_equations(self, move: Move) -> List[Dict]:
        """Validate equations affected by a move."""
        affected_equations = []

        # Check horizontal equations
        for col in range(max(0, move.col - 4), min(len(self.grid[0]), move.col + 1)):
            if col + 4 < len(self.grid[0]):  # Need 5 cells for equation
                equation = self._validate_equation_at(move.row, col, 'horizontal')
                if equation:
                    affected_equations.append(equation)

        # Check vertical equations
        for row in range(max(0, move.row - 4), min(len(self.grid), move.row + 1)):
            if row + 4 < len(self.grid):  # Need 5 cells for equation
                equation = self._validate_equation_at(row, move.col, 'vertical')
                if equation:
                    affected_equations.append(equation)

        return affected_equations

    def _validate_equation_at(self, start_row: int, start_col: int, orientation: str) -> Optional[Dict]:
        """Validate equation at given position and orientation."""
        cells = []
        for i in range(5):  # X op Y = Z format needs 5 cells
            row = start_row + (i if orientation == 'vertical' else 0)
            col = start_col + (i if orientation == 'horizontal' else 0)
            cell = self.grid[row][col]
            if not cell or not cell.get('inEquation', False):
                return None
            cells.append(cell)

        # Check if this forms a complete equation
        if not all(cell.get('value') is not None or cell.get('isOperator') for cell in cells):
            return None

        # Extract values and operator
        num1 = cells[0].get('value')
        op = cells[1].get('operator')
        num2 = cells[2].get('value')
        equals = cells[3].get('operator')
        result = cells[4].get('value')

        if not all([num1 is not None, op, num2 is not None, equals == '=', result is not None]):
            return None

        # Validate equation
        expected = None
        if op == '+':
            expected = num1 + num2
        elif op == '-':
            expected = num1 - num2
        elif op == '*':
            expected = num1 * num2

        is_valid = expected == result

        # Update cell states
        for cell in cells:
            if not cell.get('isOperator'):
                cell['isCorrect'] = is_valid
                cell['isIncorrect'] = not is_valid

        return {
            'start': {'row': start_row, 'col': start_col},
            'orientation': orientation,
            'isValid': is_valid
        }

class GameStateManager:
    def __init__(self):
        self.active_games: Dict[str, GameState] = {}
        self.cleanup_threshold = 3600  # 1 hour in seconds

    def create_game(self, puzzle_data: Dict, difficulty: str) -> GameState:
        """Create a new game state from puzzle data."""
        game = GameState(
            grid=puzzle_data['grid'],
            equations=puzzle_data['equations'],
            number_bank=puzzle_data['numberBank'],
            difficulty=difficulty
        )
        self.active_games[game.id] = game
        return game

    def get_game(self, game_id: str) -> Optional[GameState]:
        """Get game state by ID."""
        self._cleanup_old_games()
        return self.active_games.get(game_id)

    def _cleanup_old_games(self):
        """Remove inactive games older than cleanup_threshold."""
        current_time = time.time()
        to_remove = []
        for game_id, game in self.active_games.items():
            if current_time - game.last_activity > self.cleanup_threshold:
                to_remove.append(game_id)
        for game_id in to_remove:
            del self.active_games[game_id] 