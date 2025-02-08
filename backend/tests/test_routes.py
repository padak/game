import pytest
import json

def test_new_game_endpoint(client):
    """Test the new game generation endpoint."""
    # Test with valid difficulty
    response = client.get('/api/newGame?difficulty=medium')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'grid' in data
    assert 'equations' in data
    assert 'numberBank' in data

    # Test with invalid difficulty
    response = client.get('/api/newGame?difficulty=invalid')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_validate_move_endpoint(client):
    """Test the move validation endpoint."""
    # Test with valid move data
    move_data = {
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
        # Missing 'col' and 'value'
    }
    response = client.post('/api/validateMove',
                          data=json.dumps(invalid_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_game_state_endpoint(client):
    """Test the game state endpoint."""
    response = client.get('/api/gameState')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data  # Currently returns placeholder message 