from typing import Dict, Any, Optional, List
from .api import XenditAPI
from .schemas import (
    CustomerRequest, PaymentMethodRequest, PaymentRequest,
    PaymentMethodResponse, PaymentResponse
)
from app.core.third_party import ThirdPartyAPIException

class XenditUseCase:
    """Use cases for Xendit API"""

    def __init__(self, api_client: XenditAPI = None):
        """Initialize Xendit use cases"""
        self.api = api_client or XenditAPI()

    # Customer Operations
    async def create_customer(self, customer_data: CustomerRequest) -> Dict[str, Any]:
        """Create a new customer"""
        try:
            return self.api.create_customer(customer_data.dict(exclude_none=True))
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to create customer: {str(e)}")

    async def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details"""
        try:
            return self.api.get_customer(customer_id)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to get customer: {str(e)}")

    # Payment Method Operations
    async def create_payment_method(self, payment_method_data: PaymentMethodRequest) -> PaymentMethodResponse:
        """Create a new payment method"""
        try:
            response = self.api.create_payment_method(payment_method_data.dict(exclude_none=True))
            return PaymentMethodResponse(**response)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to create payment method: {str(e)}")

    async def get_payment_method(self, payment_method_id: str) -> PaymentMethodResponse:
        """Get payment method details"""
        try:
            response = self.api.get_payment_method(payment_method_id)
            return PaymentMethodResponse(**response)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to get payment method: {str(e)}")

    async def update_payment_method(self, payment_method_id: str, update_data: Dict[str, Any]) -> PaymentMethodResponse:
        """Update a payment method"""
        try:
            response = self.api.update_payment_method(payment_method_id, update_data)
            return PaymentMethodResponse(**response)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to update payment method: {str(e)}")

    async def list_payment_methods(self, params: Optional[Dict[str, Any]] = None) -> List[PaymentMethodResponse]:
        """List payment methods"""
        try:
            response = self.api.list_payment_methods(params)
            return [PaymentMethodResponse(**method) for method in response.get('data', [])]
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to list payment methods: {str(e)}")

    async def expire_payment_method(self, payment_method_id: str) -> PaymentMethodResponse:
        """Expire a payment method"""
        try:
            response = self.api.expire_payment_method(payment_method_id)
            return PaymentMethodResponse(**response)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to expire payment method: {str(e)}")

    # Payment Operations
    async def create_payment(self, payment_data: PaymentRequest) -> PaymentResponse:
        """Create a new payment"""
        try:
            response = self.api.create_payment(payment_data.dict(exclude_none=True))
            return PaymentResponse(**response)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to create payment: {str(e)}")

    async def get_payment(self, payment_id: str) -> PaymentResponse:
        """Get payment details"""
        try:
            response = self.api.get_payment(payment_id)
            return PaymentResponse(**response)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to get payment: {str(e)}")

    async def list_payments(self, params: Optional[Dict[str, Any]] = None) -> List[PaymentResponse]:
        """List payments"""
        try:
            response = self.api.list_payments(params)
            return [PaymentResponse(**payment) for payment in response.get('data', [])]
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to list payments: {str(e)}")

    # Card Payment Operations
    async def create_card_payment(self, payment_data: Dict[str, Any]) -> PaymentResponse:
        """Create a card payment"""
        try:
            response = self.api.create_card_payment(payment_data)
            return PaymentResponse(**response)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to create card payment: {str(e)}")

    async def capture_card_payment(self, payment_id: str, capture_data: Dict[str, Any]) -> PaymentResponse:
        """Capture a card payment"""
        try:
            response = self.api.capture_card_payment(payment_id, capture_data)
            return PaymentResponse(**response)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to capture card payment: {str(e)}")

    async def refund_card_payment(self, payment_id: str, refund_data: Dict[str, Any]) -> Dict[str, Any]:
        """Refund a card payment"""
        try:
            return self.api.refund_card_payment(payment_id, refund_data)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to refund card payment: {str(e)}")

    # eWallet Operations
    async def create_ewallet_charge(self, charge_data: Dict[str, Any]) -> PaymentResponse:
        """Create an eWallet charge"""
        try:
            response = self.api.create_ewallet_charge(charge_data)
            return PaymentResponse(**response)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to create eWallet charge: {str(e)}")

    async def get_ewallet_charge_status(self, charge_id: str) -> PaymentResponse:
        """Get eWallet charge status"""
        try:
            response = self.api.get_ewallet_charge_status(charge_id)
            return PaymentResponse(**response)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to get eWallet charge status: {str(e)}")

    # QR Code Operations
    async def create_qr_code(self, qr_code_data: Dict[str, Any]) -> PaymentResponse:
        """Create a QR code payment"""
        try:
            response = self.api.create_qr_code(qr_code_data)
            return PaymentResponse(**response)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to create QR code payment: {str(e)}")

    async def get_qr_code_status(self, qr_code_id: str) -> PaymentResponse:
        """Get QR code payment status"""
        try:
            response = self.api.get_qr_code_status(qr_code_id)
            return PaymentResponse(**response)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to get QR code payment status: {str(e)}")

    # Over-the-Counter Operations
    async def create_otc_payment(self, otc_data: Dict[str, Any]) -> PaymentResponse:
        """Create an over-the-counter payment"""
        try:
            response = self.api.create_otc_payment(otc_data)
            return PaymentResponse(**response)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to create OTC payment: {str(e)}")

    async def get_otc_payment_status(self, payment_id: str) -> PaymentResponse:
        """Get over-the-counter payment status"""
        try:
            response = self.api.get_otc_payment_status(payment_id)
            return PaymentResponse(**response)
        except ThirdPartyAPIException as e:
            raise ThirdPartyAPIException(f"Failed to get OTC payment status: {str(e)}")
