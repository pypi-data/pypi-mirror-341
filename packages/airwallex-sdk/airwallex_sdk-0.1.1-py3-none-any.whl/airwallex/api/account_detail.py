"""
Airwallex Account Detail API.
"""
from typing import Dict, Any, List, Optional, Type, TypeVar, Union, cast
from datetime import datetime
from ..models.account_detail import (
    AccountDetailModel, AccountCreateRequest, AccountUpdateRequest,
    Amendment, AmendmentCreateRequest, WalletInfo, TermsAndConditionsRequest
)
from .base import AirwallexAPIBase

T = TypeVar("T", bound=AccountDetailModel)


class AccountDetail(AirwallexAPIBase[AccountDetailModel]):
    """
    Operations for Airwallex account details.
    
    Account details represent the complete information about an Airwallex account,
    including business details, persons, and compliance information.
    """
    endpoint = "accounts"
    model_class = cast(Type[AccountDetailModel], AccountDetailModel)
    
    def get_my_account(self) -> AccountDetailModel:
        """
        Retrieve account details for your own Airwallex account.
        
        Returns:
            AccountDetailModel: Your account details.
        """
        url = "/api/v1/account"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", url)
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use get_my_account_async for async clients")
            
    async def get_my_account_async(self) -> AccountDetailModel:
        """
        Retrieve account details for your own Airwallex account asynchronously.
        
        Returns:
            AccountDetailModel: Your account details.
        """
        url = "/api/v1/account"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", url)
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use get_my_account for sync clients")
    
    def get_amendment(self, amendment_id: str) -> Amendment:
        """
        Get an account amendment.
        
        Args:
            amendment_id: The ID of the amendment to retrieve.
            
        Returns:
            Amendment: The amendment.
        """
        url = f"/api/v1/account/amendments/{amendment_id}"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", url)
            return Amendment.from_api_response(response.json())
        else:
            raise ValueError("Use get_amendment_async for async clients")
            
    async def get_amendment_async(self, amendment_id: str) -> Amendment:
        """
        Get an account amendment asynchronously.
        
        Args:
            amendment_id: The ID of the amendment to retrieve.
            
        Returns:
            Amendment: The amendment.
        """
        url = f"/api/v1/account/amendments/{amendment_id}"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", url)
            return Amendment.from_api_response(response.json())
        else:
            raise ValueError("Use get_amendment for sync clients")
    
    def create_amendment(self, amendment: AmendmentCreateRequest) -> Amendment:
        """
        Create an account amendment.
        
        Args:
            amendment: AmendmentCreateRequest model with amendment details.
            
        Returns:
            Amendment: The created amendment.
        """
        url = "/api/v1/account/amendments/create"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url, json=amendment.to_api_dict())
            return Amendment.from_api_response(response.json())
        else:
            raise ValueError("Use create_amendment_async for async clients")
            
    async def create_amendment_async(self, amendment: AmendmentCreateRequest) -> Amendment:
        """
        Create an account amendment asynchronously.
        
        Args:
            amendment: AmendmentCreateRequest model with amendment details.
            
        Returns:
            Amendment: The created amendment.
        """
        url = "/api/v1/account/amendments/create"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url, json=amendment.to_api_dict())
            return Amendment.from_api_response(response.json())
        else:
            raise ValueError("Use create_amendment for sync clients")
    
    def get_wallet_info(self) -> WalletInfo:
        """
        Retrieve account wallet information.
        
        Returns:
            WalletInfo: The wallet information.
        """
        url = "/api/v1/account/wallet_info"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", url)
            return WalletInfo.from_api_response(response.json())
        else:
            raise ValueError("Use get_wallet_info_async for async clients")
            
    async def get_wallet_info_async(self) -> WalletInfo:
        """
        Retrieve account wallet information asynchronously.
        
        Returns:
            WalletInfo: The wallet information.
        """
        url = "/api/v1/account/wallet_info"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", url)
            return WalletInfo.from_api_response(response.json())
        else:
            raise ValueError("Use get_wallet_info for sync clients")
    
    def create_account(self, account: AccountCreateRequest) -> AccountDetailModel:
        """
        Create a new Airwallex account.
        
        Args:
            account: AccountCreateRequest model with account creation details.
            
        Returns:
            AccountDetailModel: The created account.
        """
        url = "/api/v1/accounts/create"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url, json=account.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use create_account_async for async clients")
            
    async def create_account_async(self, account: AccountCreateRequest) -> AccountDetailModel:
        """
        Create a new Airwallex account asynchronously.
        
        Args:
            account: AccountCreateRequest model with account creation details.
            
        Returns:
            AccountDetailModel: The created account.
        """
        url = "/api/v1/accounts/create"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url, json=account.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use create_account for sync clients")
    
    def update_account(self, account_id: str, account: AccountUpdateRequest) -> AccountDetailModel:
        """
        Update a connected account.
        
        Args:
            account_id: The ID of the account to update.
            account: AccountUpdateRequest model with account update details.
            
        Returns:
            AccountDetailModel: The updated account.
        """
        url = f"/api/v1/accounts/{account_id}/update"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url, json=account.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use update_account_async for async clients")
            
    async def update_account_async(self, account_id: str, account: AccountUpdateRequest) -> AccountDetailModel:
        """
        Update a connected account asynchronously.
        
        Args:
            account_id: The ID of the account to update.
            account: AccountUpdateRequest model with account update details.
            
        Returns:
            AccountDetailModel: The updated account.
        """
        url = f"/api/v1/accounts/{account_id}/update"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url, json=account.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use update_account for sync clients")
    
    def submit_account(self, account_id: str) -> AccountDetailModel:
        """
        Submit account for activation.
        
        Args:
            account_id: The ID of the account to submit.
            
        Returns:
            AccountDetailModel: The submitted account.
        """
        url = f"/api/v1/accounts/{account_id}/submit"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url)
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use submit_account_async for async clients")
            
    async def submit_account_async(self, account_id: str) -> AccountDetailModel:
        """
        Submit account for activation asynchronously.
        
        Args:
            account_id: The ID of the account to submit.
            
        Returns:
            AccountDetailModel: The submitted account.
        """
        url = f"/api/v1/accounts/{account_id}/submit"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url)
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use submit_account for sync clients")
    
    def get_account(self, account_id: str) -> AccountDetailModel:
        """
        Get account by ID.
        
        Args:
            account_id: The ID of the account to retrieve.
            
        Returns:
            AccountDetailModel: The account.
        """
        url = f"/api/v1/accounts/{account_id}"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", url)
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use get_account_async for async clients")
            
    async def get_account_async(self, account_id: str) -> AccountDetailModel:
        """
        Get account by ID asynchronously.
        
        Args:
            account_id: The ID of the account to retrieve.
            
        Returns:
            AccountDetailModel: The account.
        """
        url = f"/api/v1/accounts/{account_id}"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", url)
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use get_account for sync clients")
    
    def list_accounts(
        self,
        account_status: Optional[str] = None,
        email: Optional[str] = None,
        from_created_at: Optional[Union[str, datetime]] = None,
        identifier: Optional[str] = None,
        metadata: Optional[str] = None,
        page_num: Optional[int] = None,
        page_size: Optional[int] = None,
        to_created_at: Optional[Union[str, datetime]] = None
    ) -> List[AccountDetailModel]:
        """
        Get list of connected accounts with filtering options.
        
        Args:
            account_status: Filter by account status (CREATED, SUBMITTED, ACTION_REQUIRED, ACTIVE, SUSPENDED)
            email: Filter by email
            from_created_at: Filter by creation date (start, inclusive)
            identifier: Filter by identifier
            metadata: Filter by metadata (key:value format)
            page_num: Page number (0-indexed)
            page_size: Number of results per page (default 100, max 500)
            to_created_at: Filter by creation date (end, inclusive)
            
        Returns:
            List[AccountDetailModel]: List of matching accounts.
        """
        url = "/api/v1/accounts"
        params = {}
        
        if account_status:
            params["account_status"] = account_status
        
        if email:
            params["email"] = email
        
        if from_created_at:
            if isinstance(from_created_at, datetime):
                from_created_at = from_created_at.isoformat()
            params["from_created_at"] = from_created_at
        
        if identifier:
            params["identifier"] = identifier
        
        if metadata:
            params["metadata"] = metadata
        
        if page_num is not None:
            params["page_num"] = page_num
        
        if page_size is not None:
            params["page_size"] = page_size
        
        if to_created_at:
            if isinstance(to_created_at, datetime):
                to_created_at = to_created_at.isoformat()
            params["to_created_at"] = to_created_at
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", url, params=params)
            data = response.json()
            return [self.model_class.from_api_response(item) for item in data.get("items", [])]
        else:
            raise ValueError("Use list_accounts_async for async clients")
            
    async def list_accounts_async(
        self,
        account_status: Optional[str] = None,
        email: Optional[str] = None,
        from_created_at: Optional[Union[str, datetime]] = None,
        identifier: Optional[str] = None,
        metadata: Optional[str] = None,
        page_num: Optional[int] = None,
        page_size: Optional[int] = None,
        to_created_at: Optional[Union[str, datetime]] = None
    ) -> List[AccountDetailModel]:
        """
        Get list of connected accounts with filtering options asynchronously.
        
        Args:
            account_status: Filter by account status (CREATED, SUBMITTED, ACTION_REQUIRED, ACTIVE, SUSPENDED)
            email: Filter by email
            from_created_at: Filter by creation date (start, inclusive)
            identifier: Filter by identifier
            metadata: Filter by metadata (key:value format)
            page_num: Page number (0-indexed)
            page_size: Number of results per page (default 100, max 500)
            to_created_at: Filter by creation date (end, inclusive)
            
        Returns:
            List[AccountDetailModel]: List of matching accounts.
        """
        url = "/api/v1/accounts"
        params = {}
        
        if account_status:
            params["account_status"] = account_status
        
        if email:
            params["email"] = email
        
        if from_created_at:
            if isinstance(from_created_at, datetime):
                from_created_at = from_created_at.isoformat()
            params["from_created_at"] = from_created_at
        
        if identifier:
            params["identifier"] = identifier
        
        if metadata:
            params["metadata"] = metadata
        
        if page_num is not None:
            params["page_num"] = page_num
        
        if page_size is not None:
            params["page_size"] = page_size
        
        if to_created_at:
            if isinstance(to_created_at, datetime):
                to_created_at = to_created_at.isoformat()
            params["to_created_at"] = to_created_at
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", url, params=params)
            data = response.json()
            return [self.model_class.from_api_response(item) for item in data.get("items", [])]
        else:
            raise ValueError("Use list_accounts for sync clients")
    
    def agree_to_terms(self, account_id: str, request: TermsAndConditionsRequest) -> AccountDetailModel:
        """
        Agree to terms and conditions.
        
        Args:
            account_id: The ID of the account agreeing to terms.
            request: TermsAndConditionsRequest model with agreement details.
            
        Returns:
            AccountDetailModel: The updated account.
        """
        url = f"/api/v1/accounts/{account_id}/terms_and_conditions/agree"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url, json=request.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use agree_to_terms_async for async clients")
            
    async def agree_to_terms_async(self, account_id: str, request: TermsAndConditionsRequest) -> AccountDetailModel:
        """
        Agree to terms and conditions asynchronously.
        
        Args:
            account_id: The ID of the account agreeing to terms.
            request: TermsAndConditionsRequest model with agreement details.
            
        Returns:
            AccountDetailModel: The updated account.
        """
        url = f"/api/v1/accounts/{account_id}/terms_and_conditions/agree"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url, json=request.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use agree_to_terms for sync clients")