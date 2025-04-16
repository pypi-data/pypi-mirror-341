"""
Airwallex Invoice API.
"""
from typing import Dict, Any, List, Optional, Type, TypeVar, Union, cast
from datetime import datetime
from ..models.invoice import Invoice, InvoiceItem, InvoicePreviewRequest, InvoicePreviewResponse
from .base import AirwallexAPIBase

T = TypeVar("T", bound=Invoice)


class Invoice(AirwallexAPIBase[Invoice]):
    """
    Operations for Airwallex invoices.
    
    Invoices record one-off sales transactions between you and your customers.
    """
    endpoint = "invoices"
    model_class = cast(Type[Invoice], Invoice)
    
    def preview(self, preview_request: InvoicePreviewRequest) -> InvoicePreviewResponse:
        """
        Preview an upcoming invoice.
        
        This method allows you to preview the upcoming invoice of an existing subscription
        or the first invoice before creating a new subscription.
        
        Args:
            preview_request: InvoicePreviewRequest model with preview details
            
        Returns:
            InvoicePreviewResponse: The preview of the upcoming invoice
        """
        url = self._build_url(suffix="preview")
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url, json=preview_request.to_api_dict())
            return InvoicePreviewResponse.from_api_response(response.json())
        else:
            raise ValueError("Use preview_async for async clients")
    
    async def preview_async(self, preview_request: InvoicePreviewRequest) -> InvoicePreviewResponse:
        """
        Preview an upcoming invoice asynchronously.
        
        This method allows you to preview the upcoming invoice of an existing subscription
        or the first invoice before creating a new subscription.
        
        Args:
            preview_request: InvoicePreviewRequest model with preview details
            
        Returns:
            InvoicePreviewResponse: The preview of the upcoming invoice
        """
        url = self._build_url(suffix="preview")
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url, json=preview_request.to_api_dict())
            return InvoicePreviewResponse.from_api_response(response.json())
        else:
            raise ValueError("Use preview for sync clients")
    
    def list_items(self, invoice_id: str, page_num: int = 0, page_size: int = 20) -> List[InvoiceItem]:
        """
        List all items for a specific invoice.
        
        Args:
            invoice_id: The ID of the invoice to fetch items for
            page_num: Page number (0-indexed) for pagination
            page_size: Number of items per page
            
        Returns:
            List[InvoiceItem]: List of invoice items
        """
        url = f"{self._build_url(invoice_id)}/items"
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", url, params=params)
            data = response.json()
            
            if "items" in data:
                return [InvoiceItem.from_api_response(item) for item in data["items"]]
            return []
        else:
            raise ValueError("Use list_items_async for async clients")
    
    async def list_items_async(self, invoice_id: str, page_num: int = 0, page_size: int = 20) -> List[InvoiceItem]:
        """
        List all items for a specific invoice asynchronously.
        
        Args:
            invoice_id: The ID of the invoice to fetch items for
            page_num: Page number (0-indexed) for pagination
            page_size: Number of items per page
            
        Returns:
            List[InvoiceItem]: List of invoice items
        """
        url = f"{self._build_url(invoice_id)}/items"
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", url, params=params)
            data = response.json()
            
            if "items" in data:
                return [InvoiceItem.from_api_response(item) for item in data["items"]]
            return []
        else:
            raise ValueError("Use list_items for sync clients")
    
    def get_item(self, invoice_id: str, item_id: str) -> InvoiceItem:
        """
        Retrieve a specific invoice item.
        
        Args:
            invoice_id: The ID of the invoice that contains the item
            item_id: The ID of the invoice item to retrieve
            
        Returns:
            InvoiceItem: The requested invoice item
        """
        url = f"{self._build_url(invoice_id)}/items/{item_id}"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", url)
            return InvoiceItem.from_api_response(response.json())
        else:
            raise ValueError("Use get_item_async for async clients")
    
    async def get_item_async(self, invoice_id: str, item_id: str) -> InvoiceItem:
        """
        Retrieve a specific invoice item asynchronously.
        
        Args:
            invoice_id: The ID of the invoice that contains the item
            item_id: The ID of the invoice item to retrieve
            
        Returns:
            InvoiceItem: The requested invoice item
        """
        url = f"{self._build_url(invoice_id)}/items/{item_id}"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", url)
            return InvoiceItem.from_api_response(response.json())
        else:
            raise ValueError("Use get_item for sync clients")
    
    def list_with_filters(
        self, 
        customer_id: Optional[str] = None,
        subscription_id: Optional[str] = None,
        status: Optional[str] = None,
        from_created_at: Optional[Union[str, datetime]] = None,
        to_created_at: Optional[Union[str, datetime]] = None,
        page_num: int = 0,
        page_size: int = 20
    ) -> List[Invoice]:
        """
        List invoices with filtering options.
        
        Args:
            customer_id: Filter by customer ID
            subscription_id: Filter by subscription ID
            status: Filter by status (SENT, PAID, PAYMENT_FAILED)
            from_created_at: Filter by creation date (start, inclusive)
            to_created_at: Filter by creation date (end, exclusive)
            page_num: Page number (0-indexed) for pagination
            page_size: Number of invoices per page
            
        Returns:
            List[Invoice]: List of matching invoices
        """
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if customer_id:
            params["customer_id"] = customer_id
        
        if subscription_id:
            params["subscription_id"] = subscription_id
        
        if status:
            params["status"] = status
        
        if from_created_at:
            if isinstance(from_created_at, datetime):
                from_created_at = from_created_at.isoformat()
            params["from_created_at"] = from_created_at
        
        if to_created_at:
            if isinstance(to_created_at, datetime):
                to_created_at = to_created_at.isoformat()
            params["to_created_at"] = to_created_at
        
        return self.list(**params)
    
    async def list_with_filters_async(
        self, 
        customer_id: Optional[str] = None,
        subscription_id: Optional[str] = None,
        status: Optional[str] = None,
        from_created_at: Optional[Union[str, datetime]] = None,
        to_created_at: Optional[Union[str, datetime]] = None,
        page_num: int = 0,
        page_size: int = 20
    ) -> List[Invoice]:
        """
        List invoices with filtering options asynchronously.
        
        Args:
            customer_id: Filter by customer ID
            subscription_id: Filter by subscription ID
            status: Filter by status (SENT, PAID, PAYMENT_FAILED)
            from_created_at: Filter by creation date (start, inclusive)
            to_created_at: Filter by creation date (end, exclusive)
            page_num: Page number (0-indexed) for pagination
            page_size: Number of invoices per page
            
        Returns:
            List[Invoice]: List of matching invoices
        """
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if customer_id:
            params["customer_id"] = customer_id
        
        if subscription_id:
            params["subscription_id"] = subscription_id
        
        if status:
            params["status"] = status
        
        if from_created_at:
            if isinstance(from_created_at, datetime):
                from_created_at = from_created_at.isoformat()
            params["from_created_at"] = from_created_at
        
        if to_created_at:
            if isinstance(to_created_at, datetime):
                to_created_at = to_created_at.isoformat()
            params["to_created_at"] = to_created_at
        
        return await self.list_async(**params)
