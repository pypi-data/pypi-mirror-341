"""
Airwallex Payment API.
"""
from typing import Dict, Any, List, Optional, Type, TypeVar, Union, cast
from ..models.payment import Payment, PaymentCreateRequest, PaymentUpdateRequest, PaymentQuote
from .base import AirwallexAPIBase

T = TypeVar("T", bound=Payment)


class Payment(AirwallexAPIBase[Payment]):
    """
    Operations for Airwallex payments.
    
    Payments represent money transfers to beneficiaries.
    """
    endpoint = "payments"
    model_class = cast(Type[Payment], Payment)
    
    def create_from_model(self, payment: PaymentCreateRequest) -> Payment:
        """
        Create a new payment using a Pydantic model.
        
        Args:
            payment: PaymentCreateRequest model with payment creation details.
            
        Returns:
            Payment: The created payment.
        """
        return self.create(payment)
    
    async def create_from_model_async(self, payment: PaymentCreateRequest) -> Payment:
        """
        Create a new payment using a Pydantic model asynchronously.
        
        Args:
            payment: PaymentCreateRequest model with payment creation details.
            
        Returns:
            Payment: The created payment.
        """
        return await self.create_async(payment)
    
    def update_from_model(self, payment_id: str, payment: PaymentUpdateRequest) -> Payment:
        """
        Update a payment using a Pydantic model.
        
        Args:
            payment_id: The ID of the payment to update.
            payment: PaymentUpdateRequest model with payment update details.
            
        Returns:
            Payment: The updated payment.
        """
        return self.update(payment_id, payment)
    
    async def update_from_model_async(self, payment_id: str, payment: PaymentUpdateRequest) -> Payment:
        """
        Update a payment using a Pydantic model asynchronously.
        
        Args:
            payment_id: The ID of the payment to update.
            payment: PaymentUpdateRequest model with payment update details.
            
        Returns:
            Payment: The updated payment.
        """
        return await self.update_async(payment_id, payment)
    
    def cancel(self, payment_id: str) -> Payment:
        """
        Cancel a payment.
        
        Args:
            payment_id: The ID of the payment to cancel.
            
        Returns:
            Payment: The cancelled payment.
        """
        update_request = PaymentUpdateRequest(status="cancelled")
        return self.update(payment_id, update_request)
    
    async def cancel_async(self, payment_id: str) -> Payment:
        """
        Cancel a payment asynchronously.
        
        Args:
            payment_id: The ID of the payment to cancel.
            
        Returns:
            Payment: The cancelled payment.
        """
        update_request = PaymentUpdateRequest(status="cancelled")
        return await self.update_async(payment_id, update_request)
    
    def get_quote(self, source_currency: str, target_currency: str, amount: float, source_type: str = "source") -> PaymentQuote:
        """
        Get a quote for a payment.
        
        Args:
            source_currency: Source currency code (ISO 4217)
            target_currency: Target currency code (ISO 4217)
            amount: Amount to convert
            source_type: Whether the amount is in the source or target currency ('source' or 'target')
            
        Returns:
            PaymentQuote: The payment quote.
        """
        url = self._build_url(suffix="quote")
        payload = {
            "source_currency": source_currency,
            "target_currency": target_currency,
            "amount": amount,
            "source_type": source_type
        }
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url, json=payload)
            return PaymentQuote.from_api_response(response.json())
        else:
            raise ValueError("Use get_quote_async for async clients")
    
    async def get_quote_async(self, source_currency: str, target_currency: str, amount: float, source_type: str = "source") -> PaymentQuote:
        """
        Get a quote for a payment asynchronously.
        
        Args:
            source_currency: Source currency code (ISO 4217)
            target_currency: Target currency code (ISO 4217)
            amount: Amount to convert
            source_type: Whether the amount is in the source or target currency ('source' or 'target')
            
        Returns:
            PaymentQuote: The payment quote.
        """
        url = self._build_url(suffix="quote")
        payload = {
            "source_currency": source_currency,
            "target_currency": target_currency,
            "amount": amount,
            "source_type": source_type
        }
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url, json=payload)
            return PaymentQuote.from_api_response(response.json())
        else:
            raise ValueError("Use get_quote for sync clients")
