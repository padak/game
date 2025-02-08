from flask import Flask
from flask_cors import CORS

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Configure app
    app.config.from_object('config.default')
    
    # Register routes (will be implemented later)
    from .routes import game
    app.register_blueprint(game.bp)

    return app 