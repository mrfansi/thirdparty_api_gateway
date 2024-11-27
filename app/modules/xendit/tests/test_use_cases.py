import pytest
from app.modules.xendit.schemas import (
    CustomerRequest, PaymentMethodRequest, PaymentRequest
)
from app.core.third_party import ThirdPartyAPIException

async def test_create_customer_success(xendit_use_case, mock_xendit_api, mock_customer_response):
    mock_xendit_api.create_customer.return_value = mock_customer_response
    customer_request = CustomerRequest(
        reference_id="ref-123",
        email="test@example.com",
        given_names="John",
        surname="Doe",
        mobile_number="+1234567890"
    )
    
    result = await xendit_use_case.create_customer(customer_request)
    
    assert result == mock_customer_response
    mock_xendit_api.create_customer.assert_called_once_with(customer_request)

async def test_create_customer_failure(xendit_use_case, mock_xendit_api):
    mock_xendit_api.create_customer.side_effect = ThirdPartyAPIException("API Error")
    customer_request = CustomerRequest(
        reference_id="ref-123",
        email="test@example.com",
        given_names="John",
        surname="Doe"
    )
    
    with pytest.raises(ThirdPartyAPIException):
        await xendit_use_case.create_customer(customer_request)

async def test_get_customer_success(xendit_use_case, mock_xendit_api, mock_customer_response):
    mock_xendit_api.get_customer.return_value = mock_customer_response
    customer_id = "cust-123"
    
    result = await xendit_use_case.get_customer(customer_id)
    
    assert result == mock_customer_response
    mock_xendit_api.get_customer.assert_called_once_with(customer_id)

async def test_create_payment_method_success(xendit_use_case, mock_xendit_api, mock_payment_method_response):
    mock_xendit_api.create_payment_method.return_value = mock_payment_method_response
    payment_method_request = PaymentMethodRequest(
        type="CARD",
        customer_id="cust-123",
        reference_id="ref-123",
        card={
            "token_id": "token-123"
        }
    )
    
    result = await xendit_use_case.create_payment_method(payment_method_request)
    
    assert result.id == mock_payment_method_response["id"]
    assert result.type == mock_payment_method_response["type"]
    mock_xendit_api.create_payment_method.assert_called_once_with(payment_method_request)

async def test_get_payment_method_success(xendit_use_case, mock_xendit_api, mock_payment_method_response):
    mock_xendit_api.get_payment_method.return_value = mock_payment_method_response
    payment_method_id = "pm-123"
    
    result = await xendit_use_case.get_payment_method(payment_method_id)
    
    assert result.id == mock_payment_method_response["id"]
    assert result.type == mock_payment_method_response["type"]
    mock_xendit_api.get_payment_method.assert_called_once_with(payment_method_id)

async def test_create_payment_success(xendit_use_case, mock_xendit_api, mock_payment_response):
    mock_xendit_api.create_payment.return_value = mock_payment_response
    payment_request = PaymentRequest(
        reference_id="ref-123",
        amount=10000,
        currency="IDR",
        payment_method_id="pm-123",
        customer_id="cust-123"
    )
    
    result = await xendit_use_case.create_payment(payment_request)
    
    assert result.id == mock_payment_response["id"]
    assert result.status == mock_payment_response["status"]
    mock_xendit_api.create_payment.assert_called_once_with(payment_request)

async def test_get_payment_success(xendit_use_case, mock_xendit_api, mock_payment_response):
    mock_xendit_api.get_payment.return_value = mock_payment_response
    payment_id = "pay-123"
    
    result = await xendit_use_case.get_payment(payment_id)
    
    assert result.id == mock_payment_response["id"]
    assert result.status == mock_payment_response["status"]
    mock_xendit_api.get_payment.assert_called_once_with(payment_id)

async def test_create_ewallet_charge_success(xendit_use_case, mock_xendit_api, mock_ewallet_charge_response):
    mock_xendit_api.create_ewallet_charge.return_value = mock_ewallet_charge_response
    charge_data = {
        "reference_id": "ref-123",
        "amount": 10000,
        "currency": "IDR",
        "payment_method_id": "pm-123"
    }
    
    result = await xendit_use_case.create_ewallet_charge(charge_data)
    
    assert result.id == mock_ewallet_charge_response["id"]
    assert result.status == mock_ewallet_charge_response["status"]
    mock_xendit_api.create_ewallet_charge.assert_called_once_with(charge_data)

async def test_create_qr_code_success(xendit_use_case, mock_xendit_api, mock_qr_code_response):
    mock_xendit_api.create_qr_code.return_value = mock_qr_code_response
    qr_code_data = {
        "reference_id": "ref-123",
        "amount": 10000,
        "currency": "IDR"
    }
    
    result = await xendit_use_case.create_qr_code(qr_code_data)
    
    assert result.id == mock_qr_code_response["id"]
    assert result.qr_string == mock_qr_code_response["qr_string"]
    mock_xendit_api.create_qr_code.assert_called_once_with(qr_code_data)

async def test_create_otc_payment_success(xendit_use_case, mock_xendit_api, mock_otc_payment_response):
    mock_xendit_api.create_otc_payment.return_value = mock_otc_payment_response
    otc_data = {
        "reference_id": "ref-123",
        "amount": 10000,
        "currency": "IDR",
        "payment_code": "12345678"
    }
    
    result = await xendit_use_case.create_otc_payment(otc_data)
    
    assert result.id == mock_otc_payment_response["id"]
    assert result.payment_code == mock_otc_payment_response["payment_code"]
    mock_xendit_api.create_otc_payment.assert_called_once_with(otc_data)
