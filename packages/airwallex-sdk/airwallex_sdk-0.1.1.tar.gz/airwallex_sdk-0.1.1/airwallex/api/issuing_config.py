"""
Airwallex Issuing Config API.
"""
from typing import Dict, Any, List, Optional, Type, TypeVar, Union, cast
from ..models.issuing_config import IssuingConfig, IssuingConfigUpdateRequest
from .base import AirwallexAPIBase

T = TypeVar("T", bound=IssuingConfig)


class IssuingConfig(AirwallexAPIBase[IssuingConfig]):
    """
    Operations for Airwallex issuing configuration.
    
    Configuration for issuance settings and controls.
    """
    endpoint = "issuing/config"
    model_class = cast(Type[IssuingConfig], IssuingConfig)
    
    def get_config(self) -> IssuingConfig:
        """
        Get the current issuing configuration.
        
        Returns:
            IssuingConfig: The current issuing configuration
        """
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", self._build_url())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use get_config_async for async clients")
    
    async def get_config_async(self) -> IssuingConfig:
        """
        Get the current issuing configuration asynchronously.
        
        Returns:
            IssuingConfig: The current issuing configuration
        """
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", self._build_url())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use get_config for sync clients")
    
    def update_config(self, update_data: IssuingConfigUpdateRequest) -> IssuingConfig:
        """
        Update the issuing configuration.
        
        Args:
            update_data: IssuingConfigUpdateRequest model with update details
            
        Returns:
            IssuingConfig: The updated issuing configuration
        """
        url = f"{self._build_url()}/update"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url, json=update_data.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use update_config_async for async clients")
    
    async def update_config_async(self, update_data: IssuingConfigUpdateRequest) -> IssuingConfig:
        """
        Update the issuing configuration asynchronously.
        
        Args:
            update_data: IssuingConfigUpdateRequest model with update details
            
        Returns:
            IssuingConfig: The updated issuing configuration
        """
        url = f"{self._build_url()}/update"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url, json=update_data.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use update_config for sync clients")
