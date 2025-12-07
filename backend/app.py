#!/usr/bin/env python3
"""
TalkGuest Backend API
=====================
Flask-based REST API for hospitality data processing and analysis.
"""

import os
from flask import Flask
from flask_cors import CORS

from routers.upload import upload_bp
from routers.process import process_bp
from routers.results import results_bp
from routers.download import download_bp
from routers.health import health_bp


def create_app(config=None):
    """Application factory for creating Flask app."""
    app = Flask(__name__)
    
    # Default configuration
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
    app.config['DATA_STORAGE'] = {}  # In-memory storage for uploaded files and results
    
    # Apply custom config if provided
    if config:
        app.config.update(config)
    
    # Enable CORS for frontend communication
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000", 
                "http://frontend:3000",
                "https://talkguest-automate-webapp.onrender.com",
                "https://*.onrender.com",
                "https://talkguest-webapp-frontend-production.up.railway.app",
                "https://*.railway.app"
            ],
            "methods": ["GET", "POST", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(process_bp, url_prefix='/api')
    app.register_blueprint(results_bp, url_prefix='/api')
    app.register_blueprint(download_bp, url_prefix='/api')
    
    # Disable caching for all responses
    @app.after_request
    def add_header(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return app


# Create app instance for running directly
app = create_app()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
