from flask import Blueprint, jsonify, request
from ..game.puzzle_generator import PuzzleGenerator

bp = Blueprint('game', __name__, url_prefix='/api')
puzzle_generator = PuzzleGenerator()

@bp.route('/newGame', methods=['GET'])
def new_game():
    """Generate a new game with specified difficulty."""
    difficulty = request.args.get('difficulty', 'medium')
    if difficulty not in ['easy', 'medium', 'hard']:
        return jsonify({'error': 'Invalid difficulty level'}), 400

    try:
        puzzle = puzzle_generator.generate_puzzle(difficulty)
        return jsonify(puzzle)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/validateMove', methods=['POST'])
def validate_move():
    """Validate a player's move."""
    data = request.get_json()
    if not data or 'row' not in data or 'col' not in data or 'value' not in data:
        return jsonify({'error': 'Invalid move data'}), 400

    # TODO: Implement move validation
    # For now, return success
    return jsonify({'valid': True})

@bp.route('/gameState', methods=['GET'])
def get_game_state():
    """Get the current game state."""
    # TODO: Implement game state retrieval
    return jsonify({'message': 'Game state endpoint - To be implemented'}) 