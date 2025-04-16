"""
Models for the Airwallex Issuing Card API.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import Field
from .base import AirwallexModel
from .issuing_common import Address, TransactionUsage, DeliveryDetails, HasMoreResponse


class CardVersionInfo(AirwallexModel):
    """Model for card version information."""
    card_number: str = Field(..., description="Masked card number")
    card_status: str = Field(..., description="Current card status")
    card_version: int = Field(..., description="Card version")
    created_at: datetime = Field(..., description="Creation time of the card version")


class SpendLimit(AirwallexModel):
    """Model for spend limit."""
    amount: float = Field(..., description="Limit amount")
    interval: str = Field(..., description="Limit interval (e.g., 'PER_TRANSACTION')")
    remaining: Optional[float] = Field(None, description="Remaining limit amount")


class CardLimits(AirwallexModel):
    """Model for card limits."""
    cash_withdrawal_limits: List[SpendLimit] = Field(..., description="Cash withdrawal limits")
    currency: str = Field(..., description="Currency of limits")
    limits: List[SpendLimit] = Field(..., description="Spending limits")


class PrimaryContactDetails(AirwallexModel):
    """Model for primary contact details."""
    email: Optional[str] = Field(None, description="Email address")
    name: Optional[str] = Field(None, description="Name")
    phone_number: Optional[str] = Field(None, description="Phone number")


class CardProgram(AirwallexModel):
    """Model for card program."""
    id: str = Field(..., description="Program ID")
    name: str = Field(..., description="Program name")


class AuthorizationControls(AirwallexModel):
    """Model for card authorization controls."""
    active_from: Optional[datetime] = Field(None, description="Start time for card validity")
    active_to: Optional[datetime] = Field(None, description="End time for card validity")
    allowed_currencies: Optional[List[str]] = Field(None, description="Allowed currencies")
    allowed_merchant_categories: Optional[List[str]] = Field(None, description="Allowed merchant category codes")
    allowed_transaction_count: Optional[str] = Field(None, description="Allowed transaction count (SINGLE or MULTIPLE)")
    blocked_transaction_usages: Optional[List[TransactionUsage]] = Field(None, description="Blocked transaction usages")
    country_limitations: Optional[List[str]] = Field(None, description="Country limitations")
    spend_limits: Optional[List[SpendLimit]] = Field(None, description="Spend limits")


class CardCreateRequest(AirwallexModel):
    """Model for card creation request."""
    activate_on_issue: Optional[bool] = Field(None, description="Activate on issue")
    additional_cardholder_ids: Optional[List[str]] = Field(None, description="Additional cardholder IDs")
    authorization_controls: AuthorizationControls = Field(..., description="Authorization controls")
    brand: Optional[str] = Field(None, description="Card brand")
    cardholder_id: str = Field(..., description="Cardholder ID")
    client_data: Optional[str] = Field(None, description="Client data")
    created_by: str = Field(..., description="Full legal name of user requesting new card")
    form_factor: str = Field(..., description="Form factor (PHYSICAL or VIRTUAL)")
    funding_source_id: Optional[str] = Field(None, description="Funding source ID")
    is_personalized: bool = Field(..., description="Whether the card is personalized")
    metadata: Optional[Dict[str, str]] = Field(None, description="Metadata")
    nick_name: Optional[str] = Field(None, description="Card nickname")
    note: Optional[str] = Field(None, description="Note")
    postal_address: Optional[Address] = Field(None, description="Postal address")
    program: CardProgram = Field(..., description="Card program")
    purpose: Optional[str] = Field(None, description="Card purpose")
    request_id: str = Field(..., description="Request ID")


class CardUpdateRequest(AirwallexModel):
    """Model for card update request."""
    additional_cardholder_ids: Optional[List[str]] = Field(None, description="Additional cardholder IDs")
    authorization_controls: Optional[AuthorizationControls] = Field(None, description="Authorization controls")
    card_status: Optional[str] = Field(None, description="Card status")
    cardholder_id: Optional[str] = Field(None, description="Cardholder ID")
    metadata: Optional[Dict[str, str]] = Field(None, description="Metadata")
    nick_name: Optional[str] = Field(None, description="Card nickname")
    purpose: Optional[str] = Field(None, description="Card purpose")


class Card(AirwallexModel):
    """Model for an Airwallex issuing card."""
    resource_name: str = "issuing/cards"
    
    activate_on_issue: Optional[bool] = Field(None, description="Activate on issue")
    additional_cardholder_ids: Optional[List[str]] = Field(None, description="Additional cardholder IDs")
    all_card_versions: Optional[List[CardVersionInfo]] = Field(None, description="All card versions")
    authorization_controls: AuthorizationControls = Field(..., description="Authorization controls")
    brand: str = Field(..., description="Card brand")
    card_id: str = Field(..., description="Card ID")
    card_number: str = Field(..., description="Masked card number")
    card_status: str = Field(..., description="Card status")
    card_version: int = Field(..., description="Card version")
    cardholder_id: str = Field(..., description="Cardholder ID")
    client_data: Optional[str] = Field(None, description="Client data")
    created_at: datetime = Field(..., description="Creation time")
    created_by: str = Field(..., description="Created by")
    delivery_details: Optional[DeliveryDetails] = Field(None, description="Delivery details")
    form_factor: str = Field(..., description="Form factor")
    funding_source_id: Optional[str] = Field(None, description="Funding source ID")
    is_personalized: bool = Field(..., description="Whether the card is personalized")
    issue_to: str = Field(..., description="Who the card is issued to")
    metadata: Optional[Dict[str, str]] = Field(None, description="Metadata")
    name_on_card: Optional[str] = Field(None, description="Name on card")
    nick_name: Optional[str] = Field(None, description="Nickname")
    note: Optional[str] = Field(None, description="Note")
    postal_address: Optional[Address] = Field(None, description="Postal address")
    primary_contact_details: Optional[PrimaryContactDetails] = Field(None, description="Primary contact details")
    program: CardProgram = Field(..., description="Card program")
    purpose: Optional[str] = Field(None, description="Purpose")
    request_id: str = Field(..., description="Request ID")
    updated_at: datetime = Field(..., description="Last update time")


class CardDetails(AirwallexModel):
    """Model for sensitive card details."""
    card_number: str = Field(..., description="Full card number")
    cvv: str = Field(..., description="Card verification value")
    expiry_month: int = Field(..., description="Expiry month")
    expiry_year: int = Field(..., description="Expiry year")
    name_on_card: str = Field(..., description="Name on card")


class CardListResponse(HasMoreResponse):
    """Model for card list response."""
    items: List[Card] = Field(..., description="List of cards")
