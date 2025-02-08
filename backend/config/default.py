"""Default configuration for the Flask application."""

import os

# Flask settings
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')  # Change in production

# Game settings
MAX_GRID_SIZE = 8  # Based on the screenshot example
MAX_PLAYERS = 2
DIFFICULTY_LEVELS = ['easy', 'medium', 'hard']

# Game rules
VALID_OPERATORS = ['+', '-', '*', '/']
MIN_NUMBER = 1
MAX_NUMBER = 100  # Adjust based on difficulty 