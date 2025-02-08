from flask import Flask
from flask_cors import CORS

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configure CORS to allow requests from any origin
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Configure app
    app.config.from_object('config.default')
    
    # Register routes
    from .routes import game
    app.register_blueprint(game.bp)

    return app 