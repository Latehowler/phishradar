"""
Entry point for the Phishing Detection System
Run this file to start the Flask application
"""
import os
import sys
from app.app import create_app

if __name__ == '__main__':
    # Set environment
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Create app
    app = create_app(env)
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.debug
    )
