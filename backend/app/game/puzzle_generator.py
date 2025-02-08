"""
Puzzle generator for Math Crossword Game.
Handles creation of valid math equations and their placement in the grid.
"""

from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass
import random
import time
import logging

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
    OPERATORS = ['+', '-', '*']
    
    # Pre-computed valid equations for each operator with numbers 1-15
    VALID_EQUATIONS = {
        '+': [(a, b, a + b) for a in range(1, 10) for b in range(1, 10) if a + b <= 15],
        '-': [(a, b, a - b) for a in range(2, 16) for b in range(1, a) if a - b <= 15],
        '*': [(a, b, a * b) for a in range(1, 6) for b in range(1, 6) if a * b <= 15]
    }

    def __init__(self, grid_size: int = 11):  # Increased to 11x11
        self.grid_size = grid_size
        self.grid: List[List[Optional[Dict]]] = []
        self.equations: List[Equation] = []
        self.empty_cells: Set[Tuple[int, int]] = set()
        self.intersection_points: Set[Tuple[int, int]] = set()
        self._used_cells: Set[Tuple[int, int]] = set()

    @property
    def used_cells(self) -> Set[Tuple[int, int]]:
        """Return the set of used cells in the grid."""
        if not self._used_cells:
            self._used_cells = set()
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    if self.grid[row][col] and self.grid[row][col].get('inEquation', False):
                        self._used_cells.add((row, col))
        return self._used_cells

    def generate_puzzle(self, difficulty: str) -> Dict:
        """Generate a complete puzzle based on difficulty level."""
        logging.info(f"\n{'='*20}\nStarting puzzle generation with difficulty: {difficulty}\n{'='*20}")
        
        # Reset state
        self.grid = [[{
            'value': None,
            'isOperator': False,
            'operator': None,
            'isFixed': False,
            'isResult': False,
            'isEmpty': False,  # Initialize as not empty
            'inEquation': False,
            'isCorrect': False,
            'isIncorrect': False
        } for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.equations = []
        self.empty_cells.clear()
        self.intersection_points.clear()
        self._used_cells.clear()
        
        # 1. Generate crossword pattern
        self._generate_pattern(difficulty)
        
        # 2. Fill numbers
        self._fill_numbers()
        
        # 3. Hide some numbers
        number_bank = self._hide_numbers(difficulty)
        
        # Log the generated puzzle
        logging.info("\n=== Generated Puzzle Details ===")
        logging.info(f"Number of equations: {len(self.equations)}")
        logging.info(f"Number of intersections: {len(self.intersection_points)}")
        logging.info(f"Number of empty cells: {len(self.empty_cells)}")
        logging.info(f"Number bank size: {len(number_bank)}")
        
        # Verify empty cells match number bank
        empty_count = sum(1 for row in self.grid for cell in row if cell.get('isEmpty', False))
        if empty_count != len(number_bank):
            logging.error(f"Mismatch between empty cells ({empty_count}) and number bank size ({len(number_bank)})")
            # Fix empty cells to match number bank
            self._fix_empty_cells(number_bank)
        
        return {
            'grid': self.grid,
            'equations': self.equations,
            'numberBank': sorted(number_bank),
            'gridSize': self.grid_size,
            'difficulty': difficulty
        }

    def _fix_empty_cells(self, number_bank: List[int]):
        """Fix empty cells to match number bank size."""
        # Count current empty cells
        empty_cells = [(r, c) for r in range(self.grid_size) 
                      for c in range(self.grid_size) 
                      if self.grid[r][c].get('isEmpty', False)]
        
        # If we have too many empty cells, mark some as fixed
        while len(empty_cells) > len(number_bank):
            row, col = empty_cells.pop()
            self.grid[row][col]['isEmpty'] = False
            self.grid[row][col]['isFixed'] = True
            if (row, col) in self.empty_cells:
                self.empty_cells.remove((row, col))

    def _generate_pattern(self, difficulty: str) -> None:
        """Generate the crossword pattern without numbers."""
        max_attempts = 30  # Increased attempts for more complex patterns
        
        for attempt in range(max_attempts):
            logging.info(f"\nAttempt {attempt + 1}/{max_attempts} to generate pattern")
            
            # Reset state for this attempt
            self.equations.clear()
            self.intersection_points.clear()
            self._used_cells.clear()
            
            # Start with a horizontal equation in the middle
            center_row = self.grid_size // 2
            h_pos = Position(center_row, 1, 'horizontal')
            
            if not self._place_first_equation(h_pos):
                continue
                
            # Add more equations based on difficulty
            target_equations = {
                'easy': 3,
                'medium': 6,
                'hard': 10
            }[difficulty]
            
            # Try to place additional equations
            placed_equations = 1
            max_placement_attempts = 50
            
            for _ in range(max_placement_attempts):
                if placed_equations >= target_equations:
                    break
                    
                # Alternate between horizontal and vertical equations
                orientation = 'vertical' if len(self.equations) % 2 == 1 else 'horizontal'
                
                # Find valid position for new equation
                valid_positions = []
                for row in range(1, self.grid_size - 4):
                    for col in range(1, self.grid_size - 4):
                        pos = Position(row, col, orientation)
                        cells = self._get_equation_cells(pos, 5)
                        if self._is_valid_equation_position(cells):
                            valid_positions.append(pos)
                
                if not valid_positions:
                    continue
                    
                # Try each position until we find one that works
                random.shuffle(valid_positions)
                equation_placed = False
                
                for pos in valid_positions:
                    if self._place_first_equation(pos):
                        placed_equations += 1
                        equation_placed = True
                        break
                        
                if not equation_placed:
                    continue
            
            # If we placed enough equations, we're done
            if placed_equations >= target_equations:
                logging.info(f"Successfully generated pattern with {placed_equations} equations")
                break
        else:
            raise ValueError(f"Could not generate valid pattern for {difficulty} difficulty")

    def _place_first_equation(self, pos: Position) -> bool:
        """Place first equation with random numbers."""
        cells = self._get_equation_cells(pos, 5)
        if not self._is_valid_equation_position(cells):
            logging.info(f"Invalid position for first equation at {pos}")
            return False
            
        operator = random.choice(self.OPERATORS)
        a, b, result = random.choice(self.VALID_EQUATIONS[operator])
        
        equation = Equation(pos, a, operator, b, result, cells)
        self.equations.append(equation)
        
        # Place equation in grid
        values = [a, operator, b, '=', result]
        for i, (row, col) in enumerate(cells):
            is_operator = i in [1, 3]
            self.grid[row][col].update({
                'value': values[i] if not is_operator else None,
                'isOperator': is_operator,
                'operator': values[i] if is_operator else None,
                'isFixed': False,
                'isResult': i == 4,
                'isEmpty': False,
                'inEquation': True,
                'isCorrect': False,
                'isIncorrect': False
            })
            self._used_cells.add((row, col))
        
        logging.info(f"Placed first equation: {a} {operator} {b} = {result}")
        return True

    def _place_second_equation(self, pos: Position, intersection_point: Tuple[int, int], intersection_value: int) -> bool:
        """Place second equation that must use the intersection value."""
        cells = self._get_equation_cells(pos, 5)
        if not self._is_valid_equation_position(cells):
            logging.info(f"Invalid position for second equation at {pos}")
            return False
            
        # Find which position in the equation is the intersection point
        intersection_idx = None
        for i, cell in enumerate(cells):
            if cell == intersection_point:
                intersection_idx = i
                break
        
        if intersection_idx is None or intersection_idx % 2 != 0:  # Must be a number position (0, 2, or 4)
            logging.info(f"Invalid intersection index {intersection_idx}")
            return False
            
        # Choose operator
        operator = random.choice(self.OPERATORS)
        
        # Find valid equation that uses intersection_value in the correct position
        valid_equations = self.VALID_EQUATIONS[operator]
        random.shuffle(valid_equations)
        
        for a, b, result in valid_equations:
            values = [a, b, result]
            if values[intersection_idx // 2] == intersection_value:
                # Found a valid equation
                equation = Equation(pos, a, operator, b, result, cells)
                self.equations.append(equation)
                
                # Place equation in grid
                values = [a, operator, b, '=', result]
                for i, (row, col) in enumerate(cells):
                    if (row, col) != intersection_point:  # Skip intersection point, it's already set
                        is_operator = i in [1, 3]
                        self.grid[row][col].update({
                            'value': values[i] if not is_operator else None,
                            'isOperator': is_operator,
                            'operator': values[i] if is_operator else None,
                            'isFixed': False,
                            'isResult': i == 4,
                            'isEmpty': False,
                            'inEquation': True,
                            'isCorrect': False,
                            'isIncorrect': False
                        })
                        self._used_cells.add((row, col))
                logging.info(f"Placed second equation: {a} {operator} {b} = {result}")
                return True
        
        logging.info(f"Could not find valid equation using {intersection_value} at position {intersection_idx}")
        return False

    def _fill_numbers(self) -> None:
        """Fill in numbers for all equations ensuring mathematical validity."""
        # First, handle intersecting equations
        for point in self.intersection_points:
            # Find equations that share this point
            shared_equations = []
            for eq in self.equations:
                if point in eq.cells:
                    shared_equations.append(eq)
            
            if len(shared_equations) == 2:
                self._fill_intersecting_equations(shared_equations[0], shared_equations[1], point)
        
        # Then fill remaining equations
        for eq in self.equations:
            if eq.a == 0:  # Not yet filled
                self._fill_single_equation(eq)

    def _fill_intersecting_equations(self, eq1: Equation, eq2: Equation, point: Tuple[int, int]) -> None:
        """Fill numbers for two intersecting equations."""
        # Find valid number for intersection point
        valid_numbers = set(range(1, 10))
        for num in valid_numbers:
            if self._try_fill_equations_with_intersection(eq1, eq2, point, num):
                break

    def _try_fill_equations_with_intersection(self, eq1: Equation, eq2: Equation, point: Tuple[int, int], num: int) -> bool:
        """Try to fill two equations using a specific number at intersection."""
        # Find position of intersection in each equation
        pos1 = eq1.cells.index(point)
        pos2 = eq2.cells.index(point)
        
        # Try valid equations that use this number in the correct position
        for a1, b1, r1 in self.VALID_EQUATIONS[eq1.operator]:
            nums1 = [a1, b1, r1]
            if nums1[pos1 // 2] == num:  # If number fits in correct position
                for a2, b2, r2 in self.VALID_EQUATIONS[eq2.operator]:
                    nums2 = [a2, b2, r2]
                    if nums2[pos2 // 2] == num:  # If number fits in correct position
                        # Fill equations
                        eq1.a, eq1.b, eq1.result = a1, b1, r1
                        eq2.a, eq2.b, eq2.result = a2, b2, r2
                        
                        # Update grid
                        self._update_equation_in_grid(eq1)
                        self._update_equation_in_grid(eq2)
                        return True
        return False

    def _fill_single_equation(self, equation: Equation) -> None:
        """Fill numbers for a single equation."""
        valid_equations = self.VALID_EQUATIONS[equation.operator]
        a, b, result = random.choice(valid_equations)
        equation.a, equation.b, equation.result = a, b, result
        self._update_equation_in_grid(equation)

    def _update_equation_in_grid(self, equation: Equation) -> None:
        """Update grid cells with equation numbers."""
        values = [equation.a, equation.operator, equation.b, '=', equation.result]
        for (row, col), value in zip(equation.cells, values):
            if not isinstance(value, str):  # If it's a number
                self.grid[row][col]['value'] = value

    def _hide_numbers(self, difficulty: str) -> List[int]:
        """Hide some numbers and return them as number bank."""
        number_bank = []
        self.empty_cells.clear()
        
        for equation in self.equations:
            # Determine which positions to hide (0=first number, 2=second number, 4=result)
            hide_positions = self._get_positions_to_hide(equation, difficulty)
            
            # Hide numbers and add to number bank
            for i, cell in enumerate(equation.cells):
                row, col = cell
                if i in hide_positions:
                    value = self.grid[row][col]['value']
                    if value is not None:  # Only add non-None values
                        self.grid[row][col]['value'] = None
                        self.grid[row][col]['isEmpty'] = True
                        self.grid[row][col]['isFixed'] = False
                        number_bank.append(value)
                        self.empty_cells.add(cell)
                elif not self.grid[row][col]['isOperator']:
                    # Mark non-operator cells as fixed if they're not hidden
                    self.grid[row][col]['isFixed'] = True
                    self.grid[row][col]['isEmpty'] = False
        
        return sorted(number_bank)

    def _get_positions_to_hide(self, equation: Equation, difficulty: str) -> List[int]:
        """Determine which positions to hide based on difficulty."""
        candidates = [0, 2, 4]  # Possible positions to hide (first number, second number, result)
        
        # For medium/hard, don't hide intersection points
        if difficulty != 'easy':
            candidates = [pos for pos in candidates 
                        if equation.cells[pos] not in self.intersection_points]
        
        # Always hide exactly 2 positions per equation
        # If we can't hide 2 positions (due to intersections), hide just 1
        num_to_hide = min(2, len(candidates))
        return random.sample(candidates, num_to_hide)

    def _get_equation_cells(self, position: Position, length: int) -> List[Tuple[int, int]]:
        """Get the cells that would be used by an equation."""
        cells = []
        for i in range(length):
            if position.orientation == 'horizontal':
                cells.append((position.row, position.col + i))
            else:
                cells.append((position.row + i, position.col))
        return cells

    def _is_valid_equation_position(self, cells: List[Tuple[int, int]]) -> bool:
        """Check if an equation can be placed at the given position."""
        # Check if all cells are within grid bounds
        if not all(0 <= row < self.grid_size and 0 <= col < self.grid_size for row, col in cells):
            return False
            
        # Check if any cell is already used by another equation
        if any((row, col) in self._used_cells for row, col in cells):
            return False
            
        # Check if there's enough space around the equation
        for row, col in cells:
            # Check adjacent cells (not including diagonals)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                adj_row, adj_col = row + dr, col + dc
                if (0 <= adj_row < self.grid_size and 
                    0 <= adj_col < self.grid_size and 
                    (adj_row, adj_col) in self._used_cells):
                    # Allow adjacent cells only for intersections at number positions
                    if (row, col) not in cells:
                        # Check if this is a potential intersection point
                        if cells.index((row, col)) % 2 == 0:  # Number position
                            continue
                        return False
        
        return True

    def _used_operators(self) -> Set[str]:
        """Return the set of used operators in the grid."""
        used_operators = set()
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.grid[row][col] and self.grid[row][col].get('isOperator', False):
                    used_operators.add(self.grid[row][col]['operator'])
        return used_operators

    def _used_numbers(self) -> Set[int]:
        """Return the set of used numbers in the grid."""
        used_numbers = set()
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.grid[row][col] and not self.grid[row][col].get('isOperator', False):
                    used_numbers.add(self.grid[row][col]['value'])
        return used_numbers

    def _score_puzzle(self, equations_placed: int, intersections: int, difficulty: str) -> int:
        """Score a puzzle based on its properties and difficulty."""
        base_score = equations_placed * 10
        
        if difficulty == 'easy':
            # For easy, we just want 2 equations
            if equations_placed >= 2:
                base_score += 20
        elif difficulty == 'medium':
            # For medium, prefer 2 equations with at least 1 intersection
            if equations_placed >= 2:
                base_score += 20
                if intersections > 0:
                    base_score += 10
        else:  # hard
            # For hard, prefer 2+ equations with intersections
            if equations_placed >= 2:
                base_score += 20
                base_score += intersections * 10
        
        return base_score

    def _get_minimum_score(self, difficulty: str) -> int:
        """Get the minimum acceptable score for a difficulty level."""
        return {
            'easy': 20,    # Just need 2 equations
            'medium': 35,  # 2 equations + 1 intersection
            'hard': 50     # 2 equations + 2 intersections
        }.get(difficulty, 20) 