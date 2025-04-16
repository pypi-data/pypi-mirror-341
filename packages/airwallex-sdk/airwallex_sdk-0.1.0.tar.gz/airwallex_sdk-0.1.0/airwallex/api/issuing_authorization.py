"""
Airwallex Issuing Authorization API.
"""
from typing import Dict, Any, List, Optional, Type, TypeVar, Union, cast
from datetime import datetime
from ..models.issuing_authorization import Authorization, AuthorizationListResponse
from .base import AirwallexAPIBase

T = TypeVar("T", bound=Authorization)


class IssuingAuthorization(AirwallexAPIBase[Authorization]):
    """
    Operations for Airwallex issuing authorizations.
    
    Authorizations represent pre-auth and capture processed against individual cards.
    """
    endpoint = "issuing/authorizations"
    model_class = cast(Type[Authorization], Authorization)
    
    def list_with_filters(
        self,
        billing_currency: Optional[str] = None,
        card_id: Optional[str] = None,
        digital_wallet_token_id: Optional[str] = None,
        from_created_at: Optional[Union[str, datetime]] = None,
        lifecycle_id: Optional[str] = None,
        page_num: int = 0,
        page_size: int = 10,
        retrieval_ref: Optional[str] = None,
        status: Optional[str] = None,
        to_created_at: Optional[Union[str, datetime]] = None,
    ) -> List[Authorization]:
        """
        List authorizations with filtering options.
        
        Args:
            billing_currency: Currency in which transition was billed (3-letter ISO-4217 code)
            card_id: Unique Identifier for card
            digital_wallet_token_id: Unique Identifier for digital token
            from_created_at: Start of Transaction Date in ISO8601 format (inclusive)
            lifecycle_id: Unique Identifier for lifecycle
            page_num: Page number, starts from 0
            page_size: Number of results per page
            retrieval_ref: Retrieval reference number
            status: Authorization status (CLEARED, EXPIRED, FAILED, PENDING, REVERSED)
            to_created_at: End of Transaction Date in ISO8601 format (exclusive)
            
        Returns:
            List[Authorization]: List of matching authorizations
        """
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if billing_currency:
            params["billing_currency"] = billing_currency
        
        if card_id:
            params["card_id"] = card_id
            
        if digital_wallet_token_id:
            params["digital_wallet_token_id"] = digital_wallet_token_id
            
        if from_created_at:
            if isinstance(from_created_at, datetime):
                from_created_at = from_created_at.isoformat()
            params["from_created_at"] = from_created_at
            
        if lifecycle_id:
            params["lifecycle_id"] = lifecycle_id
            
        if retrieval_ref:
            params["retrieval_ref"] = retrieval_ref
            
        if status:
            params["status"] = status
            
        if to_created_at:
            if isinstance(to_created_at, datetime):
                to_created_at = to_created_at.isoformat()
            params["to_created_at"] = to_created_at
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", self._build_url(), params=params)
            data = response.json()
            return [self.model_class.from_api_response(item) for item in data.get("items", [])]
        else:
            raise ValueError("Use list_with_filters_async for async clients")
    
    async def list_with_filters_async(
        self,
        billing_currency: Optional[str] = None,
        card_id: Optional[str] = None,
        digital_wallet_token_id: Optional[str] = None,
        from_created_at: Optional[Union[str, datetime]] = None,
        lifecycle_id: Optional[str] = None,
        page_num: int = 0,
        page_size: int = 10,
        retrieval_ref: Optional[str] = None,
        status: Optional[str] = None,
        to_created_at: Optional[Union[str, datetime]] = None,
    ) -> List[Authorization]:
        """
        List authorizations with filtering options asynchronously.
        
        Args:
            billing_currency: Currency in which transition was billed (3-letter ISO-4217 code)
            card_id: Unique Identifier for card
            digital_wallet_token_id: Unique Identifier for digital token
            from_created_at: Start of Transaction Date in ISO8601 format (inclusive)
            lifecycle_id: Unique Identifier for lifecycle
            page_num: Page number, starts from 0
            page_size: Number of results per page
            retrieval_ref: Retrieval reference number
            status: Authorization status (CLEARED, EXPIRED, FAILED, PENDING, REVERSED)
            to_created_at: End of Transaction Date in ISO8601 format (exclusive)
            
        Returns:
            List[Authorization]: List of matching authorizations
        """
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if billing_currency:
            params["billing_currency"] = billing_currency
        
        if card_id:
            params["card_id"] = card_id
            
        if digital_wallet_token_id:
            params["digital_wallet_token_id"] = digital_wallet_token_id
            
        if from_created_at:
            if isinstance(from_created_at, datetime):
                from_created_at = from_created_at.isoformat()
            params["from_created_at"] = from_created_at
            
        if lifecycle_id:
            params["lifecycle_id"] = lifecycle_id
            
        if retrieval_ref:
            params["retrieval_ref"] = retrieval_ref
            
        if status:
            params["status"] = status
            
        if to_created_at:
            if isinstance(to_created_at, datetime):
                to_created_at = to_created_at.isoformat()
            params["to_created_at"] = to_created_at
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", self._build_url(), params=params)
            data = response.json()
            return [self.model_class.from_api_response(item) for item in data.get("items", [])]
        else:
            raise ValueError("Use list_with_filters for sync clients")
    
    def paginate(self, **params: Any) -> List[Authorization]:
        """
        Fetch all pages of authorizations.
        
        Args:
            **params: Filter parameters to pass to the API
            
        Returns:
            List[Authorization]: All authorizations matching the filters
        """
        if str(self.client.__class__.__name__).startswith('Async'):
            raise ValueError("This method requires a sync client.")
            
        all_items: List[Dict[str, Any]] = []
        page_num = params.get("page_num", 0)
        page_size = params.get("page_size", 10)
        
        while True:
            params["page_num"] = page_num
            params["page_size"] = page_size
            
            response = self.client._request("GET", self._build_url(), params=params)
            data = response.json()
            
            items = data.get("items", [])
            has_more = data.get("has_more", False)
            
            if not items:
                break
                
            all_items.extend(items)
            
            if not has_more:
                break
                
            page_num += 1
                
        return [self.model_class.from_api_response(item) for item in all_items]
    
    async def paginate_async(self, **params: Any) -> List[Authorization]:
        """
        Fetch all pages of authorizations asynchronously.
        
        Args:
            **params: Filter parameters to pass to the API
            
        Returns:
            List[Authorization]: All authorizations matching the filters
        """
        if not self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires an async client.")
            
        all_items: List[Dict[str, Any]] = []
        page_num = params.get("page_num", 0)
        page_size = params.get("page_size", 10)
        
        while True:
            params["page_num"] = page_num
            params["page_size"] = page_size
            
            response = await self.client._request("GET", self._build_url(), params=params)
            data = response.json()
            
            items = data.get("items", [])
            has_more = data.get("has_more", False)
            
            if not items:
                break
                
            all_items.extend(items)
            
            if not has_more:
                break
                
            page_num += 1
                
        return [self.model_class.from_api_response(item) for item in all_items]
    
    def paginate_generator(self, **params: Any):
        """
        Generate items one by one from paginated results.
        
        Args:
            **params: Filter parameters to pass to the API
            
        Yields:
            Authorization: Authorization objects one by one
        """
        if self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires a sync client.")
            
        page_num = params.get("page_num", 0)
        page_size = params.get("page_size", 10)
        
        while True:
            params["page_num"] = page_num
            params["page_size"] = page_size
            
            response = self.client._request("GET", self._build_url(), params=params)
            data = response.json()
            
            items = data.get("items", [])
            has_more = data.get("has_more", False)
            
            if not items:
                break
                
            for item in items:
                yield self.model_class.from_api_response(item)
            
            if not has_more:
                break
                
            page_num += 1
    
    async def paginate_async_generator(self, **params: Any):
        """
        Generate items one by one from paginated results asynchronously.
        
        Args:
            **params: Filter parameters to pass to the API
            
        Yields:
            Authorization: Authorization objects one by one
        """
        if not self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires an async client.")
            
        page_num = params.get("page_num", 0)
        page_size = params.get("page_size", 10)
        
        while True:
            params["page_num"] = page_num
            params["page_size"] = page_size
            
            response = await self.client._request("GET", self._build_url(), params=params)
            data = response.json()
            
            items = data.get("items", [])
            has_more = data.get("has_more", False)
            
            if not items:
                break
                
            for item in items:
                yield self.model_class.from_api_response(item)
            
            if not has_more:
                break
                
            page_num += 1
