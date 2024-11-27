import pytest
from unittest.mock import Mock
from app.modules.xendit.api import XenditAPI
from app.modules.xendit.use_cases import XenditUseCase
from app.modules.xendit.tests.test_config import create_test_app

@pytest.fixture
def app():
    return create_test_app()

@pytest.fixture
def mock_xendit_api():
    api = Mock(spec=XenditAPI)
    api.get_headers.return_value = {
        'Authorization': 'Basic test_key',
        'Content-Type': 'application/json'
    }
    return api

@pytest.fixture
def xendit_use_case(mock_xendit_api):
    return XenditUseCase(api_client=mock_xendit_api)

@pytest.fixture
def mock_customer_response():
    return {
        "id": "cust-123",
        "reference_id": "ref-123",
        "email": "test@example.com",
        "given_names": "John",
        "surname": "Doe",
        "mobile_number": "+1234567890",
        "created": "2023-01-01T00:00:00Z"
    }

@pytest.fixture
def mock_payment_method_response():
    return {
        "id": "pm-123",
        "type": "CARD",
        "status": "ACTIVE",
        "created": "2023-01-01T00:00:00Z",
        "customer_id": "cust-123",
        "reference_id": "ref-123",
        "card": {
            "last_four": "4242",
            "expiry_month": "12",
            "expiry_year": "2025",
            "token_id": "token-123"
        }
    }

@pytest.fixture
def mock_payment_response():
    return {
        "id": "pay-123",
        "reference_id": "ref-123",
        "customer_id": "cust-123",
        "payment_method_id": "pm-123",
        "amount": 10000,
        "currency": "IDR",
        "status": "SUCCEEDED",
        "created": "2023-01-01T00:00:00Z"
    }

@pytest.fixture
def mock_ewallet_charge_response():
    return {
        "id": "ew-123",
        "reference_id": "ref-123",
        "status": "PENDING",
        "currency": "IDR",
        "amount": 10000,
        "checkout_url": "https://checkout.xendit.co/web/123",
        "created": "2023-01-01T00:00:00Z"
    }

@pytest.fixture
def mock_qr_code_response():
    return {
        "id": "qr-123",
        "reference_id": "ref-123",
        "status": "ACTIVE",
        "currency": "IDR",
        "amount": 10000,
        "qr_string": "00020101021226...",
        "created": "2023-01-01T00:00:00Z"
    }

@pytest.fixture
def mock_otc_payment_response():
    return {
        "id": "otc-123",
        "reference_id": "ref-123",
        "status": "PENDING",
        "currency": "IDR",
        "amount": 10000,
        "payment_code": "12345678",
        "created": "2023-01-01T00:00:00Z"
    }
