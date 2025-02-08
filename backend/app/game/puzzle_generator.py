"""
Puzzle generator for Math Crossword Game.
Handles creation of valid math equations and their placement in the grid.
"""

from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass
import random
import time

@dataclass
class Position:
    row: int
    col: int
    orientation: str  # 'horizontal' or 'vertical'

@dataclass
class Equation:
    position: Position
    a: int
    operator: str
    b: int
    result: int
    cells: List[Tuple[int, int]]  # List of (row, col) for each cell in equation

class PuzzleGenerator:
    OPERATORS = ['+', '-', '*']  # Removed division to simplify
    MAX_ATTEMPTS = 20  # Further reduced from 50
    MAX_GENERATION_TIME = 2  # Reduced from 5 seconds
    
    # Pre-computed valid equations for each operator
    VALID_EQUATIONS = {
        '+': [(a, b, a + b) for a in range(1, 10) for b in range(1, 10) if a + b <= 15],
        '-': [(a, b, a - b) for a in range(1, 10) for b in range(1, 10) if a > b],
        '*': [(a, b, a * b) for a in range(1, 6) for b in range(1, 6)]
    }

    def __init__(self, grid_size: int = 8):
        self.grid_size = grid_size
        self.used_cells: Set[Tuple[int, int]] = set()
        self.equations: List[Equation] = []
        self.grid: List[List[Optional[Dict]]] = [
            [None for _ in range(grid_size)] for _ in range(grid_size)
        ]
        self.cell_equations: Dict[Tuple[int, int], List[Equation]] = {}
        self.start_time = 0

    def generate_puzzle(self, difficulty: str) -> Dict:
        """Generate a complete puzzle based on difficulty level."""
        self.start_time = time.time()
        self._reset()
        eq_count = self._get_equation_count(difficulty)
        
        # Generate and place equations
        equations_placed = 0
        attempts = 0
        max_total_attempts = eq_count * 3  # Limit total attempts
        
        while equations_placed < eq_count and attempts < max_total_attempts:
            if time.time() - self.start_time > self.MAX_GENERATION_TIME:
                break
            if self._add_equation():
                equations_placed += 1
            attempts += 1

        # Generate number bank
        number_bank = self._generate_number_bank()

        return {
            'grid': self.grid,
            'equations': self.equations,
            'numberBank': sorted(number_bank)
        }

    def _reset(self):
        """Reset the generator state."""
        self.used_cells.clear()
        self.equations.clear()
        self.cell_equations.clear()
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def _get_equation_count(self, difficulty: str) -> int:
        """Determine number of equations based on difficulty."""
        return {
            'easy': 2,
            'medium': 3,
            'hard': 4
        }.get(difficulty, 2)

    def _add_equation(self) -> bool:
        """Try to add a new equation to the puzzle."""
        orientation = random.choice(['horizontal', 'vertical'])
        operator = random.choice(self.OPERATORS)
        
        # Get a valid position
        position = self._find_valid_position(orientation)
        if not position:
            return False

        # Get intersections
        intersections = self._find_intersections(position)
        if not self._try_place_equation(position, operator, intersections):
            return False

        return True

    def _try_place_equation(self, position: Position, operator: str, intersections: List[Tuple[Tuple[int, int], int]]) -> bool:
        """Try to place an equation at the given position."""
        # Get valid equations for this operator
        valid_equations = self.VALID_EQUATIONS[operator]
        
        # Shuffle to try random combinations
        random.shuffle(valid_equations)
        
        for a, b, result in valid_equations[:10]:  # Only try first 10 combinations
            if self._validate_numbers_with_existing(position, a, b, result):
                cells = self._get_equation_cells(position, 5)
                equation = Equation(position, a, operator, b, result, cells)
                if self._place_equation(equation):
                    self.equations.append(equation)
                    for cell in cells:
                        if cell not in self.cell_equations:
                            self.cell_equations[cell] = []
                        self.cell_equations[cell].append(equation)
                    return True
        return False

    def _find_valid_position(self, orientation: str) -> Optional[Position]:
        """Find a valid position for a new equation."""
        attempts = 0
        max_attempts = 10  # Limit position finding attempts
        
        while attempts < max_attempts:
            if orientation == 'horizontal':
                row = random.randint(0, self.grid_size - 1)
                col = random.randint(0, self.grid_size - 5)  # Need 5 cells for equation
            else:
                row = random.randint(0, self.grid_size - 5)
                col = random.randint(0, self.grid_size - 1)
            
            position = Position(row, col, orientation)
            cells = self._get_equation_cells(position, 5)
            
            # Quick check if position is valid
            if all((r, c) not in self.used_cells for r, c in cells):
                return position
            
            attempts += 1
        return None

    def _get_equation_cells(self, position: Position, length: int) -> List[Tuple[int, int]]:
        """Get the cells that would be used by an equation."""
        cells = []
        for i in range(length):
            if position.orientation == 'horizontal':
                cells.append((position.row, position.col + i))
            else:
                cells.append((position.row + i, position.col))
        return cells

    def _place_equation(self, equation: Equation) -> bool:
        """Place an equation in the grid."""
        # Check if any cells are already used
        for cell in equation.cells:
            if cell in self.used_cells:
                return False
        
        # Place the equation
        cell_values = [equation.a, equation.operator, equation.b, '=', equation.result]
        for (row, col), value in zip(equation.cells, cell_values):
            self.used_cells.add((row, col))
            is_operator = isinstance(value, str)
            self.grid[row][col] = {
                'value': value,
                'isOperator': is_operator,
                'operator': value if is_operator else None,
                'isResult': not is_operator and value == equation.result
            }
        return True

    def _find_intersections(self, position: Position) -> List[Tuple[Tuple[int, int], int]]:
        """Find intersection points with existing equations."""
        intersections = []
        cells = self._get_equation_cells(position, 5)
        
        for i, (row, col) in enumerate(cells):
            if i % 2 == 1:  # Skip operator positions
                continue
            if (row, col) in self.cell_equations:
                for eq in self.cell_equations[(row, col)]:
                    cell_idx = eq.cells.index((row, col))
                    if cell_idx == 0:
                        value = eq.a
                    elif cell_idx == 2:
                        value = eq.b
                    elif cell_idx == 4:
                        value = eq.result
                    else:
                        continue
                    intersections.append(((row, col), value))
                    break
        return intersections

    def _validate_numbers_with_existing(self, position: Position, a: int, b: int, result: int) -> bool:
        """Validate that new numbers work with existing equations at intersection points."""
        cells = self._get_equation_cells(position, 5)
        values = [a, None, b, None, result]
        
        for i, (row, col) in enumerate(cells):
            if values[i] is None:  # Skip operator positions
                continue
            if (row, col) in self.cell_equations:
                for eq in self.cell_equations[(row, col)]:
                    cell_idx = eq.cells.index((row, col))
                    if cell_idx % 2 == 0:  # Number position
                        eq_value = [eq.a, eq.b, eq.result][cell_idx // 2]
                        if eq_value != values[i]:
                            return False
        return True

    def _generate_number_bank(self) -> List[int]:
        """Generate the number bank for the puzzle."""
        numbers = set()
        for eq in self.equations:
            numbers.add(eq.a)
            numbers.add(eq.b)
            numbers.add(eq.result)
        return list(numbers) 