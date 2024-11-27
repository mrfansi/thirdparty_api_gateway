from flask import Blueprint
from .controller import bp as xendit_bp
from .websocket import init_xendit_websocket

def create_xendit_blueprint():
    """Create and configure the Xendit blueprint"""
    # Initialize WebSocket handlers
    init_xendit_websocket()
    return xendit_bp
