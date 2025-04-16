"""
Models for the Airwallex Issuing Authorization API.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import Field
from .base import AirwallexModel
from .issuing_common import Merchant, RiskDetails, HasMoreResponse


class Authorization(AirwallexModel):
    """Model for an Airwallex issuing authorization."""
    resource_name: str = "issuing/authorizations"
    
    acquiring_institution_identifier: Optional[str] = Field(None, description="Unique Identifier for acquiring institution")
    auth_code: Optional[str] = Field(None, description="Authorization Code")
    billing_amount: float = Field(..., description="Billing Amount")
    billing_currency: str = Field(..., description="Billing Currency")
    card_id: str = Field(..., description="Unique Identifier for card")
    card_nickname: Optional[str] = Field(None, description="The nickname of the card used")
    client_data: Optional[str] = Field(None, description="Client data stored against the card record")
    create_time: datetime = Field(..., description="The time this outstanding authorization was created")
    digital_wallet_token_id: Optional[str] = Field(None, description="Unique Identifier for digital token")
    expiry_date: Optional[datetime] = Field(None, description="The authorization will expire after this date if not posted")
    failure_reason: Optional[str] = Field(None, description="The reason why this authorization failed (if status is FAILED)")
    lifecycle_id: Optional[str] = Field(None, description="A identifier that links multiple related transactions")
    masked_card_number: Optional[str] = Field(None, description="Masked card number")
    merchant: Optional[Merchant] = Field(None, description="Merchant details")
    network_transaction_id: Optional[str] = Field(None, description="The transaction ID from network")
    retrieval_ref: Optional[str] = Field(None, description="Transaction retrieval reference number")
    risk_details: Optional[RiskDetails] = Field(None, description="Risk details")
    status: str = Field(..., description="The status of this authorization")
    transaction_amount: float = Field(..., description="Transaction amount")
    transaction_currency: str = Field(..., description="Transaction currency")
    transaction_id: str = Field(..., description="Unique id for transaction")
    updated_by_transaction: Optional[str] = Field(None, description="Id of the transaction which updated status of this transaction")


class AuthorizationListResponse(HasMoreResponse):
    """Model for authorization list response."""
    items: List[Authorization] = Field(..., description="List of authorizations")
