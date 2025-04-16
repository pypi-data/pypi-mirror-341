"""
Models for the Airwallex Issuing Transaction Dispute API.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import Field
from .base import AirwallexModel


class DisputeUpdateHistory(AirwallexModel):
    """Model for dispute update history."""
    evidence_files: Optional[List[str]] = Field(None, description="Evidence files")
    note: Optional[str] = Field(None, description="Note")
    updated_at: datetime = Field(..., description="Update timestamp")
    updated_by: str = Field(..., description="Entity that performed the update")


class TransactionDisputeCreateRequest(AirwallexModel):
    """Model for transaction dispute creation request."""
    amount: Optional[float] = Field(None, description="The amount to be disputed")
    evidence_files: Optional[List[str]] = Field(None, description="Evidence file IDs")
    notes: Optional[str] = Field(None, description="Explanation for the dispute")
    reason: str = Field(..., description="The reason for raising the dispute")
    reference: Optional[str] = Field(None, description="Internal reference")
    transaction_id: str = Field(..., description="The transaction ID to dispute")


class TransactionDisputeUpdateRequest(AirwallexModel):
    """Model for transaction dispute update request."""
    amount: Optional[float] = Field(None, description="The disputed amount")
    evidence_files: Optional[List[str]] = Field(None, description="Evidence file IDs")
    notes: Optional[str] = Field(None, description="Explanation for the dispute")
    reason: Optional[str] = Field(None, description="The reason for raising the dispute")
    request_id: str = Field(..., description="A unique request ID")


class TransactionDispute(AirwallexModel):
    """Model for an Airwallex transaction dispute."""
    resource_name: str = "issuing/transaction_disputes"
    
    amount: float = Field(..., description="Dispute amount")
    created_at: datetime = Field(..., description="Creation timestamp")
    detailed_status: Optional[str] = Field(None, description="Detailed status")
    id: str = Field(..., description="Unique identifier")
    notes: Optional[str] = Field(None, description="Notes")
    reason: str = Field(..., description="Dispute reason")
    reference: Optional[str] = Field(None, description="Internal reference")
    status: str = Field(..., description="Status")
    transaction_id: str = Field(..., description="Transaction ID")
    update_history: List[DisputeUpdateHistory] = Field(..., description="Update history")
    updated_at: datetime = Field(..., description="Last update timestamp")
    updated_by: str = Field(..., description="Last updated by")


class TransactionDisputeListResponse(AirwallexModel):
    """Model for transaction dispute list response."""
    items: List[TransactionDispute] = Field(..., description="List of transaction disputes")
    page_after: Optional[str] = Field(None, description="Page bookmark for next page")
    page_before: Optional[str] = Field(None, description="Page bookmark for previous page")
