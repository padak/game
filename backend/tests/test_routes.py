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