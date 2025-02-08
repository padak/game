import pytest
from app.game.game_state import GameState, GameStateManager, Move
import time

@pytest.fixture
def sample_puzzle():
    return {
        'grid': [
            [
                {'value': 2, 'isFixed': True, 'isOperator': False},
                {'value': None, 'isOperator': True, 'operator': '+'},
                {'value': None, 'isFixed': False, 'isOperator': False},
                {'value': None, 'isOperator': True, 'operator': '='},
                {'value': 5, 'isFixed': True, 'isOperator': False, 'isResult': True}
            ]
        ],
        'equations': [],
        'numberBank': [1, 2, 3, 4, 5]
    }

@pytest.fixture
def game_state(sample_puzzle):
    return GameState(
        grid=sample_puzzle['grid'],
        equations=sample_puzzle['equations'],
        number_bank=sample_puzzle['numberBank'],
        difficulty='medium'
    )

def test_game_state_initialization(game_state):
    """Test game state initialization."""
    assert game_state.id is not None
    assert len(game_state.grid) == 1
    assert len(game_state.grid[0]) == 5
    assert game_state.difficulty == 'medium'
    assert len(game_state.number_bank) == 5
    assert len(game_state.moves) == 0

def test_valid_move(game_state):
    """Test making a valid move."""
    move = Move(0, 2, 3)  # Complete equation 2 + 3 = 5
    result = game_state.validate_move(move)
    
    assert result['valid'] is True
    assert 3 not in result['numberBank']
    assert result['grid'][0][2]['value'] == 3
    assert len(result['affectedEquations']) == 1
    assert result['affectedEquations'][0]['isValid'] is True

def test_invalid_move_operator_cell(game_state):
    """Test attempting to place number in operator cell."""
    move = Move(0, 1, 3)  # Try to place in operator cell
    result = game_state.validate_move(move)
    
    assert result['valid'] is False
    assert 'error' in result
    assert 3 in game_state.number_bank

def test_invalid_move_fixed_cell(game_state):
    """Test attempting to place number in fixed cell."""
    move = Move(0, 0, 3)  # Try to place in fixed cell
    result = game_state.validate_move(move)
    
    assert result['valid'] is False
    assert 'error' in result
    assert 3 in game_state.number_bank

def test_invalid_move_unavailable_number(game_state):
    """Test attempting to use unavailable number."""
    move = Move(0, 2, 9)  # 9 is not in number bank
    result = game_state.validate_move(move)
    
    assert result['valid'] is False
    assert 'error' in result
    assert game_state.grid[0][2]['value'] is None

def test_clear_cell(game_state):
    """Test clearing a cell."""
    # First place a number
    game_state.validate_move(Move(0, 2, 3))
    
    # Then clear it
    result = game_state.clear_cell(0, 2)
    
    assert result['valid'] is True
    assert 3 in result['numberBank']
    assert result['grid'][0][2]['value'] is None

def test_clear_invalid_cell(game_state):
    """Test attempting to clear invalid cells."""
    # Try to clear operator cell
    result = game_state.clear_cell(0, 1)
    assert result['valid'] is False
    
    # Try to clear fixed cell
    result = game_state.clear_cell(0, 0)
    assert result['valid'] is False

def test_game_state_manager():
    """Test game state manager functionality."""
    manager = GameStateManager()
    puzzle = {
        'grid': [[{'value': None}]],
        'equations': [],
        'numberBank': [1, 2, 3]
    }
    
    # Create game
    game = manager.create_game(puzzle, 'easy')
    assert game.id in manager.active_games
    
    # Get game
    retrieved_game = manager.get_game(game.id)
    assert retrieved_game is game
    
    # Test cleanup of old games
    game.last_activity = time.time() - 3700  # Older than cleanup threshold
    manager._cleanup_old_games()
    assert game.id not in manager.active_games

def test_equation_validation(game_state):
    """Test equation validation logic."""
    # Place correct number
    move = Move(0, 2, 3)  # Makes 2 + 3 = 5
    result = game_state.validate_move(move)
    assert result['affectedEquations'][0]['isValid'] is True
    
    # Place incorrect number
    game_state.clear_cell(0, 2)
    move = Move(0, 2, 4)  # Makes 2 + 4 = 5 (incorrect)
    result = game_state.validate_move(move)
    assert result['affectedEquations'][0]['isValid'] is False 