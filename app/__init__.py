from flask import Flask
from flask_cors import CORS
from config import Config
from app.core.websocket import websocket_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize CORS
    CORS(app)
    
    # Initialize WebSocket
    websocket_manager.init_app(app)
    
    # Register blueprints
    from app.modules.xendit import create_xendit_blueprint
    app.register_blueprint(create_xendit_blueprint(), url_prefix='/api/xendit')
    
    return app
