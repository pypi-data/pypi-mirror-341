"""
Models for the Airwallex account API.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import Field
from .base import AirwallexModel


class AccountBalanceAmount(AirwallexModel):
    """Model for account balance amount."""
    currency: str = Field(..., description="Currency code (ISO 4217)")
    value: float = Field(..., description="Balance amount value")


class AccountBalance(AirwallexModel):
    """Model for account balance."""
    available_amount: AccountBalanceAmount = Field(..., description="Available account balance")
    pending_amount: Optional[AccountBalanceAmount] = Field(None, description="Pending account balance")


class Account(AirwallexModel):
    """Model for an Airwallex account."""
    resource_name: str = "accounts"
    
    id: str = Field(..., description="Unique account ID")
    account_name: str = Field(..., description="Account name")
    account_type: str = Field(..., description="Account type")
    account_currency: str = Field(..., description="Account currency (ISO 4217)")
    status: str = Field(..., description="Account status")
    swift_code: Optional[str] = Field(None, description="SWIFT/BIC code")
    iban: Optional[str] = Field(None, description="IBAN (International Bank Account Number)")
    routing_number: Optional[str] = Field(None, description="Routing number")
    account_number: Optional[str] = Field(None, description="Account number")
    bsb: Optional[str] = Field(None, description="BSB (Bank State Branch code) for AU accounts")
    sort_code: Optional[str] = Field(None, description="Sort code for UK accounts")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Account last update timestamp")
    balance: Optional[AccountBalance] = Field(None, description="Account balance")
    

class AccountCreateRequest(AirwallexModel):
    """Model for account creation request."""
    account_name: str = Field(..., description="Name for the account")
    account_currency: str = Field(..., description="Currency code (ISO 4217)")


class AccountUpdateRequest(AirwallexModel):
    """Model for account update request."""
    account_name: Optional[str] = Field(None, description="New name for the account")
    status: Optional[str] = Field(None, description="New status for the account")
