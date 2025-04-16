"""
Airwallex Issuing Digital Wallet Token API.
"""
from typing import Dict, Any, List, Optional, Type, TypeVar, Union, cast
from datetime import datetime
from ..models.issuing_digital_wallet_token import DigitalWalletToken
from .base import AirwallexAPIBase

T = TypeVar("T", bound=DigitalWalletToken)


class IssuingDigitalWalletToken(AirwallexAPIBase[DigitalWalletToken]):
    """
    Operations for Airwallex issuing digital wallet tokens.
    
    Digital wallet tokens represent tokenized cards in digital wallets.
    """
    endpoint = "issuing/digital_wallet_tokens"
    model_class = cast(Type[DigitalWalletToken], DigitalWalletToken)
    
    def list_with_filters(
        self,
        card_id: Optional[str] = None,
        cardholder_id: Optional[str] = None,
        from_created_at: Optional[Union[str, datetime]] = None,
        from_token_expires_on: Optional[str] = None,
        to_created_at: Optional[Union[str, datetime]] = None,
        to_token_expires_on: Optional[str] = None,
        token_reference_id: Optional[str] = None,
        token_statuses: Optional[str] = None,
        token_types: Optional[str] = None,
        page_num: int = 0,
        page_size: int = 10
    ) -> List[DigitalWalletToken]:
        """
        List digital wallet tokens with filtering options.
        
        Args:
            card_id: Filter by card ID
            cardholder_id: Filter by cardholder ID
            from_created_at: Filter by creation date (start, inclusive)
            from_token_expires_on: Filter by expiration date (start, inclusive, format MMyy)
            to_created_at: Filter by creation date (end, inclusive)
            to_token_expires_on: Filter by expiration date (end, inclusive, format MMyy)
            token_reference_id: Filter by token reference ID
            token_statuses: Filter by token statuses (comma-separated)
            token_types: Filter by token types (comma-separated)
            page_num: Page number, starts from 0
            page_size: Number of results per page
            
        Returns:
            List[DigitalWalletToken]: List of matching digital wallet tokens
        """
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if card_id:
            params["card_id"] = card_id
        
        if cardholder_id:
            params["cardholder_id"] = cardholder_id
            
        if from_created_at:
            if isinstance(from_created_at, datetime):
                from_created_at = from_created_at.isoformat()
            params["from_created_at"] = from_created_at
            
        if from_token_expires_on:
            params["from_token_expires_on"] = from_token_expires_on
            
        if to_created_at:
            if isinstance(to_created_at, datetime):
                to_created_at = to_created_at.isoformat()
            params["to_created_at"] = to_created_at
            
        if to_token_expires_on:
            params["to_token_expires_on"] = to_token_expires_on
            
        if token_reference_id:
            params["token_reference_id"] = token_reference_id
            
        if token_statuses:
            params["token_statuses"] = token_statuses
            
        if token_types:
            params["token_types"] = token_types
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", self._build_url(), params=params)
            data = response.json()
            return [self.model_class.from_api_response(item) for item in data.get("items", [])]
        else:
            raise ValueError("Use list_with_filters_async for async clients")
    
    async def list_with_filters_async(
        self,
        card_id: Optional[str] = None,
        cardholder_id: Optional[str] = None,
        from_created_at: Optional[Union[str, datetime]] = None,
        from_token_expires_on: Optional[str] = None,
        to_created_at: Optional[Union[str, datetime]] = None,
        to_token_expires_on: Optional[str] = None,
        token_reference_id: Optional[str] = None,
        token_statuses: Optional[str] = None,
        token_types: Optional[str] = None,
        page_num: int = 0,
        page_size: int = 10
    ) -> List[DigitalWalletToken]:
        """
        List digital wallet tokens with filtering options asynchronously.
        
        Args:
            card_id: Filter by card ID
            cardholder_id: Filter by cardholder ID
            from_created_at: Filter by creation date (start, inclusive)
            from_token_expires_on: Filter by expiration date (start, inclusive, format MMyy)
            to_created_at: Filter by creation date (end, inclusive)
            to_token_expires_on: Filter by expiration date (end, inclusive, format MMyy)
            token_reference_id: Filter by token reference ID
            token_statuses: Filter by token statuses (comma-separated)
            token_types: Filter by token types (comma-separated)
            page_num: Page number, starts from 0
            page_size: Number of results per page
            
        Returns:
            List[DigitalWalletToken]: List of matching digital wallet tokens
        """
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if card_id:
            params["card_id"] = card_id
        
        if cardholder_id:
            params["cardholder_id"] = cardholder_id
            
        if from_created_at:
            if isinstance(from_created_at, datetime):
                from_created_at = from_created_at.isoformat()
            params["from_created_at"] = from_created_at
            
        if from_token_expires_on:
            params["from_token_expires_on"] = from_token_expires_on
            
        if to_created_at:
            if isinstance(to_created_at, datetime):
                to_created_at = to_created_at.isoformat()
            params["to_created_at"] = to_created_at
            
        if to_token_expires_on:
            params["to_token_expires_on"] = to_token_expires_on
            
        if token_reference_id:
            params["token_reference_id"] = token_reference_id
            
        if token_statuses:
            params["token_statuses"] = token_statuses
            
        if token_types:
            params["token_types"] = token_types
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", self._build_url(), params=params)
            data = response.json()
            return [self.model_class.from_api_response(item) for item in data.get("items", [])]
        else:
            raise ValueError("Use list_with_filters for sync clients")
    
    def paginate(self, **params: Any) -> List[DigitalWalletToken]:
        """
        Fetch all pages of digital wallet tokens.
        
        Args:
            **params: Filter parameters to pass to the API
            
        Returns:
            List[DigitalWalletToken]: All digital wallet tokens matching the filters
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
    
    async def paginate_async(self, **params: Any) -> List[DigitalWalletToken]:
        """
        Fetch all pages of digital wallet tokens asynchronously.
        
        Args:
            **params: Filter parameters to pass to the API
            
        Returns:
            List[DigitalWalletToken]: All digital wallet tokens matching the filters
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
