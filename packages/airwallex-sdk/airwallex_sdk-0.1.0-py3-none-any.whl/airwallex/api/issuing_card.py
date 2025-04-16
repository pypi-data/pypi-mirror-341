"""
Airwallex Issuing Card API.
"""
from typing import Dict, Any, List, Optional, Type, TypeVar, Union, cast
from datetime import datetime
from ..models.issuing_card import Card, CardCreateRequest, CardUpdateRequest, CardDetails, CardLimits
from .base import AirwallexAPIBase

T = TypeVar("T", bound=Card)


class IssuingCard(AirwallexAPIBase[Card]):
    """
    Operations for Airwallex issuing cards.
    
    Cards represent virtual or physical payment cards associated with cardholders.
    """
    endpoint = "issuing/cards"
    model_class = cast(Type[Card], Card)
    
    def create_card(self, card: CardCreateRequest) -> Card:
        """
        Create a new card.
        
        Args:
            card: CardCreateRequest model with card details
            
        Returns:
            Card: The created card
        """
        url = f"{self.base_path}/create"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url, json=card.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use create_card_async for async clients")
    
    async def create_card_async(self, card: CardCreateRequest) -> Card:
        """
        Create a new card asynchronously.
        
        Args:
            card: CardCreateRequest model with card details
            
        Returns:
            Card: The created card
        """
        url = f"{self.base_path}/create"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url, json=card.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use create_card for sync clients")
    
    def get_card_details(self, card_id: str) -> CardDetails:
        """
        Get sensitive card details.
        
        Args:
            card_id: The ID of the card
            
        Returns:
            CardDetails: Sensitive card details
        """
        url = f"{self._build_url(card_id)}/details"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", url)
            return CardDetails.from_api_response(response.json())
        else:
            raise ValueError("Use get_card_details_async for async clients")
    
    async def get_card_details_async(self, card_id: str) -> CardDetails:
        """
        Get sensitive card details asynchronously.
        
        Args:
            card_id: The ID of the card
            
        Returns:
            CardDetails: Sensitive card details
        """
        url = f"{self._build_url(card_id)}/details"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", url)
            return CardDetails.from_api_response(response.json())
        else:
            raise ValueError("Use get_card_details for sync clients")
    
    def activate_card(self, card_id: str) -> None:
        """
        Activate a physical card.
        
        Args:
            card_id: The ID of the card to activate
        """
        url = f"{self._build_url(card_id)}/activate"
        
        if not self.client.__class__.__name__.startswith('Async'):
            self.client._request("POST", url)
        else:
            raise ValueError("Use activate_card_async for async clients")
    
    async def activate_card_async(self, card_id: str) -> None:
        """
        Activate a physical card asynchronously.
        
        Args:
            card_id: The ID of the card to activate
        """
        url = f"{self._build_url(card_id)}/activate"
        
        if self.client.__class__.__name__.startswith('Async'):
            await self.client._request("POST", url)
        else:
            raise ValueError("Use activate_card for sync clients")
    
    def get_card_limits(self, card_id: str) -> CardLimits:
        """
        Get card remaining limits.
        
        Args:
            card_id: The ID of the card
            
        Returns:
            CardLimits: Card remaining limits
        """
        url = f"{self._build_url(card_id)}/limits"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", url)
            return CardLimits.from_api_response(response.json())
        else:
            raise ValueError("Use get_card_limits_async for async clients")
    
    async def get_card_limits_async(self, card_id: str) -> CardLimits:
        """
        Get card remaining limits asynchronously.
        
        Args:
            card_id: The ID of the card
            
        Returns:
            CardLimits: Card remaining limits
        """
        url = f"{self._build_url(card_id)}/limits"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", url)
            return CardLimits.from_api_response(response.json())
        else:
            raise ValueError("Use get_card_limits for sync clients")
    
    def update_card(self, card_id: str, update_data: CardUpdateRequest) -> Card:
        """
        Update a card.
        
        Args:
            card_id: The ID of the card to update
            update_data: CardUpdateRequest model with update details
            
        Returns:
            Card: The updated card
        """
        url = f"{self._build_url(card_id)}/update"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url, json=update_data.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use update_card_async for async clients")
    
    async def update_card_async(self, card_id: str, update_data: CardUpdateRequest) -> Card:
        """
        Update a card asynchronously.
        
        Args:
            card_id: The ID of the card to update
            update_data: CardUpdateRequest model with update details
            
        Returns:
            Card: The updated card
        """
        url = f"{self._build_url(card_id)}/update"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url, json=update_data.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use update_card for sync clients")
    
    def list_with_filters(
        self,
        card_status: Optional[str] = None,
        cardholder_id: Optional[str] = None,
        from_created_at: Optional[Union[str, datetime]] = None,
        from_updated_at: Optional[Union[str, datetime]] = None,
        nick_name: Optional[str] = None,
        to_created_at: Optional[Union[str, datetime]] = None,
        to_updated_at: Optional[Union[str, datetime]] = None,
        page_num: int = 0,
        page_size: int = 10
    ) -> List[Card]:
        """
        List cards with filtering options.
        
        Args:
            card_status: Filter by status
            cardholder_id: Filter by cardholder ID
            from_created_at: Filter by creation date (start, inclusive)
            from_updated_at: Filter by update date (start, inclusive)
            nick_name: Filter by card nickname
            to_created_at: Filter by creation date (end, inclusive)
            to_updated_at: Filter by update date (end, inclusive)
            page_num: Page number, starts from 0
            page_size: Number of results per page
            
        Returns:
            List[Card]: List of matching cards
        """
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if card_status:
            params["card_status"] = card_status
        
        if cardholder_id:
            params["cardholder_id"] = cardholder_id
            
        if from_created_at:
            if isinstance(from_created_at, datetime):
                from_created_at = from_created_at.isoformat()
            params["from_created_at"] = from_created_at
            
        if from_updated_at:
            if isinstance(from_updated_at, datetime):
                from_updated_at = from_updated_at.isoformat()
            params["from_updated_at"] = from_updated_at
            
        if nick_name:
            params["nick_name"] = nick_name
            
        if to_created_at:
            if isinstance(to_created_at, datetime):
                to_created_at = to_created_at.isoformat()
            params["to_created_at"] = to_created_at
            
        if to_updated_at:
            if isinstance(to_updated_at, datetime):
                to_updated_at = to_updated_at.isoformat()
            params["to_updated_at"] = to_updated_at
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", self._build_url(), params=params)
            data = response.json()
            return [self.model_class.from_api_response(item) for item in data.get("items", [])]
        else:
            raise ValueError("Use list_with_filters_async for async clients")
    
    async def list_with_filters_async(
        self,
        card_status: Optional[str] = None,
        cardholder_id: Optional[str] = None,
        from_created_at: Optional[Union[str, datetime]] = None,
        from_updated_at: Optional[Union[str, datetime]] = None,
        nick_name: Optional[str] = None,
        to_created_at: Optional[Union[str, datetime]] = None,
        to_updated_at: Optional[Union[str, datetime]] = None,
        page_num: int = 0,
        page_size: int = 10
    ) -> List[Card]:
        """
        List cards with filtering options asynchronously.
        
        Args:
            card_status: Filter by status
            cardholder_id: Filter by cardholder ID
            from_created_at: Filter by creation date (start, inclusive)
            from_updated_at: Filter by update date (start, inclusive)
            nick_name: Filter by card nickname
            to_created_at: Filter by creation date (end, inclusive)
            to_updated_at: Filter by update date (end, inclusive)
            page_num: Page number, starts from 0
            page_size: Number of results per page
            
        Returns:
            List[Card]: List of matching cards
        """
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if card_status:
            params["card_status"] = card_status
        
        if cardholder_id:
            params["cardholder_id"] = cardholder_id
            
        if from_created_at:
            if isinstance(from_created_at, datetime):
                from_created_at = from_created_at.isoformat()
            params["from_created_at"] = from_created_at
            
        if from_updated_at:
            if isinstance(from_updated_at, datetime):
                from_updated_at = from_updated_at.isoformat()
            params["from_updated_at"] = from_updated_at
            
        if nick_name:
            params["nick_name"] = nick_name
            
        if to_created_at:
            if isinstance(to_created_at, datetime):
                to_created_at = to_created_at.isoformat()
            params["to_created_at"] = to_created_at
            
        if to_updated_at:
            if isinstance(to_updated_at, datetime):
                to_updated_at = to_updated_at.isoformat()
            params["to_updated_at"] = to_updated_at
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", self._build_url(), params=params)
            data = response.json()
            return [self.model_class.from_api_response(item) for item in data.get("items", [])]
        else:
            raise ValueError("Use list_with_filters for sync clients")
    
    def paginate(self, **params: Any) -> List[Card]:
        """
        Fetch all pages of cards.
        
        Args:
            **params: Filter parameters to pass to the API
            
        Returns:
            List[Card]: All cards matching the filters
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
    
    async def paginate_async(self, **params: Any) -> List[Card]:
        """
        Fetch all pages of cards asynchronously.
        
        Args:
            **params: Filter parameters to pass to the API
            
        Returns:
            List[Card]: All cards matching the filters
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
