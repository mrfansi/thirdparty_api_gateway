import os

# Test configuration
os.environ['XENDIT_API_KEY'] = 'test_key'
os.environ['XENDIT_API_BASE_URL'] = 'https://api.xendit.co'

# Create a Flask test app
from flask import Flask

def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app
