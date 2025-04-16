"""
Models for the Airwallex Issuing Cardholder API.
"""
from typing import Optional, List, Dict, Any, Literal
from pydantic import Field, EmailStr
from .base import AirwallexModel
from .issuing_common import Address, Name, Employer, HasMoreResponse


class Individual(AirwallexModel):
    """Model for individual cardholder details."""
    address: Address = Field(..., description="Address of the cardholder")
    cardholder_agreement_terms_consent_obtained: Optional[str] = Field(None, description="Whether consent was obtained")
    date_of_birth: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    employers: Optional[List[Employer]] = Field(None, description="Employers")
    express_consent_obtained: Optional[str] = Field(None, description="Whether express consent was obtained")
    name: Name = Field(..., description="Name of the cardholder")


class CardholderCreateRequest(AirwallexModel):
    """Model for cardholder creation request."""
    email: EmailStr = Field(..., description="Email address of the cardholder")
    individual: Individual = Field(..., description="Details about the cardholder")
    mobile_number: Optional[str] = Field(None, description="Mobile number of the cardholder")
    postal_address: Optional[Address] = Field(None, description="Postal address of the cardholder")
    type: str = Field(..., description="The type of cardholder (INDIVIDUAL or DELEGATE)")


class CardholderUpdateRequest(AirwallexModel):
    """Model for cardholder update request."""
    individual: Optional[Individual] = Field(None, description="Details about the cardholder")
    mobile_number: Optional[str] = Field(None, description="Mobile number of the cardholder")
    postal_address: Optional[Address] = Field(None, description="Postal address of the cardholder")
    type: Optional[str] = Field(None, description="The type of cardholder (INDIVIDUAL or DELEGATE)")


class Cardholder(AirwallexModel):
    """Model for an Airwallex cardholder."""
    resource_name: str = "issuing/cardholders"
    
    cardholder_id: str = Field(..., description="Unique Identifier for cardholder")
    email: EmailStr = Field(..., description="Email address of the cardholder")
    individual: Optional[Individual] = Field(None, description="Details about the cardholder")
    mobile_number: Optional[str] = Field(None, description="The mobile number of the cardholder")
    postal_address: Optional[Address] = Field(None, description="Postal address for the cardholder")
    status: str = Field(..., description="The status of the cardholder (PENDING, READY, DISABLED, INCOMPLETE)")
    type: str = Field(..., description="The type of cardholder (INDIVIDUAL or DELEGATE)")


class CardholderListResponse(HasMoreResponse):
    """Model for cardholder list response."""
    items: List[Cardholder] = Field(..., description="List of cardholders")
