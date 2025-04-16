"""
Models for the Airwallex payment API.
"""
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import Field, EmailStr
from .base import AirwallexModel


class PaymentAmount(AirwallexModel):
    """Model for payment amount."""
    value: float = Field(..., description="Payment amount value")
    currency: str = Field(..., description="Currency code (ISO 4217)")


class PaymentSourceDetails(AirwallexModel):
    """Model for payment source details."""
    type: str = Field(..., description="Source type (e.g., 'account')")
    account_id: Optional[str] = Field(None, description="Account ID for account sources")
    card_id: Optional[str] = Field(None, description="Card ID for card sources")


class PaymentBeneficiary(AirwallexModel):
    """Model for payment beneficiary."""
    type: str = Field(..., description="Beneficiary type (e.g., 'bank_account', 'email')")
    id: Optional[str] = Field(None, description="Beneficiary ID for saved beneficiaries")
    name: Optional[str] = Field(None, description="Beneficiary name")
    email: Optional[EmailStr] = Field(None, description="Beneficiary email")
    country_code: Optional[str] = Field(None, description="Beneficiary country code (ISO 3166-1 alpha-2)")
    bank_details: Optional[Dict[str, Any]] = Field(None, description="Bank details for bank transfers")


class Payment(AirwallexModel):
    """Model for an Airwallex payment."""
    resource_name: str = "payments"
    
    id: str = Field(..., description="Unique payment ID")
    request_id: Optional[str] = Field(None, description="Client-generated request ID")
    amount: PaymentAmount = Field(..., description="Payment amount")
    source: PaymentSourceDetails = Field(..., description="Payment source details")
    beneficiary: PaymentBeneficiary = Field(..., description="Payment beneficiary details")
    payment_method: str = Field(..., description="Payment method type")
    status: str = Field(..., description="Payment status")
    payment_date: Optional[datetime] = Field(None, description="Payment date")
    reference: Optional[str] = Field(None, description="Payment reference")
    description: Optional[str] = Field(None, description="Payment description")
    metadata: Optional[Dict[str, str]] = Field(None, description="Additional metadata")
    created_at: datetime = Field(..., description="Payment creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Payment last update timestamp")


class PaymentCreateRequest(AirwallexModel):
    """Model for payment creation request."""
    request_id: str = Field(..., description="Client-generated unique ID for the request")
    amount: PaymentAmount = Field(..., description="Payment amount")
    source: PaymentSourceDetails = Field(..., description="Payment source details")
    beneficiary: PaymentBeneficiary = Field(..., description="Payment beneficiary details")
    payment_method: str = Field(..., description="Payment method type")
    payment_date: Optional[datetime] = Field(None, description="Requested payment date")
    reference: Optional[str] = Field(None, description="Payment reference visible to the beneficiary")
    description: Optional[str] = Field(None, description="Internal payment description")
    metadata: Optional[Dict[str, str]] = Field(None, description="Additional metadata")


class PaymentUpdateRequest(AirwallexModel):
    """Model for payment update request."""
    status: Optional[str] = Field(None, description="New payment status (for cancellation)")
    payment_date: Optional[datetime] = Field(None, description="Updated payment date")
    reference: Optional[str] = Field(None, description="Updated payment reference")
    description: Optional[str] = Field(None, description="Updated payment description")
    metadata: Optional[Dict[str, str]] = Field(None, description="Updated metadata")


class PaymentQuote(AirwallexModel):
    """Model for payment quote details."""
    id: str = Field(..., description="Quote ID")
    source_amount: PaymentAmount = Field(..., description="Source amount")
    target_amount: PaymentAmount = Field(..., description="Target amount")
    fx_rate: float = Field(..., description="FX rate applied")
    fee: Optional[PaymentAmount] = Field(None, description="Fee amount")
    expires_at: datetime = Field(..., description="Quote expiration timestamp")
