"""
Base API class for the Airwallex SDK.
"""
import asyncio
import logging
from typing import (
    Any, 
    Dict, 
    List, 
    Optional, 
    Type, 
    TypeVar, 
    Union, 
    Coroutine, 
    Generator, 
    AsyncGenerator,
    Generic,
    cast,
    get_args,
    get_origin
)
import httpx

from ..models.base import AirwallexModel, PaginatedResponse
from ..utils import snake_to_pascal_case, serialize, deserialize
from ..exceptions import (
    AirwallexAPIError, 
    AuthenticationError, 
    RateLimitError, 
    ResourceNotFoundError, 
    ValidationError, 
    ServerError
)

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=AirwallexModel)
ClientType = TypeVar("ClientType")

class AirwallexAPIBase(Generic[T]):
    """
    Base class for Airwallex API endpoints.
    
    This class provides standard CRUD methods and pagination handling
    for all API endpoints. It serves as the foundation for specific 
    API endpoint implementations.
    """
    endpoint: str = ""
    model_class: Type[T] = cast(Type[T], AirwallexModel)  # Will be overridden by subclasses
    
    def __init__(
        self,
        *,
        client: Any,
        data: Optional[Dict[str, Any]] = None,
        parent: Optional["AirwallexAPIBase"] = None,
        parent_path: Optional[str] = None  # e.g. "/api/v1/accounts/{account_id}"
    ) -> None:
        self.client = client
        self.data: Dict[str, Any] = data or {}
        self.parent: Optional["AirwallexAPIBase"] = parent
        self.parent_path: Optional[str] = parent_path
    
    def __getattr__(self, item: str) -> Any:
        # If the attribute exists in the model's data, return it.
        if item in self.data:
            return self.data[item]

        # If the model has an ID, we can try to access a subresource
        if not getattr(self, 'id', None):
            raise AttributeError(f"No such attribute '{item}' in {self.__class__.__name__} context.")
            
        # Try to load an API module for this attribute.
        try:
            from importlib import import_module
            base_package = self.client.__class__.__module__.split(".")[0]
            module = import_module(f"{base_package}.api.{item.lower()}")
            # We define modules in pascal case, but refer to them as attributes in snake case.
            api_class = getattr(module, snake_to_pascal_case(item))
            return api_class(client=self.client, parent=self, parent_path=self._build_url(self.id))
        except (ModuleNotFoundError, AttributeError):
            # Split snake case item into a path e.g. report_details -> report/details
            path_item = "/".join(item.split("_"))
            
            # If no module exists for this attribute and model has an id, then assume the attribute
            # is a valid endpoint suffix. Return a callable that makes a GET request.
            def dynamic_endpoint(*args, **kwargs):
                """
                :param dataframe: If True, return a DataFrame instead of a list of dictionaries.
                """
                url = self._build_url(resource_id=self.id, suffix=path_item)
                if not self.client.__class__.__name__.startswith('Async'):
                    response = self.client._request("GET", url, params=kwargs)
                    data = self._parse_response_data(response.json())
                    return data
                else:
                    async def async_endpoint():
                        response = await self.client._request("GET", url, params=kwargs)
                        data = self._parse_response_data(response.json())
                        return data
                    return async_endpoint()
            return dynamic_endpoint

    def __repr__(self) -> str:
        identifier = self.data.get("id", "unknown")
        return f"<{self.__class__.__name__} id={identifier}>"
    
    def __call__(self, resource_id: Optional[Any] = None, **kwargs: Any) -> Union[
        T,
        Generator[T, None, None],
        Coroutine[Any, Any, AsyncGenerator[T, None]]
    ]:
        """
        If a resource_id is provided, fetch and return a single instance;
        otherwise, return a generator that yields resources one by one.

        For sync clients, returns a Generator[T, None, None].
        For async clients, returns a coroutine that yields an AsyncGenerator[T, None].
        """
        if resource_id is not None:
            if not self.client.__class__.__name__.startswith('Async'):
                return self.fetch(resource_id)
            else:
                return self.fetch_async(resource_id)
        else:
            if not self.client.__class__.__name__.startswith('Async'):
                return self.paginate_generator(**kwargs)
            else:
                return self.paginate_async_generator(**kwargs)
    
    @classmethod
    def get_endpoint(cls) -> str:
        """Get the API endpoint path."""
        return cls.endpoint if cls.endpoint else cls.__name__.lower()
    
    @staticmethod
    def _parse_response_data(
        response: Union[List[Any], Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Parse response data into a list of dictionaries."""
        # If response is a dictionary with an 'items' key, it's paginated
        if isinstance(response, dict) and 'items' in response:
            return response['items']
        # If response is a dictionary, wrap it in a list
        if isinstance(response, dict):
            return [response]
        # If response is already a list, return it
        return response
    
    @property
    def base_path(self) -> str:
        """Get the base API path for this endpoint."""
        if self.parent_path:
            return f"{self.parent_path}/{self.get_endpoint()}"
        return f"/api/v1/{self.get_endpoint()}"
    
    def _build_url(self, resource_id: Optional[Any] = None, suffix: str = "") -> str:
        """Build a URL for a specific resource."""
        url = self.base_path
        if resource_id is not None:
            url = f"{url}/{resource_id}"
        if suffix:
            url = f"{url}/{suffix}"
        return url
    
    def show(self, indent: int = 0, indent_step: int = 2) -> str:
        """
        Return a nicely formatted string representation of this model and its data.
        """
        pad = " " * indent
        lines = [f"{pad}{self.__class__.__name__}:"]
        for key, value in self.data.items():
            if isinstance(value, AirwallexAPIBase):
                lines.append(f"{pad}{' ' * indent_step}{key}:")
                lines.append(value.show(indent + indent_step, indent_step))
            elif isinstance(value, list):
                lines.append(f"{pad}{' ' * indent_step}{key}: [")
                for item in value:
                    if isinstance(item, AirwallexAPIBase):
                        lines.append(item.show(indent + indent_step, indent_step))
                    else:
                        lines.append(f"{pad}{' ' * (indent_step * 2)}{item}")
                lines.append(f"{pad}{' ' * indent_step}]")
            else:
                lines.append(f"{pad}{' ' * indent_step}{key}: {value}")
        return "\n".join(lines)
    
    def to_model(self) -> T:
        """Convert the raw data to a Pydantic model."""
        if not self.data:
            raise ValueError("No data available to convert to a model")
        return self.model_class.from_api_response(self.data)
    
    # Synchronous API methods
    
    def fetch(self, resource_id: Any) -> T:
        """Fetch a single resource by ID."""
        if self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires a sync client.")
        url = self._build_url(resource_id)
        response = self.client._request("GET", url)
        data = self._parse_response_data(response.json())
        # If the returned data is a list, take the first item.
        if isinstance(data, list):
            data = data[0] if data else {}
        return self.model_class.from_api_response(data)
    
    def list(self, **params: Any) -> List[T]:
        """List resources with optional filtering parameters."""
        if self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires a sync client.")
        url = self._build_url()
        response = self.client._request("GET", url, params=serialize(params))
        data_list = self._parse_response_data(response.json())
        return [self.model_class.from_api_response(item) for item in data_list]
    
    def create(self, payload: Union[Dict[str, Any], T]) -> T:
        """Create a new resource."""
        if str(self.client.__class__.__name__).startswith('Async'):
            raise ValueError("This method requires a sync client.")
        
        # Convert Pydantic model to dict if needed
        if isinstance(payload, AirwallexModel):
            payload_dict = payload.to_api_dict()
        else:
            payload_dict = serialize(payload)
            
        url = self._build_url()
        response = self.client._request("POST", url, json=payload_dict)
        data = self._parse_response_data(response.json())
        # If the returned data is a list, take the first item.
        if isinstance(data, list):
            data = data[0] if data else {}
        return self.model_class.from_api_response(data)
    
    def update(self, resource_id: Any, payload: Union[Dict[str, Any], T]) -> T:
        """Update an existing resource."""
        if self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires a sync client.")
            
        # Convert Pydantic model to dict if needed
        if isinstance(payload, AirwallexModel):
            payload_dict = payload.to_api_dict()
        else:
            payload_dict = serialize(payload)
            
        url = self._build_url(resource_id)
        response = self.client._request("PUT", url, json=payload_dict)
        data = self._parse_response_data(response.json())
        # If the returned data is a list, take the first item.
        if isinstance(data, list):
            data = data[0] if data else {}
        return self.model_class.from_api_response(data)
    
    def delete(self, resource_id: Any) -> None:
        """Delete a resource."""
        if self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires a sync client.")
        url = self._build_url(resource_id)
        self.client._request("DELETE", url)
    
    def paginate(self, **params: Any) -> List[T]:
        """Fetch all pages of data."""
        if str(self.client.__class__.__name__).startswith('Async'):
            raise ValueError("This method requires a sync client.")
            
        all_items: List[Dict[str, Any]] = []
        page = params.get("page", 1)
        page_size = params.get("page_size", 100)
        
        while True:
            params["page"] = page
            params["page_size"] = page_size
            url = self._build_url()
            response = self.client._request("GET", url, params=serialize(params))
            response_data = response.json()
            
            # Check if response is paginated
            if isinstance(response_data, dict) and 'items' in response_data:
                items = response_data['items']
                total_pages = response_data.get('total_pages', 1)
                
                if not items:
                    break
                    
                all_items.extend(items)
                
                if page >= total_pages:
                    break
                    
                page += 1
            else:
                # Not paginated, just use the data as is
                page_data = self._parse_response_data(response_data)
                if not page_data:
                    break
                all_items.extend(page_data)
                break
                
        return [self.model_class.from_api_response(item) for item in all_items]
    
    def paginate_generator(self, **params: Any) -> Generator[T, None, None]:
        """Generate items one by one from paginated results."""
        if self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires a sync client.")
            
        page = params.get("page", 1)
        page_size = params.get("page_size", 100)
        
        while True:
            params["page"] = page
            params["page_size"] = page_size
            url = self._build_url()
            response = self.client._request("GET", url, params=serialize(params))
            response_data = response.json()
            
            # Check if response is paginated
            if isinstance(response_data, dict) and 'items' in response_data:
                items = response_data['items']
                total_pages = response_data.get('total_pages', 1)
                
                if not items:
                    break
                    
                for item in items:
                    yield self.model_class.from_api_response(item)
                
                if page >= total_pages:
                    break
                    
                page += 1
            else:
                # Not paginated, just use the data as is
                page_data = self._parse_response_data(response_data)
                if not page_data:
                    break
                    
                for item in page_data:
                    yield self.model_class.from_api_response(item)
                break
    
    # Asynchronous API methods
    
    async def fetch_async(self, resource_id: Any) -> T:
        """Fetch a single resource by ID asynchronously."""
        if not self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires an async client.")
        url = self._build_url(resource_id)
        response = await self.client._request("GET", url)
        data = self._parse_response_data(response.json())
        # If the returned data is a list, take the first item.
        if isinstance(data, list):
            data = data[0] if data else {}
        return self.model_class.from_api_response(data)
    
    async def list_async(self, **params: Any) -> List[T]:
        """List resources with optional filtering parameters asynchronously."""
        if not self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires an async client.")
        url = self._build_url()
        response = await self.client._request("GET", url, params=serialize(params))
        data_list = self._parse_response_data(response.json())
        return [self.model_class.from_api_response(item) for item in data_list]
    
    async def create_async(self, payload: Union[Dict[str, Any], T]) -> T:
        """Create a new resource asynchronously."""
        if not self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires an async client.")
            
        # Convert Pydantic model to dict if needed
        if isinstance(payload, AirwallexModel):
            payload_dict = payload.to_api_dict()
        else:
            payload_dict = serialize(payload)
            
        url = self._build_url()
        response = await self.client._request("POST", url, json=payload_dict)
        data = self._parse_response_data(response.json())
        # If the returned data is a list, take the first item.
        if isinstance(data, list):
            data = data[0] if data else {}
        return self.model_class.from_api_response(data)
    
    async def update_async(self, resource_id: Any, payload: Union[Dict[str, Any], T]) -> T:
        """Update an existing resource asynchronously."""
        if not self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires an async client.")
            
        # Convert Pydantic model to dict if needed
        if isinstance(payload, AirwallexModel):
            payload_dict = payload.to_api_dict()
        else:
            payload_dict = serialize(payload)
            
        url = self._build_url(resource_id)
        response = await self.client._request("PUT", url, json=payload_dict)
        data = self._parse_response_data(response.json())
        # If the returned data is a list, take the first item.
        if isinstance(data, list):
            data = data[0] if data else {}
        return self.model_class.from_api_response(data)
    
    async def delete_async(self, resource_id: Any) -> None:
        """Delete a resource asynchronously."""
        if not self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires an async client.")
        url = self._build_url(resource_id)
        await self.client._request("DELETE", url)
    
    async def paginate_async(self, **params: Any) -> List[T]:
        """Fetch all pages of data asynchronously."""
        if not self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires an async client.")
            
        all_items: List[Dict[str, Any]] = []
        page = params.get("page", 1)
        page_size = params.get("page_size", 100)
        
        while True:
            params["page"] = page
            params["page_size"] = page_size
            url = self._build_url()
            response = await self.client._request("GET", url, params=serialize(params))
            response_data = response.json()
            
            # Check if response is paginated
            if isinstance(response_data, dict) and 'items' in response_data:
                items = response_data['items']
                total_pages = response_data.get('total_pages', 1)
                
                if not items:
                    break
                    
                all_items.extend(items)
                
                if page >= total_pages:
                    break
                    
                page += 1
            else:
                # Not paginated, just use the data as is
                page_data = self._parse_response_data(response_data)
                if not page_data:
                    break
                all_items.extend(page_data)
                break
                
        return [self.model_class.from_api_response(item) for item in all_items]
    
    async def paginate_async_generator(self, **params: Any) -> AsyncGenerator[T, None]:
        """Generate items one by one from paginated results asynchronously."""
        if not self.client.__class__.__name__.startswith('Async'):
            raise ValueError("This method requires an async client.")
            
        page = params.get("page", 1)
        page_size = params.get("page_size", 100)
        
        while True:
            params["page"] = page
            params["page_size"] = page_size
            url = self._build_url()
            response = await self.client._request("GET", url, params=serialize(params))
            response_data = response.json()
            
            # Check if response is paginated
            if isinstance(response_data, dict) and 'items' in response_data:
                items = response_data['items']
                total_pages = response_data.get('total_pages', 1)
                
                if not items:
                    break
                    
                for item in items:
                    yield self.model_class.from_api_response(item)
                
                if page >= total_pages:
                    break
                    
                page += 1
            else:
                # Not paginated, just use the data as is
                page_data = self._parse_response_data(response_data)
                if not page_data:
                    break
                    
                for item in page_data:
                    yield self.model_class.from_api_response(item)
                break
