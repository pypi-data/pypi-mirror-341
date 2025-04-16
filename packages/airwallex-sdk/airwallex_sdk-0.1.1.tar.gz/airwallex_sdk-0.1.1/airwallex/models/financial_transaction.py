"""
Models for the Airwallex financial transaction API.
"""
from typing import Optional
from datetime import datetime
from pydantic import Field
from .base import AirwallexModel


class FinancialTransaction(AirwallexModel):
    """Model for an Airwallex financial transaction."""
    resource_name: str = "financial_transactions"
    
    id: str = Field(..., description="ID of the transaction")
    amount: float = Field(..., description="Gross amount of the transaction")
    net: float = Field(..., description="Net amount of the transaction")
    fee: float = Field(..., description="Fee paid for the transaction")
    currency: str = Field(..., description="Currency of the transaction (3-letter ISO-4217 code)")
    status: str = Field(..., description="Status of the transaction (PENDING, SETTLED, CANCELLED)")
    description: Optional[str] = Field(None, description="Description of the transaction")
    batch_id: Optional[str] = Field(None, description="Batch ID of the settlement the transaction belongs to")
    client_rate: Optional[float] = Field(None, description="Client rate for the transaction")
    currency_pair: Optional[str] = Field(None, description="Currency pair that the client_rate is quoted in")
    source_id: Optional[str] = Field(None, description="Source ID of the transaction")
    source_type: Optional[str] = Field(None, description="Type of the source transaction")
    transaction_type: Optional[str] = Field(None, description="Type of the transaction")
    funding_source_id: Optional[str] = Field(None, description="ID of the funding source")
    created_at: datetime = Field(..., description="Transaction creation timestamp")
    estimated_settled_at: Optional[datetime] = Field(None, description="Estimated settlement timestamp")
    settled_at: Optional[datetime] = Field(None, description="Actual settlement timestamp")