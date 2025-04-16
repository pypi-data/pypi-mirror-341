"""
Models for the Airwallex Invoice API.
"""
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import Field, validator
from .base import AirwallexModel


class RecurringBilling(AirwallexModel):
    """Model for recurring billing information."""
    period: int = Field(..., description="The length of the billing cycle")
    period_unit: str = Field(..., description="The unit of the billing cycle, e.g., 'MONTH', 'YEAR'")


class PriceTier(AirwallexModel):
    """Model for price tier information."""
    amount: float = Field(..., description="The price for this tier")
    upper_bound: Optional[float] = Field(None, description="The upper bound of this tier")


class Price(AirwallexModel):
    """Model for price information."""
    id: str = Field(..., description="Unique price ID")
    name: str = Field(..., description="Price name")
    description: Optional[str] = Field(None, description="Price description")
    active: bool = Field(..., description="Whether this price is active")
    currency: str = Field(..., description="Currency code (ISO 4217)")
    product_id: str = Field(..., description="ID of the associated product")
    pricing_model: str = Field(..., description="Pricing model type (e.g., 'tiered')")
    recurring: Optional[RecurringBilling] = Field(None, description="Recurring billing details")
    tiers: Optional[List[PriceTier]] = Field(None, description="Pricing tiers for tiered pricing")
    metadata: Optional[Dict[str, str]] = Field(None, description="Additional metadata")
    request_id: Optional[str] = Field(None, description="Request ID when creating this price")


class InvoiceItem(AirwallexModel):
    """Model for an Airwallex invoice item."""
    id: str = Field(..., description="Unique invoice item ID")
    invoice_id: str = Field(..., description="ID of the invoice this item belongs to")
    amount: float = Field(..., description="Amount for this invoice item")
    currency: str = Field(..., description="Currency code (ISO 4217)")
    period_start_at: datetime = Field(..., description="Billing period start (inclusive)")
    period_end_at: datetime = Field(..., description="Billing period end (exclusive)")
    price: Price = Field(..., description="Price details")
    quantity: Optional[float] = Field(None, description="Product quantity")


class Invoice(AirwallexModel):
    """Model for an Airwallex invoice."""
    resource_name: str = "invoices"
    
    id: str = Field(..., description="Unique invoice ID")
    customer_id: str = Field(..., description="ID of the customer who will be charged")
    subscription_id: Optional[str] = Field(None, description="ID of the subscription which generated this invoice")
    currency: str = Field(..., description="Currency code (ISO 4217)")
    total_amount: float = Field(..., description="Total amount of the invoice")
    status: str = Field(..., description="Invoice status (SENT, PAID, PAYMENT_FAILED)")
    payment_intent_id: Optional[str] = Field(None, description="ID of the associated payment intent")
    period_start_at: datetime = Field(..., description="Billing period start (inclusive)")
    period_end_at: datetime = Field(..., description="Billing period end (exclusive)")
    created_at: datetime = Field(..., description="Invoice creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Invoice last update timestamp")
    paid_at: Optional[datetime] = Field(None, description="Timestamp when invoice was paid")
    last_payment_attempt_at: Optional[datetime] = Field(None, description="Timestamp of last payment attempt")
    next_payment_attempt_at: Optional[datetime] = Field(None, description="Timestamp of next scheduled payment attempt")
    past_payment_attempt_count: Optional[int] = Field(None, description="Number of payment attempts made so far")
    remaining_payment_attempt_count: Optional[int] = Field(None, description="Number of remaining payment attempts")
    items: Optional[List[InvoiceItem]] = Field(None, description="Invoice items")
    
    @validator('status')
    def validate_status(cls, v):
        """Validate invoice status."""
        valid_statuses = ['SENT', 'PAID', 'PAYMENT_FAILED']
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        return v


class InvoicePreviewRequest(AirwallexModel):
    """Model for invoice preview request."""
    customer_id: str = Field(..., description="ID of the customer for this invoice")
    subscription_id: Optional[str] = Field(None, description="ID of the subscription to preview the invoice for")
    trial_end_at: Optional[datetime] = Field(None, description="End of the trial period if applicable")
    recurring: Optional[RecurringBilling] = Field(None, description="Recurring billing details")
    
    class SubscriptionItem(AirwallexModel):
        """Model for subscription item in invoice preview."""
        price_id: str = Field(..., description="ID of the price")
        quantity: float = Field(1, description="Quantity of the product")
    
    items: Optional[List[SubscriptionItem]] = Field(None, description="List of subscription items")


class InvoicePreviewResponse(AirwallexModel):
    """Model for invoice preview response."""
    customer_id: str = Field(..., description="ID of the customer for this invoice")
    subscription_id: Optional[str] = Field(None, description="ID of the subscription for this invoice")
    currency: str = Field(..., description="Currency code (ISO 4217)")
    total_amount: float = Field(..., description="Total amount of the invoice")
    created_at: datetime = Field(..., description="Expected invoice creation timestamp")
    items: List[InvoiceItem] = Field(..., description="Invoice items in the preview")
