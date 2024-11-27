from typing import Dict, Any, Optional, Callable
from flask_socketio import SocketIO, emit, join_room, leave_room
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self._socketio: Optional[SocketIO] = None
        self._event_handlers: Dict[str, Dict[str, Callable]] = {}
        
    def init_app(self, app):
        """Initialize SocketIO with the Flask app"""
        self._socketio = SocketIO(app, cors_allowed_origins="*")
        self._register_handlers()
        
    def _register_handlers(self):
        """Register all event handlers with SocketIO"""
        for namespace, handlers in self._event_handlers.items():
            for event, handler in handlers.items():
                self._socketio.on_event(event, handler, namespace=namespace)
    
    def register_handler(self, event: str, handler: Callable, namespace: str = '/'):
        """Register a new event handler"""
        if namespace not in self._event_handlers:
            self._event_handlers[namespace] = {}
        
        self._event_handlers[namespace][event] = handler
        
        if self._socketio:
            self._socketio.on_event(event, handler, namespace=namespace)
    
    def emit(self, event: str, data: Dict[str, Any], room: Optional[str] = None, 
            namespace: str = '/', **kwargs):
        """Emit an event to connected clients"""
        try:
            if room:
                self._socketio.emit(event, data, room=room, namespace=namespace, **kwargs)
            else:
                self._socketio.emit(event, data, namespace=namespace, **kwargs)
        except Exception as e:
            logger.error(f"Error emitting event {event}: {str(e)}")
            raise
    
    def run_app(self, app, **kwargs):
        """Run the Flask app with SocketIO support"""
        if not self._socketio:
            self.init_app(app)
        self._socketio.run(app, **kwargs)

# Create a singleton instance
websocket_manager = WebSocketManager()

def ws_auth_required(f):
    """Decorator to check WebSocket authentication"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not getattr(f, 'auth_checked', False):
            # Implement your authentication logic here
            # For example, check session or token
            pass
        return f(*args, **kwargs)
    return wrapped

def join_ws_room(room_id: str):
    """Join a WebSocket room"""
    join_room(room_id)
    logger.info(f"Client joined room: {room_id}")

def leave_ws_room(room_id: str):
    """Leave a WebSocket room"""
    leave_room(room_id)
    logger.info(f"Client left room: {room_id}")

def emit_to_room(room_id: str, event: str, data: Dict[str, Any], **kwargs):
    """Emit an event to a specific room"""
    websocket_manager.emit(event, data, room=room_id, **kwargs)
