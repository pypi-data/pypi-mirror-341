"""
Exceptions for the Airwallex API client.
"""
from typing import Any, Dict, Optional, Type, ClassVar, Mapping
import httpx


class AirwallexAPIError(Exception):
    """Base exception for Airwallex API errors."""
    
    def __init__(
        self,
        *,
        status_code: int,
        response: httpx.Response,
        method: str,
        url: str,
        kwargs: Dict[str, Any],
        message: Optional[str] = None
    ):
        self.status_code = status_code
        self.response = response
        self.method = method
        self.url = url
        self.kwargs = kwargs
        
        # Try to parse error details from the response
        try:
            error_data = response.json()
            self.error_code = error_data.get("code", "unknown")
            self.error_message = error_data.get("message", "Unknown error")
            self.error_source = error_data.get("source", None)
            self.request_id = error_data.get("request_id", None)
        except Exception:
            self.error_code = "unknown"
            self.error_message = message or f"HTTP {status_code} error"
            self.error_source = None
            self.request_id = None
            
        super().__init__(self.__str__())
        
    def __str__(self) -> str:
        source_info = f" (source: {self.error_source})" if self.error_source else ""
        return (
            f"Airwallex API Error (HTTP {self.status_code}): [{self.error_code}] {self.error_message}{source_info} "
            f"for {self.method} {self.url}"
        )


class AuthenticationError(AirwallexAPIError):
    """Raised when there's an authentication issue."""
    pass


class RateLimitError(AirwallexAPIError):
    """Raised when the API rate limit has been exceeded."""
    pass


class ResourceNotFoundError(AirwallexAPIError):
    """Raised when a requested resource is not found."""
    pass


class ValidationError(AirwallexAPIError):
    """Raised when the request data is invalid."""
    pass


class ServerError(AirwallexAPIError):
    """Raised when the server returns a 5xx error."""
    pass


class ResourceExistsError(ValidationError):
    """Raised when trying to create a resource that already exists."""
    pass


class AmountLimitError(ValidationError):
    """Raised when a transaction amount exceeds or falls below the allowed limits."""
    pass


class EditForbiddenError(ValidationError):
    """Raised when trying to edit a resource that can't be modified."""
    pass


class CurrencyError(ValidationError):
    """Raised for currency-related errors like invalid pairs or unsupported currencies."""
    pass


class DateError(ValidationError):
    """Raised for date-related validation errors."""
    pass


class TransferMethodError(ValidationError):
    """Raised when the transfer method is not supported."""
    pass


class ConversionError(AirwallexAPIError):
    """Raised for conversion-related errors."""
    pass


class ServiceUnavailableError(ServerError):
    """Raised when a service is temporarily unavailable."""
    pass


# Mapping of error codes to exception classes
ERROR_CODE_MAP: Dict[str, Type[AirwallexAPIError]] = {
    # Authentication errors
    "credentials_expired": AuthenticationError,
    "credentials_invalid": AuthenticationError,
    
    # Rate limiting
    "too_many_requests": RateLimitError,
    
    # Resource exists
    "already_exists": ResourceExistsError,
    
    # Amount limit errors
    "amount_above_limit": AmountLimitError,
    "amount_below_limit": AmountLimitError,
    "amount_above_transfer_method_limit": AmountLimitError,
    
    # Edit forbidden
    "can_not_be_edited": EditForbiddenError,
    
    # Conversion errors
    "conversion_create_failed": ConversionError,
    
    # Validation errors
    "field_required": ValidationError,
    "invalid_argument": ValidationError,
    "term_agreement_is_required": ValidationError,
    
    # Currency errors
    "invalid_currency_pair": CurrencyError,
    "unsupported_currency": CurrencyError,
    
    # Date errors
    "invalid_transfer_date": DateError,
    "invalid_conversion_date": DateError,
    
    # Transfer method errors
    "unsupported_country_code": TransferMethodError,
    "unsupported_transfer_method": TransferMethodError,
    
    # Service unavailable
    "service_unavailable": ServiceUnavailableError,
}


def create_exception_from_response(
    *,
    response: httpx.Response,
    method: str,
    url: str,
    kwargs: Dict[str, Any],
    message: Optional[str] = None
) -> AirwallexAPIError:
    """
    Create the appropriate exception based on the API response.
    
    This function first checks for specific error codes in the response body.
    If no specific error code is found or it's not recognized, it falls back
    to using the HTTP status code to determine the exception type.
    
    Args:
        response: The HTTP response
        method: HTTP method used for the request
        url: URL of the request
        kwargs: Additional keyword arguments passed to the request
        message: Optional custom error message
        
    Returns:
        An instance of the appropriate AirwallexAPIError subclass
    """
    status_code = response.status_code
    
    try:
        error_data = response.json()
        error_code = error_data.get("code")
        
        if error_code and error_code in ERROR_CODE_MAP:
            exception_class = ERROR_CODE_MAP[error_code]
        else:
            # Fall back to status code-based exception
            exception_class = exception_for_status(status_code)
    except Exception:
        # If we can't parse the response JSON, fall back to status code
        exception_class = exception_for_status(status_code)
    
    return exception_class(
        status_code=status_code,
        response=response,
        method=method,
        url=url,
        kwargs=kwargs,
        message=message
    )


def exception_for_status(status_code: int) -> Type[AirwallexAPIError]:
    """Return the appropriate exception class for a given HTTP status code."""
    if status_code == 401:
        return AuthenticationError
    elif status_code == 429:
        return RateLimitError
    elif status_code == 404:
        return ResourceNotFoundError
    elif 400 <= status_code < 500:
        return ValidationError
    elif 500 <= status_code < 600:
        return ServerError
    return AirwallexAPIError  # Default to the base exception for other status codes
