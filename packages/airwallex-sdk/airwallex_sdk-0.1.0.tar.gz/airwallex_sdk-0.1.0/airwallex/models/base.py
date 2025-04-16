"""
Base Pydantic models for the Airwallex API.
"""
from typing import Any, Dict, List, Optional, ClassVar, Type, TypeVar, Generic, get_origin, get_args
from datetime import datetime
import re
from pydantic import BaseModel, Field, ConfigDict, model_validator
from ..utils import snake_to_camel_case, camel_to_snake_case

T = TypeVar('T', bound='AirwallexModel')


class AirwallexModel(BaseModel):
    """Base model for all Airwallex API models with camelCase conversion."""
    
    model_config = ConfigDict(
        populate_by_name=True,
        extra='ignore',
        arbitrary_types_allowed=True
    )
    
    # Class variable to store the API resource name
    resource_name: ClassVar[str] = ""
    
    @model_validator(mode='before')
    @classmethod
    def _convert_keys_to_snake_case(cls, data: Any) -> Any:
        """Convert camelCase keys to snake_case."""
        if not isinstance(data, dict):
            return data
            
        result = {}
        for key, value in data.items():
            # Convert camelCase keys to snake_case
            snake_key = camel_to_snake_case(key)
            
            # Handle nested dictionaries and lists
            if isinstance(value, dict):
                result[snake_key] = cls._convert_keys_to_snake_case(value)
            elif isinstance(value, list) and all(isinstance(item, dict) for item in value):
                result[snake_key] = [cls._convert_keys_to_snake_case(item) for item in value]
            else:
                result[snake_key] = value
                
        return result
        
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary with camelCase keys for API requests."""
        data = self.model_dump(exclude_unset=True)
        result: Dict[str, Any] = {}
        
        for key, value in data.items():
            # Convert snake_case keys to camelCase
            camel_key = snake_to_camel_case(key)
            
            # Handle nested models, dictionaries, and lists
            if isinstance(value, AirwallexModel):
                result[camel_key] = value.to_api_dict()
            elif isinstance(value, dict):
                # Convert dict keys to camelCase
                nested_dict = {}
                for k, v in value.items():
                    if isinstance(v, AirwallexModel):
                        nested_dict[snake_to_camel_case(k)] = v.to_api_dict()
                    elif isinstance(v, list) and all(isinstance(item, AirwallexModel) for item in v):
                        nested_dict[snake_to_camel_case(k)] = [item.to_api_dict() for item in v]
                    else:
                        nested_dict[snake_to_camel_case(k)] = v
                result[camel_key] = nested_dict
            elif isinstance(value, list):
                # Handle lists of models
                if all(isinstance(item, AirwallexModel) for item in value):
                    result[camel_key] = [item.to_api_dict() for item in value]
                else:
                    result[camel_key] = value
            elif isinstance(value, datetime):
                # Convert datetime to ISO format
                result[camel_key] = value.isoformat()
            else:
                result[camel_key] = value
                
        return result
        
    @classmethod
    def from_api_response(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create a model instance from API response data."""
        return cls.model_validate(cls._convert_keys_to_snake_case(data))


# Common types used across the SDK
class PaginationParams(AirwallexModel):
    """Common pagination parameters."""
    page: Optional[int] = Field(None, description="Page number (1-indexed)")
    page_size: Optional[int] = Field(None, description="Number of items per page")


class PaginatedResponse(AirwallexModel, Generic[T]):
    """Base model for paginated responses."""
    items: List[T] = Field(..., description="List of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_count: int = Field(..., description="Total number of items")
    total_pages: int = Field(..., description="Total number of pages")
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any], item_class: Type[T]) -> 'PaginatedResponse[T]':
        """Create a paginated response with the correct item type."""
        # Extract the items and convert them to the specified model
        items_data = data.get("items", [])
        items = [item_class.from_api_response(item) for item in items_data]
        
        # Create the paginated response with the converted items
        paginated_data = {
            "items": items,
            "page": data.get("page", 1),
            "page_size": data.get("pageSize", len(items)),
            "total_count": data.get("totalCount", len(items)),
            "total_pages": data.get("totalPages", 1)
        }
        
        return cls.model_validate(paginated_data)
