import requests
import os
from typing import Optional, Dict, Any, List
from app.core.third_party import ThirdPartyAPI, ThirdPartyAPIException
from config import Config

class XenditAPI(ThirdPartyAPI):
    """Xendit API client"""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        """Initialize Xendit API client"""
        self.api_key = api_key or os.getenv('XENDIT_API_KEY')
        self.base_url = base_url or os.getenv('XENDIT_API_BASE_URL')
        if not self.api_key:
            raise ValueError("XENDIT_API_KEY environment variable is required")
        if not self.base_url:
            raise ValueError("XENDIT_API_BASE_URL environment variable is required")
        self.headers = {
            'Authorization': f'Basic {self.api_key}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.request(method, url, json=data, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ThirdPartyAPIException(f"Xendit API error: {str(e)}")

    def get_headers(self):
        """Get headers for API requests"""
        return {
            'Authorization': f'Basic {self.api_key}',
            'Content-Type': 'application/json'
        }

    # Customer APIs
    def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new customer"""
        return self._make_request('POST', '/customers', data=customer_data)

    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details"""
        return self._make_request('GET', f'/customers/{customer_id}')

    # Payment Method APIs
    def create_payment_method(self, payment_method_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new payment method"""
        return self._make_request('POST', '/v2/payment_methods', data=payment_method_data)

    def get_payment_method(self, payment_method_id: str) -> Dict[str, Any]:
        """Get payment method details"""
        return self._make_request('GET', f'/v2/payment_methods/{payment_method_id}')

    def update_payment_method(self, payment_method_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a payment method"""
        return self._make_request('PATCH', f'/v2/payment_methods/{payment_method_id}', data=update_data)

    def list_payment_methods(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List payment methods"""
        return self._make_request('GET', '/v2/payment_methods', params=params)

    def expire_payment_method(self, payment_method_id: str) -> Dict[str, Any]:
        """Expire a payment method"""
        return self._make_request('POST', f'/v2/payment_methods/{payment_method_id}/expire')

    # Payment APIs
    def create_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new payment"""
        return self._make_request('POST', '/payment_requests', data=payment_data)

    def get_payment(self, payment_id: str) -> Dict[str, Any]:
        """Get payment details"""
        return self._make_request('GET', f'/payment_requests/{payment_id}')

    def list_payments(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List payments"""
        return self._make_request('GET', '/payment_requests', params=params)

    def list_payments_by_payment_method(self, payment_method_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List payments by payment method ID"""
        return self._make_request('GET', f'/v2/payment_methods/{payment_method_id}/payments', params=params)

    # Card Payment APIs
    def create_card_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a card payment"""
        return self._make_request('POST', '/credit_card_charges', data=payment_data)

    def capture_card_payment(self, payment_id: str, capture_data: Dict[str, Any]) -> Dict[str, Any]:
        """Capture a card payment"""
        return self._make_request('POST', f'/credit_card_charges/{payment_id}/capture', data=capture_data)

    def refund_card_payment(self, payment_id: str, refund_data: Dict[str, Any]) -> Dict[str, Any]:
        """Refund a card payment"""
        return self._make_request('POST', f'/credit_card_charges/{payment_id}/refund', data=refund_data)

    # eWallet Payment APIs
    def create_ewallet_charge(self, charge_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an eWallet charge"""
        return self._make_request('POST', '/ewallets/charges', data=charge_data)

    def get_ewallet_charge_status(self, charge_id: str) -> Dict[str, Any]:
        """Get eWallet charge status"""
        return self._make_request('GET', f'/ewallets/charges/{charge_id}')

    # QR Code Payment APIs
    def create_qr_code(self, qr_code_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a QR code payment"""
        return self._make_request('POST', '/qr_codes', data=qr_code_data)

    def get_qr_code_status(self, qr_code_id: str) -> Dict[str, Any]:
        """Get QR code payment status"""
        return self._make_request('GET', f'/qr_codes/{qr_code_id}')

    # Over-the-Counter Payment APIs
    def create_otc_payment(self, otc_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an over-the-counter payment"""
        return self._make_request('POST', '/payment_requests', data=otc_data)

    def get_otc_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Get over-the-counter payment status"""
        return self._make_request('GET', f'/payment_requests/{payment_id}')
