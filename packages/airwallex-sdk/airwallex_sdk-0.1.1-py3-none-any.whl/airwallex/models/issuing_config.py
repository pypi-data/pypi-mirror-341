"""
Models for the Airwallex Issuing Config API.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import Field
from .base import AirwallexModel
from .issuing_common import TransactionUsage


class RemoteAuthSettings(AirwallexModel):
    """Model for remote auth settings."""
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    default_action: Optional[str] = Field(None, description="Default action when remote auth fails")
    enabled: Optional[bool] = Field(None, description="Whether remote auth is enabled")
    shared_secret: Optional[str] = Field(None, description="Shared secret key")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    url: Optional[str] = Field(None, description="Remote auth endpoint URL")


class RemoteCallMethod(AirwallexModel):
    """Model for remote call method."""
    name: str = Field(..., description="Method name")
    path: str = Field(..., description="Method path")


class RemoteCallConfig(AirwallexModel):
    """Model for remote call configuration."""
    methods: List[RemoteCallMethod] = Field(..., description="Available methods")
    shared_secret: Optional[str] = Field(None, description="Shared secret key")
    url: str = Field(..., description="Base URL")


class RemoteProvisioningConfig(AirwallexModel):
    """Model for remote provisioning configuration."""
    activated: Optional[bool] = Field(None, description="Whether remote provisioning is activated")
    shared_secret: Optional[str] = Field(None, description="Shared secret key")
    url: Optional[str] = Field(None, description="Remote provisioning endpoint URL")


class SpendingLimitSettings(AirwallexModel):
    """Model for spending limit settings."""
    default_limits: Optional[Dict[str, Dict[str, float]]] = Field(None, description="Default limits")
    maximum_limits: Optional[Dict[str, Dict[str, float]]] = Field(None, description="Maximum limits")


class IssuingConfig(AirwallexModel):
    """Model for issuing configuration."""
    resource_name: str = "issuing/config"
    
    blocked_transaction_usages: Optional[List[TransactionUsage]] = Field(None, description="Blocked transaction usages")
    remote_auth_settings: Optional[RemoteAuthSettings] = Field(None, description="Remote authorization settings")
    remote_call_config: Optional[RemoteCallConfig] = Field(None, description="Remote call configuration")
    remote_provisioning_config: Optional[RemoteProvisioningConfig] = Field(None, description="Remote provisioning configuration")
    spending_limit_settings: Optional[SpendingLimitSettings] = Field(None, description="Spending limit settings")


class IssuingConfigUpdateRequest(AirwallexModel):
    """Model for issuing config update request."""
    remote_auth: Optional[RemoteAuthSettings] = Field(None, description="Remote authorization configuration")
    remote_call_config: Optional[RemoteCallConfig] = Field(None, description="Remote call configuration")
    remote_provisioning_config: Optional[RemoteProvisioningConfig] = Field(None, description="Remote provisioning configuration")
