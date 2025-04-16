"""
Common models for the Airwallex Issuing API.
"""
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import Field, EmailStr
from .base import AirwallexModel


class Address(AirwallexModel):
    """Model for address information."""
    city: str = Field(..., description="City")
    country: str = Field(..., description="Country code (ISO 3166-1 alpha-2)")
    line1: str = Field(..., description="Street address line 1")
    line2: Optional[str] = Field(None, description="Street address line 2")
    postcode: Optional[str] = Field(None, description="Postal or ZIP code")
    state: Optional[str] = Field(None, description="State or province")


class Name(AirwallexModel):
    """Model for person name."""
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    middle_name: Optional[str] = Field(None, description="Middle name")
    title: Optional[str] = Field(None, description="Title (Mr, Mrs, etc.)")


class BusinessIdentifier(AirwallexModel):
    """Model for business identifier."""
    country_code: str = Field(..., description="Country code (ISO 3166-1 alpha-2)")
    number: str = Field(..., description="Identifier number")
    type: str = Field(..., description="Identifier type (e.g., 'BRN')")


class Employer(AirwallexModel):
    """Model for employer information."""
    business_name: str = Field(..., description="Business name")
    business_identifiers: Optional[List[BusinessIdentifier]] = Field(None, description="Business identifiers")


class Merchant(AirwallexModel):
    """Model for merchant information."""
    category_code: Optional[str] = Field(None, description="Merchant category code")
    city: Optional[str] = Field(None, description="Merchant city")
    country: Optional[str] = Field(None, description="Merchant country")
    identifier: Optional[str] = Field(None, description="Merchant identifier")
    name: Optional[str] = Field(None, description="Merchant name")
    postcode: Optional[str] = Field(None, description="Merchant postal code")
    state: Optional[str] = Field(None, description="Merchant state")


class RiskDetails(AirwallexModel):
    """Model for risk details."""
    risk_actions_performed: Optional[List[str]] = Field(None, description="Risk actions performed")
    risk_factors: Optional[List[str]] = Field(None, description="Risk factors identified")
    three_dsecure_outcome: Optional[str] = Field(None, description="3D Secure outcome")


class DeviceInformation(AirwallexModel):
    """Model for device information."""
    device_id: Optional[str] = Field(None, description="Device identifier")
    device_type: Optional[str] = Field(None, description="Device type")


class TransactionUsage(AirwallexModel):
    """Model for transaction usage."""
    transaction_scope: str = Field(..., description="Transaction scope (e.g., 'MAGSTRIPE')")
    usage_scope: str = Field(..., description="Usage scope (e.g., 'INTERNATIONAL')")


class DeliveryDetails(AirwallexModel):
    """Model for delivery details."""
    delivery_method: Optional[str] = Field(None, description="Delivery method")
    tracking_number: Optional[str] = Field(None, description="Tracking number")
    courier: Optional[str] = Field(None, description="Courier")
    status: Optional[str] = Field(None, description="Delivery status")
    estimated_delivery_date: Optional[datetime] = Field(None, description="Estimated delivery date")


class HasMoreResponse(AirwallexModel):
    """Base model for paginated responses with has_more field."""
    has_more: bool = Field(..., description="Whether there are more items available")
    items: List[Any] = Field(..., description="List of items")
