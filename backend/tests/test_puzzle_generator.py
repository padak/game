import pytest
from app.game.puzzle_generator import PuzzleGenerator, Position, Equation

def test_puzzle_initialization():
    """Test basic puzzle generator initialization."""
    generator = PuzzleGenerator(grid_size=8)
    assert generator.grid_size == 8
    assert len(generator.grid) == 8
    assert len(generator.grid[0]) == 8
    assert len(generator.used_cells) == 0
    assert len(generator.equations) == 0

def test_equation_count_by_difficulty():
    """Test that different difficulties generate appropriate number of equations."""
    generator = PuzzleGenerator(grid_size=6)  # Smaller grid for faster tests
    
    # Test each difficulty once
    difficulties = ['easy', 'medium', 'hard']
    expected_counts = {'easy': 2, 'medium': 3, 'hard': 4}
    
    for difficulty in difficulties:
        puzzle = generator.generate_puzzle(difficulty)
        assert len(puzzle['equations']) <= expected_counts[difficulty]

def test_valid_equation_generation():
    """Test that generated equations are mathematically valid."""
    generator = PuzzleGenerator(grid_size=6)  # Smaller grid for faster tests
    puzzle = generator.generate_puzzle('easy')  # Use easy difficulty for faster tests
    
    for eq in puzzle['equations']:
        # Check equation validity based on operator
        if eq.operator == '+':
            assert eq.a + eq.b == eq.result
        elif eq.operator == '-':
            assert eq.a - eq.b == eq.result
        elif eq.operator == '*':
            assert eq.a * eq.b == eq.result

def test_number_bank_generation():
    """Test that number bank contains all necessary numbers."""
    generator = PuzzleGenerator(grid_size=6)  # Smaller grid for faster tests
    puzzle = generator.generate_puzzle('easy')  # Use easy difficulty for faster tests
    
    # Collect all numbers used in equations
    used_numbers = set()
    for eq in puzzle['equations']:
        used_numbers.add(eq.a)
        used_numbers.add(eq.b)
        used_numbers.add(eq.result)
    
    # Check that all used numbers are in the number bank
    for num in used_numbers:
        assert num in puzzle['numberBank']

def test_grid_cell_placement():
    """Test that equations are properly placed in the grid."""
    generator = PuzzleGenerator(grid_size=6)  # Smaller grid for faster tests
    puzzle = generator.generate_puzzle('easy')  # Use easy difficulty for faster tests
    
    # Check that each equation's cells are properly placed
    for eq in puzzle['equations']:
        # Check first number (A)
        cell_a = puzzle['grid'][eq.cells[0][0]][eq.cells[0][1]]
        assert cell_a['value'] == eq.a
        assert not cell_a['isOperator']
        
        # Check operator
        cell_op = puzzle['grid'][eq.cells[1][0]][eq.cells[1][1]]
        assert cell_op['isOperator']
        assert cell_op['operator'] == eq.operator
        
        # Check second number (B)
        cell_b = puzzle['grid'][eq.cells[2][0]][eq.cells[2][1]]
        assert cell_b['value'] == eq.b
        assert not cell_b['isOperator']
        
        # Check equals sign
        cell_eq = puzzle['grid'][eq.cells[3][0]][eq.cells[3][1]]
        assert cell_eq['isOperator']
        assert cell_eq['operator'] == '='
        
        # Check result
        cell_result = puzzle['grid'][eq.cells[4][0]][eq.cells[4][1]]
        assert cell_result['value'] == eq.result
        assert not cell_result['isOperator']
        assert cell_result['isResult']

def test_intersection_handling():
    """Test that intersecting equations are properly handled."""
    generator = PuzzleGenerator(grid_size=6)  # Smaller grid for faster tests
    
    # Create a horizontal equation
    pos1 = Position(row=2, col=0, orientation='horizontal')
    eq1 = Equation(pos1, a=3, operator='*', b=4, result=12,
                  cells=generator._get_equation_cells(pos1, 5))
    
    # Place the first equation
    assert generator._place_equation(eq1)
    generator.equations.append(eq1)
    for cell in eq1.cells:
        if cell not in generator.cell_equations:
            generator.cell_equations[cell] = []
        generator.cell_equations[cell].append(eq1)
    
    # Find intersections for a vertical equation that would cross
    pos2 = Position(row=0, col=2, orientation='vertical')
    intersections = generator._find_intersections(pos2)
    
    # Should find the intersection with b=4 from first equation
    assert len(intersections) > 0
    intersection_found = False
    for (row, col), value in intersections:
        if row == 2 and col == 2:  # Position where equations would cross
            assert value == 4  # The 'b' value from first equation
            intersection_found = True
    assert intersection_found

def test_grid_boundaries():
    """Test that equations stay within grid boundaries."""
    generator = PuzzleGenerator(grid_size=6)  # Smaller grid for faster tests
    puzzle = generator.generate_puzzle('easy')  # Use easy difficulty for faster tests
    
    # Check that no equation goes out of bounds
    for eq in puzzle['equations']:
        for row, col in eq.cells:
            assert 0 <= row < 6
            assert 0 <= col < 6

def test_positive_numbers():
    """Test that only positive numbers are generated."""
    generator = PuzzleGenerator(grid_size=6)  # Smaller grid for faster tests
    puzzle = generator.generate_puzzle('easy')  # Use easy difficulty for faster tests
    
    # Check all numbers in equations
    for eq in puzzle['equations']:
        assert eq.a > 0
        assert eq.b > 0
        assert eq.result > 0
    
    # Check number bank
    assert all(num > 0 for num in puzzle['numberBank']) 