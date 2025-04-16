"""
Client for interacting with the Airwallex API.
"""
import asyncio
import logging
import time
import httpx
import json
from datetime import datetime, timedelta, timezone, date
from typing import Any, Dict, List, Optional, Union, Type, TypeVar, cast
from importlib import import_module

from .utils import snake_to_pascal_case
from .exceptions import create_exception_from_response, AuthenticationError

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = 'https://api.airwallex.com/'
DEFAULT_AUTH_URL = 'https://api.airwallex.com/api/v1/authentication/login'

T = TypeVar("T")


class AirwallexClient:
    """
    Client for interacting with the Airwallex API.
    
    This client handles authentication, rate limiting, and provides
    access to all API endpoints through dynamic attribute access.
    """
    def __init__(
        self,
        *,
        client_id: str,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        auth_url: str = DEFAULT_AUTH_URL,
        request_timeout: int = 60,
        on_behalf_of: Optional[str] = None
    ):
        if not client_id or not api_key:
            raise ValueError("Client ID and API key are required")

        self.client_id = client_id
        self.api_key = api_key
        self.base_url = base_url
        self.auth_url = auth_url
        self.request_timeout = request_timeout
        self.on_behalf_of = on_behalf_of
        
        # Authentication state
        self._token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None
        
        # Create persistent httpx client
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.request_timeout,
        )
        
        # Cache for API instances
        self._api_instances: Dict[str, Any] = {}
    
    @property
    def headers(self) -> Dict[str, str]:
        """Default headers to use for all requests."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        # Add authentication token if available
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        
        # Add on-behalf-of header if specified
        if self.on_behalf_of:
            headers["x-on-behalf-of"] = self.on_behalf_of
            
        return headers
    
    @staticmethod
    def _prepare_params(params: Dict[str, Any]) -> Dict[str, str]:
        """Convert parameters to string format for URL encoding.
        
        datetime objects are formatted as ISO8601 strings.
        Lists are joined by commas.
        All other types are converted to strings.
        
        Args:
            params (Dict[str, Any]): _description_

        Returns:
            Dict[str, str]: _description_
        """
        prepared_params = {}
        for key, value in params.items():
            if isinstance(value, (date, datetime)):
                prepared_params[key] = value.isoformat()
            elif isinstance(value, list):
                prepared_params[key] = ",".join(map(str, value))
            else:
                prepared_params[key] = str(value)
        return prepared_params
    
    def _prepare_request(self, **kwargs) -> Dict[str, Any]:
        """Merge default headers and allow caller overrides."""
        headers = kwargs.pop('headers', {})
        params = kwargs.pop('params', {})
        kwargs['headers'] = {**self.headers, **headers}
        kwargs['params'] = self._prepare_params(params)
        return kwargs
    
    def authenticate(self) -> None:
        """
        Authenticate with the Airwallex API and get an access token.
        
        Airwallex auth requires sending the API key and client ID in headers
        and returns a token valid for 30 minutes.
        """
        # Return early if we already have a valid token
        if self._token and self._token_expiry and datetime.now(timezone.utc) < self._token_expiry:
            return
        
        # Use a separate client for authentication to avoid base_url issues
        auth_client = httpx.Client(timeout=self.request_timeout)
        try:
            # Airwallex requires x-client-id and x-api-key in the headers, not in the body
            response = auth_client.post(
                self.auth_url,
                headers={
                    "Content-Type": "application/json",
                    "x-client-id": self.client_id,
                    "x-api-key": self.api_key
                }
            )
            
            if response.status_code != 201:  # Airwallex returns 201 for successful auth
                raise AuthenticationError(
                    status_code=response.status_code,
                    response=response,
                    method="POST",
                    url=self.auth_url,
                    kwargs={"headers": {"x-client-id": self.client_id, "x-api-key": "**redacted**"}},
                    message="Authentication failed"
                )
                
            auth_data = response.json()
            self._token = auth_data.get("token")
            
            # Set token expiry based on expires_at if provided, or default to 30 minutes
            if "expires_at" in auth_data:
                # Parse ISO8601 format date
                self._token_expiry = datetime.fromisoformat(auth_data["expires_at"].replace("Z", "+00:00"))
            else:
                # Default to 30 minutes if no expires_at provided
                self._token_expiry = datetime.now(timezone.utc) + timedelta(minutes=30)
            
            logger.debug("Successfully authenticated with Airwallex API")
                
        finally:
            auth_client.close()
    
    def _request(self, method: str, url: str, **kwargs) -> Optional[httpx.Response]:
        """
        Make a synchronous HTTP request with automatic authentication.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            url: API endpoint URL (relative to base_url)
            **kwargs: Additional arguments to pass to httpx.request()
            
        Returns:
            httpx.Response: The HTTP response
            
        Raises:
            AirwallexAPIError: For API errors
        """
        # Ensure we're authenticated before making a request
        self.authenticate()
        
        retries = 5
        kwargs = self._prepare_request(**kwargs)
        
        while retries > 0:
            response = self._client.request(method, url, **kwargs)
            
            # Handle successful responses
            if 200 <= response.status_code < 300:
                return response
                
            # Handle authentication errors
            if response.status_code == 401:
                # Token might be expired, force refresh and retry
                self._token = None
                self._token_expiry = None
                self.authenticate()
                kwargs['headers'].update({"Authorization": f"Bearer {self._token}"})
                retries -= 1
                continue
                
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After')
                if retry_after and retry_after.isdigit():
                    wait_time = int(retry_after)
                    logger.info(f"Rate limited, sleeping for {wait_time} seconds")
                    time.sleep(wait_time)
                    continue
                else:
                    # Default backoff: 1 second
                    time.sleep(1)
                    continue
            
            # Retry on server errors (HTTP 5xx)
            if response.status_code >= 500 and retries > 0:
                retries -= 1
                logger.warning(f"Server error ({response.status_code}), retrying {retries} more time(s)...")
                time.sleep(1)
                continue
                
            # Create and raise the appropriate exception based on the response
            raise create_exception_from_response(
                response=response,
                method=method,
                url=url,
                kwargs=kwargs
            )
                
    def __getattr__(self, item: str) -> Any:
        """
        Dynamically load an API wrapper from the `api` subpackage.
        For example, accessing `client.account` will load the Account API wrapper.
        """
        # Check cache first
        if item in self._api_instances:
            return self._api_instances[item]
            
        try:
            base_package = self.__class__.__module__.split(".")[0]
            module = import_module(f"{base_package}.api.{item.lower()}")
            # Expect the API class to have the same name but capitalized.
            api_class = getattr(module, snake_to_pascal_case(item))
            api_instance = api_class(client=self)
            
            # Cache the instance
            self._api_instances[item] = api_instance
            return api_instance
        except (ModuleNotFoundError, AttributeError) as e:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'") from e

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()
        
    def __enter__(self) -> "AirwallexClient":
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


class AirwallexAsyncClient(AirwallexClient):
    """
    Asynchronous client for interacting with the Airwallex API.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Replace the HTTP client with an async one
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.request_timeout,
        )
    
    async def authenticate(self) -> None:
        """
        Authenticate with the Airwallex API and get an access token.
        
        Airwallex auth requires sending the API key and client ID in headers
        and returns a token valid for 30 minutes.
        """
        # Return early if we already have a valid token
        if self._token and self._token_expiry and datetime.now() < self._token_expiry:
            return
        
        # Use a separate client for authentication to avoid base_url issues
        async with httpx.AsyncClient(timeout=self.request_timeout) as auth_client:
            # Airwallex requires x-client-id and x-api-key in the headers, not in the body
            response = await auth_client.post(
                self.auth_url,
                headers={
                    "Content-Type": "application/json",
                    "x-client-id": self.client_id,
                    "x-api-key": self.api_key
                }
            )
            
            if response.status_code != 201:  # Airwallex returns 201 for successful auth
                raise AuthenticationError(
                    status_code=response.status_code,
                    response=response,
                    method="POST",
                    url=self.auth_url,
                    kwargs={"headers": {"x-client-id": self.client_id, "x-api-key": "**redacted**"}},
                    message="Authentication failed"
                )
                
            auth_data = response.json()
            self._token = auth_data.get("token")
            
            # Set token expiry based on expires_at if provided, or default to 30 minutes
            if "expires_at" in auth_data:
                # Parse ISO8601 format date
                self._token_expiry = datetime.fromisoformat(auth_data["expires_at"].replace("Z", "+00:00"))
            else:
                # Default to 30 minutes if no expires_at provided
                self._token_expiry = datetime.now() + timedelta(minutes=30)
            
            logger.debug("Successfully authenticated with Airwallex API")
    
    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """
        Make an asynchronous HTTP request with automatic authentication.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            url: API endpoint URL (relative to base_url)
            **kwargs: Additional arguments to pass to httpx.request()
            
        Returns:
            httpx.Response: The HTTP response
            
        Raises:
            AirwallexAPIError: For API errors
        """
        # Ensure we're authenticated before making a request
        await self.authenticate()
        
        retries = 5
        kwargs = self._prepare_request(**kwargs)
        
        while retries > 0:
            response = await self._client.request(method, url, **kwargs)
            
            # Handle successful responses
            if 200 <= response.status_code < 300:
                return response
                
            # Handle authentication errors
            if response.status_code == 401:
                # Token might be expired, force refresh and retry
                self._token = None
                self._token_expiry = None
                await self.authenticate()
                kwargs['headers'].update({"Authorization": f"Bearer {self._token}"})
                retries -= 1
                continue
                
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = response.headers.get('Retry-After')
                if retry_after and retry_after.isdigit():
                    wait_time = int(retry_after)
                    logger.info(f"Rate limited, sleeping for {wait_time} seconds")
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    # Default backoff: 1 second
                    await asyncio.sleep(1)
                    continue
            
            # Retry on server errors (HTTP 5xx)
            if response.status_code >= 500 and retries > 0:
                retries -= 1
                logger.warning(f"Server error ({response.status_code}), retrying {retries} more time(s)...")
                await asyncio.sleep(1)
                continue
                
            # Create and raise the appropriate exception based on the response
            raise create_exception_from_response(
                response=response,
                method=method,
                url=url,
                kwargs=kwargs
            )
    
    async def close(self) -> None:
        """Close the async HTTP client."""
        await self._client.aclose()
        
    async def __aenter__(self) -> "AirwallexAsyncClient":
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
