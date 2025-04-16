"""
Airwallex Issuing Cardholder API.
"""
from typing import Dict, Any, List, Optional, Type, TypeVar, Union, cast
from ..models.issuing_cardholder import Cardholder, CardholderCreateRequest, CardholderUpdateRequest
from .base import AirwallexAPIBase

T = TypeVar("T", bound=Cardholder)


class IssuingCardholder(AirwallexAPIBase[Cardholder]):
    """
    Operations for Airwallex issuing cardholders.
    
    Cardholders are authorized representatives that can be issued cards.
    """
    endpoint = "issuing/cardholders"
    model_class = cast(Type[Cardholder], Cardholder)
    
    def create_cardholder(self, cardholder: CardholderCreateRequest) -> Cardholder:
        """
        Create a new cardholder.
        
        Args:
            cardholder: CardholderCreateRequest model with cardholder details
            
        Returns:
            Cardholder: The created cardholder
        """
        url = f"{self.base_path}/create"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url, json=cardholder.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use create_cardholder_async for async clients")
    
    async def create_cardholder_async(self, cardholder: CardholderCreateRequest) -> Cardholder:
        """
        Create a new cardholder asynchronously.
        
        Args:
            cardholder: CardholderCreateRequest model with cardholder details
            
        Returns:
            Cardholder: The created cardholder
        """
        url = f"{self.base_path}/create"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url, json=cardholder.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use create_cardholder for sync clients")
    
    def list_with_filters(
        self,
        cardholder_status: Optional[str] = None,
        page_num: int = 0,
        page_size: int = 10
    ) -> List[Cardholder]:
        """
        List cardholders with filtering options.
        
        Args:
            cardholder_status: Filter by status (PENDING, READY, INCOMPLETE, DISABLED)
            page_num: Page number, starts from 0
            page_size: Number of results per page
            
        Returns:
            List[Cardholder]: List of matching cardholders
        """
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if cardholder_status:
            params["cardholder_status"] = cardholder_status
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", self._build_url(), params=params)
            data = response.json()
            return [self.model_class.from_api_response(item) for item in data.get("items", [])]
        else:
            raise ValueError("Use list_with_filters_async for async clients")
    
    async def list_with_filters_async(
        self,
        cardholder_status: Optional[str] = None,
        page_num: int = 0,
        page_size: int = 10
    ) -> List[Cardholder]:
        """
        List cardholders with filtering options asynchronously.
        
        Args:
            cardholder_status: Filter by status (PENDING, READY, INCOMPLETE, DISABLED)
            page_num: Page number, starts from 0
            page_size: Number of results per page
            
        Returns:
            List[Cardholder]: List of matching cardholders
        """
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if cardholder_status:
            params["cardholder_status"] = cardholder_status
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", self._build_url(), params=params)
            data = response.json()
            return [self.model_class.from_api_response(item) for item in data.get("items", [])]
        else:
            raise ValueError("Use list_with_filters for sync clients")
    
    def update_cardholder(self, cardholder_id: str, update_data: CardholderUpdateRequest) -> Cardholder:
        """
        Update a cardholder.
        
        Args:
            cardholder_id: The ID of the cardholder to update
            update_data: CardholderUpdateRequest model with update details
            
        Returns:
            Cardholder: The updated cardholder
        """
        url = f"{self._build_url(cardholder_id)}/update"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url, json=update_data.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use update_cardholder_async for async clients")
    
    async def update_cardholder_async(self, cardholder_id: str, update_data: CardholderUpdateRequest) -> Cardholder:
        """
        Update a cardholder asynchronously.
        
        Args:
            cardholder_id: The ID of the cardholder to update
            update_data: CardholderUpdateRequest model with update details
            
        Returns:
            Cardholder: The updated cardholder
        """
        url = f"{self._build_url(cardholder_id)}/update"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url, json=update_data.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use update_cardholder for sync clients")
    
    def paginate(self, **params: Any) -> List[Cardholder]:
        """
        Fetch all pages of cardholders.
        
        Args:
            **params: Filter parameters to pass to the API
            
        Returns:
            List[Cardholder]: All cardholders matching the filters
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
    
    async def paginate_async(self, **params: Any) -> List[Cardholder]:
        """
        Fetch all pages of cardholders asynchronously.
        
        Args:
            **params: Filter parameters to pass to the API
            
        Returns:
            List[Cardholder]: All cardholders matching the filters
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
