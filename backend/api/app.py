import os
from flask import Flask
from flask_cors import CORS


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY', 'change-me-in-production'
    )
    CORS(app)

    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

