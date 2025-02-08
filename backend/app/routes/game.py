from flask import Blueprint, jsonify, request
from ..game.puzzle_generator import PuzzleGenerator
from ..game.game_state import GameStateManager, Move
import logging

bp = Blueprint('game', __name__, url_prefix='/api')
puzzle_generator = PuzzleGenerator()
game_manager = GameStateManager()

@bp.route('/newGame', methods=['GET'])
def new_game():
    """Generate a new game with specified difficulty."""
    difficulty = request.args.get('difficulty', 'medium')
    logging.info(f'=== New game requested with difficulty: {difficulty} ===')
    
    if difficulty not in ['easy', 'medium', 'hard']:
        logging.error(f'Invalid difficulty level: {difficulty}')
        return jsonify({'error': 'Invalid difficulty level'}), 400

    try:
        # Generate new puzzle
        logging.info('Generating new puzzle...')
        puzzle = puzzle_generator.generate_puzzle(difficulty)
        logging.info(f'Puzzle generated successfully')
        
        # Create new game state
        game = game_manager.create_game(puzzle, difficulty)
        
        # Create response
        response = {
            'gameId': game.id,
            'grid': puzzle['grid'],
            'numberBank': puzzle['numberBank'],
            'difficulty': difficulty,
            'gridSize': puzzle['gridSize']
        }
        
        return jsonify(response)
        
    except Exception as e:
        logging.error(f'Error generating puzzle: {str(e)}')
        return jsonify({'error': str(e)}), 500

@bp.route('/validateMove', methods=['POST'])
def validate_move():
    """Validate a player's move."""
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['gameId', 'row', 'col', 'value']):
            return jsonify({'error': 'Invalid move data'}), 400

        game = game_manager.get_game(data['gameId'])
        if not game:
            return jsonify({'error': 'Game not found'}), 404

        move = Move(data['row'], data['col'], data['value'])
        result = game.validate_move(move)
        
        # Log the move and result
        logging.info(f'Move validation: row={move.row}, col={move.col}, value={move.value}')
        logging.info(f'Validation result: {result}')
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f'Error validating move: {str(e)}')
        return jsonify({'error': str(e)}), 500

@bp.route('/clearCell', methods=['POST'])
def clear_cell():
    """Clear a cell in the grid."""
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['gameId', 'row', 'col']):
            return jsonify({'error': 'Invalid clear cell data'}), 400

        game = game_manager.get_game(data['gameId'])
        if not game:
            return jsonify({'error': 'Game not found'}), 404

        result = game.clear_cell(data['row'], data['col'])
        
        # Log the clear operation and result
        logging.info(f'Clear cell: row={data["row"]}, col={data["col"]}')
        logging.info(f'Clear result: {result}')
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f'Error clearing cell: {str(e)}')
        return jsonify({'error': str(e)}), 500

@bp.route('/gameState', methods=['GET'])
def get_game_state():
    """Get the current game state."""
    try:
        game_id = request.args.get('gameId')
        if not game_id:
            return jsonify({'error': 'Game ID is required'}), 400

        game = game_manager.get_game(game_id)
        if not game:
            return jsonify({'error': 'Game not found'}), 404

        return jsonify({
            'gameId': game.id,
            'grid': game.grid,
            'numberBank': game.number_bank,
            'difficulty': game.difficulty
        })
        
    except Exception as e:
        logging.error(f'Error getting game state: {str(e)}')
        return jsonify({'error': str(e)}), 500 