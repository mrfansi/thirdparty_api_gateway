import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Third-party API configurations
    
    # Xendit API
    XENDIT_API_KEY = os.environ.get('XENDIT_API_KEY')
    XENDIT_API_BASE_URL = os.environ.get('XENDIT_API_BASE_URL', 'https://api.xendit.co')
    
    # Add other third-party API configurations here
    # Example:
    # SHIPPING_API_KEY = os.environ.get('SHIPPING_API_KEY')
    # SHIPPING_API_BASE_URL = os.environ.get('SHIPPING_API_BASE_URL')
    
    API_CONFIGS = {
        'xendit': {
            'api_key': XENDIT_API_KEY,
            'base_url': XENDIT_API_BASE_URL
        }
    }

    @classmethod
    def get_api_config(cls, service_name: str) -> dict:
        """Get API configuration for a specific service."""
        config = cls.API_CONFIGS.get(service_name)
        if not config:
            raise ValueError(f"Configuration for service '{service_name}' not found")
        return config
