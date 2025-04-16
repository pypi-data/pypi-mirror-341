"""
Models for the Airwallex beneficiary API.
"""
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import Field, EmailStr
from .base import AirwallexModel


class BankDetails(AirwallexModel):
    """Model for bank account details."""
    account_name: str = Field(..., description="Account holder name")
    account_number: Optional[str] = Field(None, description="Account number")
    swift_code: Optional[str] = Field(None, description="SWIFT/BIC code")
    iban: Optional[str] = Field(None, description="IBAN (International Bank Account Number)")
    bsb: Optional[str] = Field(None, description="BSB (Bank State Branch) for AU accounts")
    sort_code: Optional[str] = Field(None, description="Sort code for UK accounts")
    routing_number: Optional[str] = Field(None, description="ACH routing number for US accounts")
    bank_name: Optional[str] = Field(None, description="Bank name")
    bank_country_code: str = Field(..., description="Bank country code (ISO 3166-1 alpha-2)")
    bank_address: Optional[Dict[str, str]] = Field(None, description="Bank address details")


class Address(AirwallexModel):
    """Model for address details."""
    country_code: str = Field(..., description="Country code (ISO 3166-1 alpha-2)")
    state: Optional[str] = Field(None, description="State or province")
    city: str = Field(..., description="City")
    postcode: Optional[str] = Field(None, description="Postal or ZIP code")
    street_address: str = Field(..., description="Street address")
    street_address_2: Optional[str] = Field(None, description="Additional street address details")


class Beneficiary(AirwallexModel):
    """Model for an Airwallex beneficiary."""
    resource_name: str = "beneficiaries"
    
    id: str = Field(..., description="Unique beneficiary ID")
    name: str = Field(..., description="Beneficiary name")
    type: str = Field(..., description="Beneficiary type (e.g., 'bank_account', 'email')")
    email: Optional[EmailStr] = Field(None, description="Beneficiary email address")
    bank_details: Optional[BankDetails] = Field(None, description="Bank account details for bank_account type")
    address: Optional[Address] = Field(None, description="Beneficiary address")
    company_name: Optional[str] = Field(None, description="Beneficiary company name")
    entity_type: Optional[str] = Field(None, description="Beneficiary entity type (individual/company)")
    payment_methods: List[str] = Field(default_factory=list, description="Supported payment methods")
    status: str = Field(..., description="Beneficiary status")
    created_at: datetime = Field(..., description="Beneficiary creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Beneficiary last update timestamp")


class BeneficiaryCreateRequest(AirwallexModel):
    """Model for beneficiary creation request."""
    name: str = Field(..., description="Beneficiary name")
    type: str = Field(..., description="Beneficiary type (e.g., 'bank_account', 'email')")
    email: Optional[EmailStr] = Field(None, description="Beneficiary email address")
    bank_details: Optional[BankDetails] = Field(None, description="Bank account details for bank_account type")
    address: Optional[Address] = Field(None, description="Beneficiary address")
    company_name: Optional[str] = Field(None, description="Beneficiary company name")
    entity_type: Optional[str] = Field(None, description="Beneficiary entity type (individual/company)")


class BeneficiaryUpdateRequest(AirwallexModel):
    """Model for beneficiary update request."""
    name: Optional[str] = Field(None, description="Updated beneficiary name")
    email: Optional[EmailStr] = Field(None, description="Updated beneficiary email address")
    bank_details: Optional[BankDetails] = Field(None, description="Updated bank account details")
    address: Optional[Address] = Field(None, description="Updated beneficiary address")
    company_name: Optional[str] = Field(None, description="Updated beneficiary company name")
    status: Optional[str] = Field(None, description="Updated beneficiary status")
