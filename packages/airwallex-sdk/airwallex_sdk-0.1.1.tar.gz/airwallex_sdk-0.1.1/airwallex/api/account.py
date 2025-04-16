"""
Airwallex Account API.
"""
from typing import Dict, Any, List, Optional, Type, TypeVar, cast
from ..models.account import Account, AccountCreateRequest, AccountUpdateRequest
from .base import AirwallexAPIBase

T = TypeVar("T", bound=Account)


class Account(AirwallexAPIBase[Account]):
    """
    Operations for Airwallex accounts.
    
    Accounts represent the global accounts that can hold balances 
    in multiple currencies.
    """
    endpoint = "accounts"
    model_class = cast(Type[Account], Account)
    
    def fetch_balance(self, account_id: str) -> Account:
        """
        Fetch the balance for a specific account.
        
        Args:
            account_id: The ID of the account to fetch the balance for.
            
        Returns:
            Account: Account with balance information.
        """
        url = self._build_url(account_id, "balance")
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", url)
            data = response.json()
            account_data = {"id": account_id, "balance": data}
            return self.model_class.from_api_response(account_data)
        else:
            raise ValueError("Use fetch_balance_async for async clients")
            
    async def fetch_balance_async(self, account_id: str) -> Account:
        """
        Fetch the balance for a specific account asynchronously.
        
        Args:
            account_id: The ID of the account to fetch the balance for.
            
        Returns:
            Account: Account with balance information.
        """
        url = self._build_url(account_id, "balance")
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", url)
            data = response.json()
            account_data = {"id": account_id, "balance": data}
            return self.model_class.from_api_response(account_data)
        else:
            raise ValueError("Use fetch_balance for sync clients")
    
    def create_from_model(self, account: AccountCreateRequest) -> Account:
        """
        Create a new account using a Pydantic model.
        
        Args:
            account: AccountCreateRequest model with account creation details.
            
        Returns:
            Account: The newly created account.
        """
        return self.create(account)
    
    async def create_from_model_async(self, account: AccountCreateRequest) -> Account:
        """
        Create a new account using a Pydantic model asynchronously.
        
        Args:
            account: AccountCreateRequest model with account creation details.
            
        Returns:
            Account: The newly created account.
        """
        return await self.create_async(account)
    
    def update_from_model(self, account_id: str, account: AccountUpdateRequest) -> Account:
        """
        Update an account using a Pydantic model.
        
        Args:
            account_id: The ID of the account to update.
            account: AccountUpdateRequest model with account update details.
            
        Returns:
            Account: The updated account.
        """
        return self.update(account_id, account)
    
    async def update_from_model_async(self, account_id: str, account: AccountUpdateRequest) -> Account:
        """
        Update an account using a Pydantic model asynchronously.
        
        Args:
            account_id: The ID of the account to update.
            account: AccountUpdateRequest model with account update details.
            
        Returns:
            Account: The updated account.
        """
        return await self.update_async(account_id, account)
