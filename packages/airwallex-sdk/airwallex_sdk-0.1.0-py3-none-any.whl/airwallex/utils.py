"""
Utility functions for the Airwallex SDK.
"""
import re
from datetime import datetime
from typing import Any, Dict, List, Union, TypeVar

T = TypeVar('T')


def snake_to_pascal_case(snake_str: str) -> str:
    """Convert snake_case to PascalCase."""
    return ''.join(word.title() for word in snake_str.split('_'))


def pascal_to_snake_case(pascal_str: str) -> str:
    """Convert PascalCase to snake_case."""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', pascal_str).lower()


def camel_to_snake_case(camel_str: str) -> str:
    """Convert camelCase to snake_case."""
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', camel_str).lower()


def snake_to_camel_case(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def serialize(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Serialize data for the Airwallex API.
    Converts keys from snake_case to camelCase as required by the API.
    Handles datetime objects, converting them to ISO format strings.
    """
    if isinstance(data, list):
        return [serialize(item) for item in data]
    
    if not isinstance(data, dict):
        if isinstance(data, datetime):
            return data.isoformat()
        return data
    
    result: Dict[str, Any] = {}
    for key, value in data.items():
        # Convert snake_case keys to camelCase
        camel_key = snake_to_camel_case(key)
        
        # Handle nested dictionaries and lists
        if isinstance(value, dict):
            result[camel_key] = serialize(value)
        elif isinstance(value, list):
            result[camel_key] = [serialize(item) for item in value]
        elif isinstance(value, datetime):
            # Convert datetime objects to ISO format strings
            result[camel_key] = value.isoformat()
        else:
            result[camel_key] = value
            
    return result


def deserialize(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Deserialize data from the Airwallex API.
    Converts keys from camelCase to snake_case for Python convention.
    Attempts to parse ISO format date strings to datetime objects.
    """
    if isinstance(data, list):
        return [deserialize(item) for item in data]
    
    if not isinstance(data, dict):
        # Try to parse ISO date strings
        if isinstance(data, str):
            try:
                if 'T' in data and ('+' in data or 'Z' in data):
                    return datetime.fromisoformat(data.replace('Z', '+00:00'))
            except ValueError:
                pass
        return data
    
    result: Dict[str, Any] = {}
    for key, value in data.items():
        # Convert camelCase keys to snake_case
        snake_key = camel_to_snake_case(key)
        
        # Handle nested dictionaries and lists
        if isinstance(value, dict):
            result[snake_key] = deserialize(value)
        elif isinstance(value, list):
            result[snake_key] = [deserialize(item) for item in value]
        elif isinstance(value, str):
            # Try to parse ISO date strings
            try:
                if 'T' in value and ('+' in value or 'Z' in value):
                    result[snake_key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                else:
                    result[snake_key] = value
            except ValueError:
                result[snake_key] = value
        else:
            result[snake_key] = value
            
    return result
