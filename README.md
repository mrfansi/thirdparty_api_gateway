# Third Party API Gateway

A Flask-based API gateway boilerplate for handling multiple third-party API integrations following SOLID principles and clean architecture.

## Features

- Modular architecture for multiple third-party API integrations
- Clean separation of concerns following SOLID principles
- Centralized configuration management
- Type hints and data validation
- Error handling and custom exceptions
- Standardized API responses
- Extensible base classes for rapid development
- Built-in request/response logging
- Comprehensive error handling
- Environment-based configuration
- WebSocket support for real-time communication

## Table of Contents

- [Third Party API Gateway](#third-party-api-gateway)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Setup](#setup)
  - [Adding a New API Integration](#adding-a-new-api-integration)
    - [1. Module Structure](#1-module-structure)
    - [2. Configuration](#2-configuration)
    - [3. Implementation Steps](#3-implementation-steps)
  - [Testing](#testing)
    - [1. Unit Tests](#1-unit-tests)
    - [2. Integration Tests](#2-integration-tests)
  - [Debugging](#debugging)
    - [1. Enable Debug Mode](#1-enable-debug-mode)
    - [2. Logging](#2-logging)
  - [Deployment](#deployment)
    - [1. Production Configuration](#1-production-configuration)
    - [2. Gunicorn Configuration](#2-gunicorn-configuration)
    - [3. Docker Support](#3-docker-support)
  - [Advanced Usage](#advanced-usage)
    - [1. Rate Limiting](#1-rate-limiting)
    - [2. Caching](#2-caching)
    - [3. Batch Processing](#3-batch-processing)
  - [API Response Format](#api-response-format)
  - [Example Endpoints](#example-endpoints)
    - [Payment API (Example)](#payment-api-example)
  - [Error Handling](#error-handling)
  - [WebSocket Support](#websocket-support)
    - [WebSocket Features](#websocket-features)
    - [Using WebSocket in Modules](#using-websocket-in-modules)
    - [Client-Side Connection](#client-side-connection)
    - [Available WebSocket Events](#available-websocket-events)
      - [Payment Module Events](#payment-module-events)
  - [Best Practices](#best-practices)
  - [Contributing](#contributing)
  - [License](#license)

## Project Structure

```
app/
├── __init__.py                 # Main application factory
├── core/                       # Core components
│   ├── controller.py           # Base controller
│   ├── dto.py                 # Data transfer objects
│   ├── exceptions.py          # Custom exceptions
│   ├── interfaces.py          # Abstract interfaces
│   └── third_party.py         # Base third-party API client
└── modules/                    # API modules
    └── payment/               # Example payment module
        ├── __init__.py
        ├── api.py             # Payment API client
        ├── controller.py      # Payment endpoints
        ├── schemas.py         # Payment data schemas
        └── use_cases.py       # Payment business logic
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your API keys and configurations
```

4. Initialize the application:
```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

## Adding a New API Integration

### 1. Module Structure

Create a new module with this structure:
```
app/modules/your_api/
├── __init__.py          # Module initialization
├── api.py              # API client implementation
├── controller.py       # HTTP endpoints
├── schemas.py          # Data models
├── use_cases.py        # Business logic
└── tests/              # Module tests
```

### 2. Configuration

Add to `config.py`:
```python
class Config:
    YOURAPI_API_KEY = os.environ.get('YOURAPI_API_KEY')
    YOURAPI_BASE_URL = os.environ.get('YOURAPI_BASE_URL')

    @classmethod
    def get_api_config(cls, service_name: str) -> dict:
        config_map = {
            'your_api': {
                'api_key': cls.YOURAPI_API_KEY,
                'base_url': cls.YOURAPI_BASE_URL
            }
        }
```

### 3. Implementation Steps

1. **API Client** (`api.py`):
```python
from app.core.third_party import ThirdPartyAPI
from config import Config

class YourAPI(ThirdPartyAPI):
    def __init__(self):
        config = Config.get_api_config('your_api')
        if not config.get('api_key'):
            raise ValueError("API key is not configured")
            
        super().__init__(
            base_url=config['base_url'],
            api_key=config['api_key']
        )
    
    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def your_method(self, param: str) -> Dict[str, Any]:
        return self._make_request(
            method="POST",
            endpoint="/your-endpoint",
            json={"param": param}
        )
```

2. **Schemas** (`schemas.py`):
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class YourRequestSchema:
    param: str
    optional_param: Optional[str] = None

@dataclass
class YourResponseSchema:
    id: str
    status: str
    created_at: str
```

3. **Use Cases** (`use_cases.py`):
```python
from app.core.interfaces import UseCase
from app.core.dto import ResponseDTO
from .schemas import YourRequestSchema, YourResponseSchema

class YourUseCase(UseCase):
    def __init__(self):
        self.api = YourAPI()

    def execute(self, request_dto: RequestDTO) -> ResponseDTO:
        # Validate and transform input
        request = YourRequestSchema(**request_dto.data)
        
        # Call API
        result = self.api.your_method(request.param)
        
        # Transform response
        response = YourResponseSchema(**result)
        
        return ResponseDTO.success(data=response.__dict__)
```

4. **Controller** (`controller.py`):
```python
from flask import Blueprint, request
from app.core.controller import BaseController
from app.core.dto import RequestDTO
from app.core.exceptions import ValidationException

class YourController(BaseController):
    def __init__(self):
        super().__init__()
        self.use_case = YourUseCase()

    def your_endpoint(self):
        if not request.is_json:
            raise ValidationException("Content-Type must be application/json")
        
        return self.handle_request(
            self.use_case.execute,
            RequestDTO(data=request.get_json())
        )

def create_your_blueprint() -> Blueprint:
    controller = YourController()
    blueprint = Blueprint('your_api', __name__)
    blueprint.route('/your-endpoint', methods=['POST'])(
        controller.your_endpoint
    )
    return blueprint
```

## Testing

### 1. Unit Tests

Create tests in `tests/` directory:

```python
# tests/test_your_api.py
import pytest
from app.modules.your_api.api import YourAPI
from app.modules.your_api.schemas import YourRequestSchema

def test_your_api_initialization():
    api = YourAPI()
    assert api.base_url == "expected_url"
    assert api.api_key == "expected_key"

def test_your_method():
    api = YourAPI()
    result = api.your_method("test_param")
    assert result["status"] == "success"
```

Run tests:
```bash
pytest tests/
```

### 2. Integration Tests

```python
# tests/integration/test_your_api_integration.py
def test_your_endpoint_integration(client):
    response = client.post('/api/v1/your-endpoint', json={
        "param": "test"
    })
    assert response.status_code == 200
    assert response.json["status"] == "success"
```

## Debugging

### 1. Enable Debug Mode

```bash
export FLASK_DEBUG=1
flask run
```

### 2. Logging

Add to your module:
```python
import logging

logger = logging.getLogger(__name__)

class YourAPI(ThirdPartyAPI):
    def your_method(self, param: str):
        logger.debug(f"Calling your_method with param: {param}")
        try:
            result = self._make_request(...)
            logger.info(f"API call successful: {result}")
            return result
        except Exception as e:
            logger.error(f"API call failed: {str(e)}")
            raise
```

## Deployment

### 1. Production Configuration

Create `config/production.py`:
```python
class ProductionConfig(Config):
    DEBUG = False
    # Add production-specific settings
```

### 2. Gunicorn Configuration

Create `gunicorn_config.py`:
```python
bind = "0.0.0.0:8000"
workers = 4
threads = 2
worker_class = "gthread"
timeout = 120
```

### 3. Docker Support

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["gunicorn", "--config", "gunicorn_config.py", "app:create_app()"]
```

## Advanced Usage

### 1. Rate Limiting

Add rate limiting to your API client:
```python
from functools import wraps
import time

def rate_limit(calls: int, period: float):
    def decorator(func):
        last_reset = time.time()
        calls_made = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_reset, calls_made
            
            now = time.time()
            if now - last_reset > period:
                calls_made = 0
                last_reset = now
                
            if calls_made >= calls:
                sleep_time = period - (now - last_reset)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                calls_made = 0
                last_reset = time.time()
                
            calls_made += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

class YourAPI(ThirdPartyAPI):
    @rate_limit(calls=100, period=60)  # 100 calls per minute
    def your_method(self, param: str):
        return self._make_request(...)
```

### 2. Caching

Add caching to your use cases:
```python
from functools import lru_cache
from datetime import datetime, timedelta

class YourUseCase(UseCase):
    def __init__(self):
        self.api = YourAPI()
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)

    def _get_cached_result(self, key: str):
        if key in self.cache:
            result, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.cache_duration:
                return result
        return None

    def _cache_result(self, key: str, result: dict):
        self.cache[key] = (result, datetime.now())

    def execute(self, request_dto: RequestDTO) -> ResponseDTO:
        cache_key = str(request_dto.data)
        
        # Check cache
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return ResponseDTO.success(data=cached_result)
        
        # Make API call
        result = self.api.your_method(request_dto.data["param"])
        
        # Cache result
        self._cache_result(cache_key, result)
        
        return ResponseDTO.success(data=result)
```

### 3. Batch Processing

Add batch processing capabilities:
```python
from typing import List

class YourAPI(ThirdPartyAPI):
    def batch_process(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for item in items:
            try:
                result = self.your_method(**item)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
        return results
```

## API Response Format

All API responses follow this standard format:

Success Response:
```json
{
    "status": "success",
    "message": "Operation successful",
    "data": {
        // Response data here
    }
}
```

Error Response:
```json
{
    "status": "error",
    "message": "Error description",
    "error_code": 400
}
```

## Example Endpoints

### Payment API (Example)

Create Payment:
```bash
curl -X POST http://localhost:5000/api/v1/payments \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100.00,
    "currency": "USD",
    "description": "Test payment"
  }'
```

Get Payment:
```bash
curl http://localhost:5000/api/v1/payments/{payment_id}
```

## Error Handling

The boilerplate includes built-in error handling for:
- Invalid requests
- API authentication errors
- Third-party API errors
- Not found errors
- Validation errors

Custom exceptions can be added in `app/core/exceptions.py`.

## WebSocket Support

The API Gateway now includes WebSocket support for real-time communication between the server and clients. This is particularly useful for features like real-time notifications, live updates, and streaming data.

### WebSocket Features

- Real-time bidirectional communication
- Room-based messaging for targeted updates
- Authentication support for secure connections
- Namespace organization for different features
- Event-based message handling

### Using WebSocket in Modules

Each module can implement its own WebSocket handlers. Here's an example of how to use WebSockets in your module:

```python
from app.core.websocket import websocket_manager, ws_auth_required

@ws_auth_required
def handle_event(data):
    # Handle the WebSocket event
    emit('response_event', {'status': 'success', 'data': data})

def init_module_websocket():
    websocket_manager.register_handler('event_name', handle_event, namespace='/module')
```

### Client-Side Connection

Connect to the WebSocket server from your client application:

```javascript
const socket = io('http://localhost:5000/payment', {
    transports: ['websocket'],
    autoConnect: true
});

// Subscribe to payment updates
socket.emit('subscribe_payment', { payment_id: 'payment_123' });

// Listen for payment updates
socket.on('payment_update', (data) => {
    console.log('Payment update received:', data);
});
```

### Available WebSocket Events

#### Payment Module Events

- `subscribe_payment`: Subscribe to payment updates
  - Payload: `{ payment_id: string }`
  - Response: `payment_subscribed` event

- `unsubscribe_payment`: Unsubscribe from payment updates
  - Payload: `{ payment_id: string }`
  - Response: `payment_unsubscribed` event

- `payment_update`: Received when a payment status changes
  - Payload: `{ payment_id: string, status: string, details: object }`

## Best Practices

1. **Code Organization**
   - Follow the module structure strictly
   - Keep modules independent
   - Use type hints consistently
   - Document public methods

2. **Error Handling**
   - Use custom exceptions
   - Provide meaningful error messages
   - Log errors appropriately
   - Handle API-specific errors

3. **Security**
   - Never commit API keys
   - Use environment variables
   - Validate input data
   - Sanitize output data

4. **Performance**
   - Use caching when appropriate
   - Implement rate limiting
   - Handle batch operations
   - Monitor API usage

5. **Testing**
   - Write unit tests
   - Write integration tests
   - Mock external APIs
   - Test error cases

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
