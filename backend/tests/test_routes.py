import pytest
import json

def test_new_game_endpoint(client):
    """Test the new game generation endpoint."""
    # Test with valid difficulty
    response = client.get('/api/newGame?difficulty=medium')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'gameId' in data
    assert 'grid' in data
    assert 'numberBank' in data
    assert 'difficulty' in data
    assert data['difficulty'] == 'medium'

    # Test with invalid difficulty
    response = client.get('/api/newGame?difficulty=invalid')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_validate_move_endpoint(client):
    """Test the move validation endpoint."""
    # First create a game
    response = client.get('/api/newGame?difficulty=medium')
    assert response.status_code == 200
    game_data = json.loads(response.data)
    game_id = game_data['gameId']

    # Test with valid move data
    move_data = {
        'gameId': game_id,
        'row': 0,
        'col': 0,
        'value': 5
    }
    response = client.post('/api/validateMove',
                          data=json.dumps(move_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'valid' in data

    # Test with invalid move data
    invalid_data = {
        'row': 0,
        # Missing gameId, col, and value
    }
    response = client.post('/api/validateMove',
                          data=json.dumps(invalid_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

    # Test with non-existent game
    invalid_game_data = {
        'gameId': 'non-existent-id',
        'row': 0,
        'col': 0,
        'value': 5
    }
    response = client.post('/api/validateMove',
                          data=json.dumps(invalid_game_data),
                          content_type='application/json')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_game_state_endpoint(client):
    """Test the game state endpoint."""
    # First create a game
    response = client.get('/api/newGame?difficulty=medium')
    assert response.status_code == 200
    game_data = json.loads(response.data)
    game_id = game_data['gameId']

    # Test with valid game ID
    response = client.get(f'/api/gameState?gameId={game_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'gameId' in data
    assert 'grid' in data
    assert 'numberBank' in data
    assert 'difficulty' in data

    # Test with missing game ID
    response = client.get('/api/gameState')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

    # Test with non-existent game ID
    response = client.get('/api/gameState?gameId=non-existent-id')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_clear_cell_endpoint(client):
    """Test the clear cell endpoint."""
    # First create a game
    response = client.get('/api/newGame?difficulty=medium')
    assert response.status_code == 200
    game_data = json.loads(response.data)
    game_id = game_data['gameId']

    # Test with valid clear cell data
    clear_data = {
        'gameId': game_id,
        'row': 0,
        'col': 0
    }
    response = client.post('/api/clearCell',
                          data=json.dumps(clear_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'valid' in data

    # Test with invalid clear cell data
    invalid_data = {
        'row': 0,
        # Missing gameId and col
    }
    response = client.post('/api/clearCell',
                          data=json.dumps(invalid_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

    # Test with non-existent game
    invalid_game_data = {
        'gameId': 'non-existent-id',
        'row': 0,
        'col': 0
    }
    response = client.post('/api/clearCell',
                          data=json.dumps(invalid_game_data),
                          content_type='application/json')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_new_game_endpoint_basic(client):
    """Test basic functionality of new game generation endpoint."""
    # Test with valid difficulty
    response = client.get('/api/newGame?difficulty=medium')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'gameId' in data
    assert 'grid' in data
    assert 'numberBank' in data
    assert 'difficulty' in data
    assert data['difficulty'] == 'medium'

    # Test with invalid difficulty
    response = client.get('/api/newGame?difficulty=invalid')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_new_game_puzzle_structure(client):
    """Test that generated puzzles have correct structure and properties."""
    # Test for each difficulty level
    for difficulty in ['easy', 'medium', 'hard']:
        response = client.get(f'/api/newGame?difficulty={difficulty}')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Check grid structure
        assert isinstance(data['grid'], list)
        assert len(data['grid']) == 11  # Updated grid size
        assert all(len(row) == 11 for row in data['grid'])
        
        # Check number bank
        assert isinstance(data['numberBank'], list)
        assert all(isinstance(n, int) for n in data['numberBank'])
        assert all(1 <= n <= 15 for n in data['numberBank'])  # Updated number range
        
        # Find equations in grid
        equations = []
        intersection_points = set()
        
        # Helper function to check if cell is part of equation
        def is_equation_cell(cell):
            return cell and cell.get('inEquation', False)
        
        # Find horizontal equations
        for row_idx, row in enumerate(data['grid']):
            for col_idx in range(len(row) - 4):  # -4 because equation needs 5 cells
                cells = [row[col_idx + i] for i in range(5)]
                if all(is_equation_cell(cell) for cell in cells):
                    equations.append(('horizontal', row_idx, col_idx))
        
        # Find vertical equations
        for col_idx in range(len(data['grid'][0])):
            for row_idx in range(len(data['grid']) - 4):
                cells = [data['grid'][row_idx + i][col_idx] for i in range(5)]
                if all(is_equation_cell(cell) for cell in cells):
                    equations.append(('vertical', row_idx, col_idx))
        
        # Find intersection points
        for eq1 in equations:
            for eq2 in equations:
                if eq1[0] != eq2[0]:  # Different orientations
                    if eq1[0] == 'horizontal':
                        h_eq, v_eq = eq1, eq2
                    else:
                        h_eq, v_eq = eq2, eq1
                    
                    # Check if equations intersect
                    h_row = h_eq[1]
                    h_start_col = h_eq[2]
                    v_col = v_eq[2]
                    v_start_row = v_eq[1]
                    
                    if (v_start_row <= h_row <= v_start_row + 4 and 
                        h_start_col <= v_col <= h_start_col + 4):
                        intersection_points.add((h_row, v_col))
        
        # Verify puzzle properties based on difficulty
        min_equations = {
            'easy': 3,
            'medium': 6,
            'hard': 10
        }[difficulty]
        
        assert len(equations) >= min_equations  # Each difficulty should have minimum number of equations
        
        # Intersections are optional for easy difficulty
        if difficulty != 'easy':
            assert len(intersection_points) > 0  # Medium and hard should have intersections
        
        # Verify number bank matches empty cells
        empty_cells = sum(1 for row in data['grid'] 
                         for cell in row 
                         if cell.get('isEmpty', False))
        assert len(data['numberBank']) == empty_cells

def test_new_game_equation_validity(client):
    """Test that generated equations are mathematically valid."""
    response = client.get('/api/newGame?difficulty=easy')
    assert response.status_code == 200
    data = json.loads(response.data)
    
    def find_equation_values(cells):
        values = []
        operator = None
        for cell in cells:
            if cell['isOperator']:
                if cell['operator'] != '=':
                    operator = cell['operator']
            else:
                if not cell['isEmpty']:
                    values.append(cell['value'])
        return values, operator
    
    # Check horizontal equations
    for row_idx, row in enumerate(data['grid']):
        for col_idx in range(len(row) - 4):
            cells = [row[col_idx + i] for i in range(5)]
            if all(cell.get('inEquation', False) for cell in cells):
                values, operator = find_equation_values(cells)
                if len(values) == 3 and operator:  # If equation is complete
                    # Verify equation is valid
                    if operator == '+':
                        assert values[0] + values[1] == values[2]
                    elif operator == '-':
                        assert values[0] - values[1] == values[2]
                    elif operator == '*':
                        assert values[0] * values[1] == values[2]
    
    # Check vertical equations
    for col_idx in range(len(data['grid'][0])):
        for row_idx in range(len(data['grid']) - 4):
            cells = [data['grid'][row_idx + i][col_idx] for i in range(5)]
            if all(cell.get('inEquation', False) for cell in cells):
                values, operator = find_equation_values(cells)
                if len(values) == 3 and operator:  # If equation is complete
                    # Verify equation is valid
                    if operator == '+':
                        assert values[0] + values[1] == values[2]
                    elif operator == '-':
                        assert values[0] - values[1] == values[2]
                    elif operator == '*':
                        assert values[0] * values[1] == values[2] 