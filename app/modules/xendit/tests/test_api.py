import pytest
from unittest.mock import patch, Mock
from app.modules.xendit.api import XenditAPI
from app.core.third_party import ThirdPartyAPIException

@pytest.fixture
def xendit_api():
    return XenditAPI(api_key="test_key", base_url="https://api.xendit.co")

@pytest.fixture
def mock_response():
    mock = Mock()
    mock.status_code = 200
    return mock

def test_create_customer_success(xendit_api, mock_response, mock_customer_response):
    mock_response.json.return_value = mock_customer_response
    
    with patch('app.modules.xendit.api.requests.post') as mock_post:
        mock_post.return_value = mock_response
        customer_data = {
            "reference_id": "ref-123",
            "email": "test@example.com",
            "given_names": "John",
            "surname": "Doe"
        }
        
        result = xendit_api.create_customer(customer_data)
        
        assert result == mock_customer_response
        mock_post.assert_called_once()

def test_create_customer_error(xendit_api):
    error_response = Mock()
    error_response.status_code = 400
    error_response.json.return_value = {"error": "Invalid data"}
    
    with patch('app.modules.xendit.api.requests.post') as mock_post:
        mock_post.return_value = error_response
        customer_data = {
            "reference_id": "ref-123",
            "email": "invalid-email"
        }
        
        with pytest.raises(ThirdPartyAPIException):
            xendit_api.create_customer(customer_data)

def test_create_payment_method_success(xendit_api, mock_response, mock_payment_method_response):
    mock_response.json.return_value = mock_payment_method_response
    
    with patch('app.modules.xendit.api.requests.post') as mock_post:
        mock_post.return_value = mock_response
        payment_method_data = {
            "type": "CARD",
            "customer_id": "cust-123",
            "card": {
                "token_id": "token-123"
            }
        }
        
        result = xendit_api.create_payment_method(payment_method_data)
        
        assert result == mock_payment_method_response
        mock_post.assert_called_once()

def test_create_payment_success(xendit_api, mock_response, mock_payment_response):
    mock_response.json.return_value = mock_payment_response
    
    with patch('app.modules.xendit.api.requests.post') as mock_post:
        mock_post.return_value = mock_response
        payment_data = {
            "reference_id": "ref-123",
            "amount": 10000,
            "currency": "IDR",
            "payment_method_id": "pm-123"
        }
        
        result = xendit_api.create_payment(payment_data)
        
        assert result == mock_payment_response
        mock_post.assert_called_once()

def test_create_ewallet_charge_success(xendit_api, mock_response, mock_ewallet_charge_response):
    mock_response.json.return_value = mock_ewallet_charge_response
    
    with patch('app.modules.xendit.api.requests.post') as mock_post:
        mock_post.return_value = mock_response
        charge_data = {
            "reference_id": "ref-123",
            "amount": 10000,
            "currency": "IDR"
        }
        
        result = xendit_api.create_ewallet_charge(charge_data)
        
        assert result == mock_ewallet_charge_response
        mock_post.assert_called_once()

def test_create_qr_code_success(xendit_api, mock_response, mock_qr_code_response):
    mock_response.json.return_value = mock_qr_code_response
    
    with patch('app.modules.xendit.api.requests.post') as mock_post:
        mock_post.return_value = mock_response
        qr_code_data = {
            "reference_id": "ref-123",
            "amount": 10000,
            "currency": "IDR"
        }
        
        result = xendit_api.create_qr_code(qr_code_data)
        
        assert result == mock_qr_code_response
        mock_post.assert_called_once()

def test_create_otc_payment_success(xendit_api, mock_response, mock_otc_payment_response):
    mock_response.json.return_value = mock_otc_payment_response
    
    with patch('app.modules.xendit.api.requests.post') as mock_post:
        mock_post.return_value = mock_response
        otc_data = {
            "reference_id": "ref-123",
            "amount": 10000,
            "currency": "IDR"
        }
        
        result = xendit_api.create_otc_payment(otc_data)
        
        assert result == mock_otc_payment_response
        mock_post.assert_called_once()

def test_api_authentication(xendit_api, mock_response):
    mock_response.json.return_value = {}
    
    with patch('app.modules.xendit.api.requests.post') as mock_post:
        mock_post.return_value = mock_response
        xendit_api.create_customer({})
        
        headers = mock_post.call_args.kwargs['headers']
        assert 'Authorization' in headers
        assert headers['Authorization'].startswith('Basic ')

def test_api_error_handling(xendit_api):
    error_response = Mock()
    error_response.status_code = 500
    error_response.json.return_value = {"error": "Internal Server Error"}
    
    with patch('app.modules.xendit.api.requests.post') as mock_post:
        mock_post.return_value = error_response
        
        with pytest.raises(ThirdPartyAPIException) as exc_info:
            xendit_api.create_customer({})
        
        assert "Internal Server Error" in str(exc_info.value)
