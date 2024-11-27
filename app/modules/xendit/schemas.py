from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class PaymentMethodType(str, Enum):
    CARD = "CARD"
    DIRECT_DEBIT = "DIRECT_DEBIT"
    EWALLET = "EWALLET"
    VIRTUAL_ACCOUNT = "VIRTUAL_ACCOUNT"
    QR_CODE = "QR_CODE"
    OVER_THE_COUNTER = "OVER_THE_COUNTER"

class PaymentMethodReusability(str, Enum):
    SINGLE_USE = "SINGLE_USE"
    MULTIPLE_USE = "MULTIPLE_USE"

class PaymentMethodStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"
    FAILED = "FAILED"

class CustomerRequest(BaseModel):
    reference_id: str = Field(..., description="Customer reference ID")
    type: Optional[str] = Field(None, description="Customer type")
    individual_detail: Optional[Dict[str, Any]] = Field(None, description="Individual customer details")
    business_detail: Optional[Dict[str, Any]] = Field(None, description="Business customer details")
    description: Optional[str] = Field(None, description="Customer description")
    email: Optional[str] = Field(None, description="Customer email")
    mobile_number: Optional[str] = Field(None, description="Customer mobile number")
    addresses: Optional[List[Dict[str, Any]]] = Field(None, description="Customer addresses")
    identity_accounts: Optional[List[Dict[str, Any]]] = Field(None, description="Customer identity accounts")
    kyc_documents: Optional[List[Dict[str, Any]]] = Field(None, description="Customer KYC documents")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class PaymentMethodRequest(BaseModel):
    type: PaymentMethodType = Field(..., description="Payment method type")
    reusability: PaymentMethodReusability = Field(..., description="Payment method reusability")
    customer_id: str = Field(..., description="Customer ID")
    reference_id: str = Field(..., description="Payment method reference ID")
    billing_information: Optional[Dict[str, Any]] = Field(None, description="Billing information")
    direct_debit: Optional[Dict[str, Any]] = Field(None, description="Direct debit details")
    ewallet: Optional[Dict[str, Any]] = Field(None, description="eWallet details")
    qr_code: Optional[Dict[str, Any]] = Field(None, description="QR code details")
    virtual_account: Optional[Dict[str, Any]] = Field(None, description="Virtual account details")
    over_the_counter: Optional[Dict[str, Any]] = Field(None, description="Over the counter details")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class PaymentRequest(BaseModel):
    reference_id: str = Field(..., description="Payment reference ID")
    amount: float = Field(..., description="Payment amount")
    currency: str = Field(..., description="Payment currency")
    payment_method_id: str = Field(..., description="Payment method ID")
    description: Optional[str] = Field(None, description="Payment description")
    failure_code: Optional[str] = Field(None, description="Payment failure code")
    capture: Optional[bool] = Field(True, description="Whether to capture the payment immediately")
    customer_id: Optional[str] = Field(None, description="Customer ID")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    shipping_information: Optional[Dict[str, Any]] = Field(None, description="Shipping information")

class PaymentMethodResponse(BaseModel):
    id: str = Field(..., description="Payment method ID")
    type: PaymentMethodType = Field(..., description="Payment method type")
    reusability: PaymentMethodReusability = Field(..., description="Payment method reusability")
    status: PaymentMethodStatus = Field(..., description="Payment method status")
    reference_id: str = Field(..., description="Payment method reference ID")
    customer_id: str = Field(..., description="Customer ID")
    created: str = Field(..., description="Creation timestamp")
    updated: str = Field(..., description="Last update timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    billing_information: Optional[Dict[str, Any]] = Field(None, description="Billing information")
    direct_debit: Optional[Dict[str, Any]] = Field(None, description="Direct debit details")
    ewallet: Optional[Dict[str, Any]] = Field(None, description="eWallet details")
    qr_code: Optional[Dict[str, Any]] = Field(None, description="QR code details")
    virtual_account: Optional[Dict[str, Any]] = Field(None, description="Virtual account details")
    over_the_counter: Optional[Dict[str, Any]] = Field(None, description="Over the counter details")

class PaymentResponse(BaseModel):
    id: str = Field(..., description="Payment ID")
    reference_id: str = Field(..., description="Payment reference ID")
    customer_id: Optional[str] = Field(None, description="Customer ID")
    currency: str = Field(..., description="Payment currency")
    amount: float = Field(..., description="Payment amount")
    country: str = Field(..., description="Payment country")
    status: str = Field(..., description="Payment status")
    payment_method: PaymentMethodResponse = Field(..., description="Payment method details")
    description: Optional[str] = Field(None, description="Payment description")
    failure_code: Optional[str] = Field(None, description="Payment failure code")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    shipping_information: Optional[Dict[str, Any]] = Field(None, description="Shipping information")
    created: str = Field(..., description="Creation timestamp")
    updated: str = Field(..., description="Last update timestamp")
