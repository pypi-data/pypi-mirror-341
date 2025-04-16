"""
Models for the Airwallex FX API.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import Field
from .base import AirwallexModel


class ExchangeRate(AirwallexModel):
    """Model for exchange rate information."""
    source_currency: str = Field(..., description="Source currency code (ISO 4217)")
    target_currency: str = Field(..., description="Target currency code (ISO 4217)")
    rate: float = Field(..., description="Exchange rate")
    timestamp: datetime = Field(..., description="Timestamp when the rate was fetched")


class FXQuote(AirwallexModel):
    """Model for FX quote."""
    id: str = Field(..., description="Quote ID")
    source_currency: str = Field(..., description="Source currency code (ISO 4217)")
    target_currency: str = Field(..., description="Target currency code (ISO 4217)")
    source_amount: Optional[float] = Field(None, description="Source amount")
    target_amount: Optional[float] = Field(None, description="Target amount")
    rate: float = Field(..., description="Exchange rate")
    fee: Optional[Dict[str, Any]] = Field(None, description="Fee details")
    expires_at: datetime = Field(..., description="Quote expiration timestamp")
    created_at: datetime = Field(..., description="Quote creation timestamp")


class FXConversion(AirwallexModel):
    """Model for an FX conversion."""
    resource_name: str = "fx/conversions"
    
    id: str = Field(..., description="Conversion ID")
    request_id: str = Field(..., description="Client-generated request ID")
    source_currency: str = Field(..., description="Source currency code (ISO 4217)")
    target_currency: str = Field(..., description="Target currency code (ISO 4217)")
    source_amount: float = Field(..., description="Source amount")
    target_amount: float = Field(..., description="Target amount")
    rate: float = Field(..., description="Exchange rate")
    status: str = Field(..., description="Conversion status")
    created_at: datetime = Field(..., description="Conversion creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Conversion last update timestamp")
    account_id: str = Field(..., description="Source account ID")
    settlement_date: Optional[datetime] = Field(None, description="Settlement date")
    quote_id: Optional[str] = Field(None, description="Quote ID used for this conversion")


class FXConversionCreateRequest(AirwallexModel):
    """Model for FX conversion creation request."""
    request_id: str = Field(..., description="Client-generated unique ID for the request")
    source_currency: str = Field(..., description="Source currency code (ISO 4217)")
    target_currency: str = Field(..., description="Target currency code (ISO 4217)")
    source_amount: Optional[float] = Field(None, description="Source amount (required if target_amount is not provided)")
    target_amount: Optional[float] = Field(None, description="Target amount (required if source_amount is not provided)")
    account_id: str = Field(..., description="Source account ID")
    quote_id: Optional[str] = Field(None, description="Quote ID to use for this conversion")
