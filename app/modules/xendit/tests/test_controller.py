import pytest
from unittest.mock import patch
from app.modules.xendit.controller import bp

@pytest.fixture
def client(app):
    app.register_blueprint(bp, url_prefix='/xendit')
    return app.test_client()

async def test_create_customer_success(client, mock_customer_response):
    with patch('app.modules.xendit.controller.xendit_use_case.create_customer') as mock_create:
        mock_create.return_value = mock_customer_response
        customer_data = {
            "reference_id": "ref-123",
            "email": "test@example.com",
            "given_names": "John",
            "surname": "Doe",
            "mobile_number": "+1234567890"
        }
        
        response = await client.post('/xendit/customers', json=customer_data)
        
        assert response.status_code == 201
        assert response.json == mock_customer_response

async def test_create_payment_method_success(client, mock_payment_method_response):
    with patch('app.modules.xendit.controller.xendit_use_case.create_payment_method') as mock_create:
        mock_create.return_value = mock_payment_method_response
        payment_method_data = {
            "type": "CARD",
            "customer_id": "cust-123",
            "reference_id": "ref-123",
            "card": {
                "token_id": "token-123"
            }
        }
        
        response = await client.post('/xendit/payment-methods', json=payment_method_data)
        
        assert response.status_code == 201
        assert response.json == mock_payment_method_response

async def test_create_payment_success(client, mock_payment_response):
    with patch('app.modules.xendit.controller.xendit_use_case.create_payment') as mock_create:
        mock_create.return_value = mock_payment_response
        payment_data = {
            "reference_id": "ref-123",
            "amount": 10000,
            "currency": "IDR",
            "payment_method_id": "pm-123",
            "customer_id": "cust-123"
        }
        
        response = await client.post('/xendit/payments', json=payment_data)
        
        assert response.status_code == 201
        assert response.json == mock_payment_response

async def test_create_ewallet_charge_success(client, mock_ewallet_charge_response):
    with patch('app.modules.xendit.controller.xendit_use_case.create_ewallet_charge') as mock_create:
        mock_create.return_value = mock_ewallet_charge_response
        charge_data = {
            "reference_id": "ref-123",
            "amount": 10000,
            "currency": "IDR",
            "payment_method_id": "pm-123"
        }
        
        response = await client.post('/xendit/ewallet-charges', json=charge_data)
        
        assert response.status_code == 201
        assert response.json == mock_ewallet_charge_response

async def test_create_qr_code_success(client, mock_qr_code_response):
    with patch('app.modules.xendit.controller.xendit_use_case.create_qr_code') as mock_create:
        mock_create.return_value = mock_qr_code_response
        qr_code_data = {
            "reference_id": "ref-123",
            "amount": 10000,
            "currency": "IDR"
        }
        
        response = await client.post('/xendit/qr-codes', json=qr_code_data)
        
        assert response.status_code == 201
        assert response.json == mock_qr_code_response

async def test_create_otc_payment_success(client, mock_otc_payment_response):
    with patch('app.modules.xendit.controller.xendit_use_case.create_otc_payment') as mock_create:
        mock_create.return_value = mock_otc_payment_response
        otc_data = {
            "reference_id": "ref-123",
            "amount": 10000,
            "currency": "IDR",
            "payment_code": "12345678"
        }
        
        response = await client.post('/xendit/otc-payments', json=otc_data)
        
        assert response.status_code == 201
        assert response.json == mock_otc_payment_response

async def test_get_payment_success(client, mock_payment_response):
    with patch('app.modules.xendit.controller.xendit_use_case.get_payment') as mock_get:
        mock_get.return_value = mock_payment_response
        payment_id = "pay-123"
        
        response = await client.get(f'/xendit/payments/{payment_id}')
        
        assert response.status_code == 200
        assert response.json == mock_payment_response

async def test_get_payment_method_success(client, mock_payment_method_response):
    with patch('app.modules.xendit.controller.xendit_use_case.get_payment_method') as mock_get:
        mock_get.return_value = mock_payment_method_response
        payment_method_id = "pm-123"
        
        response = await client.get(f'/xendit/payment-methods/{payment_method_id}')
        
        assert response.status_code == 200
        assert response.json == mock_payment_method_response

async def test_error_handling(client):
    with patch('app.modules.xendit.controller.xendit_use_case.create_customer') as mock_create:
        mock_create.side_effect = Exception("API Error")
        customer_data = {
            "reference_id": "ref-123",
            "email": "test@example.com"
        }
        
        response = await client.post('/xendit/customers', json=customer_data)
        
        assert response.status_code == 400
        assert 'error' in response.json
