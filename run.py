from app import create_app
from app.core.websocket import websocket_manager

app = create_app()

if __name__ == '__main__':
    websocket_manager.run_app(app, host='0.0.0.0', port=5000, debug=True)
