"""
Models for the Airwallex Issuing Transaction API.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import Field
from .base import AirwallexModel
from .issuing_common import Merchant, RiskDetails, HasMoreResponse


class Transaction(AirwallexModel):
    """Model for an Airwallex issuing transaction."""
    resource_name: str = "issuing/transactions"
    
    acquiring_institution_identifier: Optional[str] = Field(None, description="Unique Identifier for acquiring institution")
    auth_code: Optional[str] = Field(None, description="Authorization Code")
    billing_amount: float = Field(..., description="Billing amount")
    billing_currency: str = Field(..., description="Billing Currency")
    card_id: str = Field(..., description="Unique Identifier for card")
    card_nickname: Optional[str] = Field(None, description="The nickname of the card used")
    client_data: Optional[str] = Field(None, description="Client data stored against the card record")
    digital_wallet_token_id: Optional[str] = Field(None, description="Unique Identifier for digital token")
    failure_reason: Optional[str] = Field(None, description="The reason why this transaction failed")
    lifecycle_id: Optional[str] = Field(None, description="Lifecycle ID")
    masked_card_number: str = Field(..., description="Masked card number")
    matched_authorizations: Optional[List[str]] = Field(None, description="Matched authorization IDs")
    merchant: Optional[Merchant] = Field(None, description="Merchant details")
    network_transaction_id: Optional[str] = Field(None, description="Network transaction ID")
    posted_date: Optional[datetime] = Field(None, description="Posted date")
    retrieval_ref: Optional[str] = Field(None, description="Retrieval reference number")
    risk_details: Optional[RiskDetails] = Field(None, description="Risk details")
    status: str = Field(..., description="Transaction status")
    transaction_amount: float = Field(..., description="Transaction amount")
    transaction_currency: str = Field(..., description="Transaction currency")
    transaction_date: datetime = Field(..., description="Transaction date")
    transaction_id: str = Field(..., description="Transaction ID")
    transaction_type: str = Field(..., description="Transaction type")


class TransactionListResponse(HasMoreResponse):
    """Model for transaction list response."""
    items: List[Transaction] = Field(..., description="List of transactions")
