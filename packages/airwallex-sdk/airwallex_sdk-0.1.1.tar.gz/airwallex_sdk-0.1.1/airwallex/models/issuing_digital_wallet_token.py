"""
Models for the Airwallex Issuing Digital Wallet Token API.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import Field
from .base import AirwallexModel
from .issuing_common import DeviceInformation, HasMoreResponse


class RiskInformation(AirwallexModel):
    """Model for token risk information."""
    wallet_provider_account_score: Optional[str] = Field(None, description="Wallet provider account score")
    wallet_provider_device_score: Optional[str] = Field(None, description="Wallet provider device score")


class DigitalWalletToken(AirwallexModel):
    """Model for an Airwallex digital wallet token."""
    resource_name: str = "issuing/digital_wallet_tokens"
    
    card_id: str = Field(..., description="Unique identifier for card associated with the token")
    cardholder_id: str = Field(..., description="Unique identifier for cardholder associated with the token")
    create_time: datetime = Field(..., description="The time this token was created")
    device_information: Optional[DeviceInformation] = Field(None, description="Device information")
    expiry_month: int = Field(..., description="Token expiry month")
    expiry_year: int = Field(..., description="Token expiry year")
    masked_card_number: str = Field(..., description="Masked card number")
    pan_reference_id: str = Field(..., description="Unique identifier for the tokenization of this card")
    risk_information: Optional[RiskInformation] = Field(None, description="Risk information")
    token_id: str = Field(..., description="Unique Identifier for token")
    token_reference_id: str = Field(..., description="Unique identifier of the digital wallet token within the card network")
    token_status: str = Field(..., description="Status of the token")
    token_type: str = Field(..., description="The type of this token")


class DigitalWalletTokenListResponse(HasMoreResponse):
    """Model for digital wallet token list response."""
    items: List[DigitalWalletToken] = Field(..., description="List of digital wallet tokens")
