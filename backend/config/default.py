"""Default configuration for the Flask application."""

import os

# Flask settings
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')  # Change in production

# Game settings
MAX_GRID_SIZE = 11  # Increased to match example
MAX_PLAYERS = 2
DIFFICULTY_LEVELS = ['easy', 'medium', 'hard']

# Game rules
VALID_OPERATORS = ['+', '-', '*']  # Removed division for simplicity
MIN_NUMBER = 1
MAX_NUMBER = 15  # Adjusted based on example

# Equation counts per difficulty
EQUATION_COUNTS = {
    'easy': 3,
    'medium': 6,
    'hard': 10
}

# Pre-fill settings per difficulty
PREFILL_PERCENTAGES = {
    'easy': 0.7,    # 70% of numbers pre-filled
    'medium': 0.5,  # 50% of numbers pre-filled
    'hard': 0.3     # 30% of numbers pre-filled
} 