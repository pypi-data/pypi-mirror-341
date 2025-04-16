"""
Airwallex Issuing Transaction Dispute API.
"""
from typing import Dict, Any, List, Optional, Type, TypeVar, Union, cast
from datetime import datetime
from ..models.issuing_transaction_dispute import TransactionDispute, TransactionDisputeCreateRequest, TransactionDisputeUpdateRequest
from .base import AirwallexAPIBase

T = TypeVar("T", bound=TransactionDispute)


class IssuingTransactionDispute(AirwallexAPIBase[TransactionDispute]):
    """
    Operations for Airwallex issuing transaction disputes.
    
    Transaction disputes represent disputes against card transactions.
    """
    endpoint = "issuing/transaction_disputes"
    model_class = cast(Type[TransactionDispute], TransactionDispute)
    
    def create_dispute(self, dispute: TransactionDisputeCreateRequest) -> TransactionDispute:
        """
        Create a new transaction dispute.
        
        Args:
            dispute: TransactionDisputeCreateRequest model with dispute details
            
        Returns:
            TransactionDispute: The created transaction dispute
        """
        url = f"{self.base_path}/create"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url, json=dispute.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use create_dispute_async for async clients")
    
    async def create_dispute_async(self, dispute: TransactionDisputeCreateRequest) -> TransactionDispute:
        """
        Create a new transaction dispute asynchronously.
        
        Args:
            dispute: TransactionDisputeCreateRequest model with dispute details
            
        Returns:
            TransactionDispute: The created transaction dispute
        """
        url = f"{self.base_path}/create"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url, json=dispute.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use create_dispute for sync clients")
    
    def update_dispute(self, dispute_id: str, update_data: TransactionDisputeUpdateRequest) -> TransactionDispute:
        """
        Update a transaction dispute.
        
        Args:
            dispute_id: The ID of the dispute to update
            update_data: TransactionDisputeUpdateRequest model with update details
            
        Returns:
            TransactionDispute: The updated transaction dispute
        """
        url = f"{self._build_url(dispute_id)}/update"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url, json=update_data.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use update_dispute_async for async clients")
    
    async def update_dispute_async(self, dispute_id: str, update_data: TransactionDisputeUpdateRequest) -> TransactionDispute:
        """
        Update a transaction dispute asynchronously.
        
        Args:
            dispute_id: The ID of the dispute to update
            update_data: TransactionDisputeUpdateRequest model with update details
            
        Returns:
            TransactionDispute: The updated transaction dispute
        """
        url = f"{self._build_url(dispute_id)}/update"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url, json=update_data.to_api_dict())
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use update_dispute for sync clients")
    
    def submit_dispute(self, dispute_id: str) -> TransactionDispute:
        """
        Submit a transaction dispute.
        
        Args:
            dispute_id: The ID of the dispute to submit
            
        Returns:
            TransactionDispute: The submitted transaction dispute
        """
        url = f"{self._build_url(dispute_id)}/submit"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url)
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use submit_dispute_async for async clients")
    
    async def submit_dispute_async(self, dispute_id: str) -> TransactionDispute:
        """
        Submit a transaction dispute asynchronously.
        
        Args:
            dispute_id: The ID of the dispute to submit
            
        Returns:
            TransactionDispute: The submitted transaction dispute
        """
        url = f"{self._build_url(dispute_id)}/submit"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url)
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use submit_dispute for sync clients")
    
    def cancel_dispute(self, dispute_id: str) -> TransactionDispute:
        """
        Cancel a transaction dispute.
        
        Args:
            dispute_id: The ID of the dispute to cancel
            
        Returns:
            TransactionDispute: The cancelled transaction dispute
        """
        url = f"{self._build_url(dispute_id)}/cancel"
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url)
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use cancel_dispute_async for async clients")
    
    async def cancel_dispute_async(self, dispute_id: str) -> TransactionDispute:
        """
        Cancel a transaction dispute asynchronously.
        
        Args:
            dispute_id: The ID of the dispute to cancel
            
        Returns:
            TransactionDispute: The cancelled transaction dispute
        """
        url = f"{self._build_url(dispute_id)}/cancel"
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url)
            return self.model_class.from_api_response(response.json())
        else:
            raise ValueError("Use cancel_dispute for sync clients")
    
    def list_with_filters(
        self,
        detailed_status: Optional[str] = None,
        from_created_at: Optional[Union[str, datetime]] = None,
        from_updated_at: Optional[Union[str, datetime]] = None,
        page: Optional[str] = None,
        page_size: int = 10,
        reason: Optional[str] = None,
        reference: Optional[str] = None,
        status: Optional[str] = None,
        to_created_at: Optional[Union[str, datetime]] = None,
        to_updated_at: Optional[Union[str, datetime]] = None,
        transaction_id: Optional[str] = None,
        updated_by: Optional[str] = None
    ) -> List[TransactionDispute]:
        """
        List transaction disputes with filtering options.
        
        Args:
            detailed_status: Filter by detailed status
            from_created_at: Filter by creation date (start, inclusive)
            from_updated_at: Filter by update date (start, inclusive)
            page: Page bookmark for pagination
            page_size: Number of results per page
            reason: Filter by dispute reason
            reference: Filter by reference
            status: Filter by status
            to_created_at: Filter by creation date (end, exclusive)
            to_updated_at: Filter by update date (end, exclusive)
            transaction_id: Filter by transaction ID
            updated_by: Filter by who last updated the dispute
            
        Returns:
            List[TransactionDispute]: List of matching transaction disputes
        """
        params = {
            "page_size": page_size
        }
        
        if detailed_status:
            params["detailed_status"] = detailed_status
            
        if from_created_at:
            if isinstance(from_created_at, datetime):
                from_created_at = from_created_at.isoformat()
            params["from_created_at"] = from_created_at
            
        if from_updated_at:
            if isinstance(from_updated_at, datetime):
                from_updated_at = from_updated_at.isoformat()
            params["from_updated_at"] = from_updated_at
            
        if page:
            params["page"] = page
            
        if reason:
            params["reason"] = reason
            
        if reference:
            params["reference"] = reference
            
        if status:
            params["status"] = status
            
        if to_created_at:
            if isinstance(to_created_at, datetime):
                to_created_at = to_created_at.isoformat()
            params["to_created_at"] = to_created_at
            
        if to_updated_at:
            if isinstance(to_updated_at, datetime):
                to_updated_at = to_updated_at.isoformat()
            params["to_updated_at"] = to_updated_at
            
        if transaction_id:
            params["transaction_id"] = transaction_id
            
        if updated_by:
            params["updated_by"] = updated_by
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("GET", self._build_url(), params=params)
            data = response.json()
            return [self.model_class.from_api_response(item) for item in data.get("items", [])]
        else:
            raise ValueError("Use list_with_filters_async for async clients")
    
    async def list_with_filters_async(
        self,
        detailed_status: Optional[str] = None,
        from_created_at: Optional[Union[str, datetime]] = None,
        from_updated_at: Optional[Union[str, datetime]] = None,
        page: Optional[str] = None,
        page_size: int = 10,
        reason: Optional[str] = None,
        reference: Optional[str] = None,
        status: Optional[str] = None,
        to_created_at: Optional[Union[str, datetime]] = None,
        to_updated_at: Optional[Union[str, datetime]] = None,
        transaction_id: Optional[str] = None,
        updated_by: Optional[str] = None
    ) -> List[TransactionDispute]:
        """
        List transaction disputes with filtering options asynchronously.
        
        Args:
            detailed_status: Filter by detailed status
            from_created_at: Filter by creation date (start, inclusive)
            from_updated_at: Filter by update date (start, inclusive)
            page: Page bookmark for pagination
            page_size: Number of results per page
            reason: Filter by dispute reason
            reference: Filter by reference
            status: Filter by status
            to_created_at: Filter by creation date (end, exclusive)
            to_updated_at: Filter by update date (end, exclusive)
            transaction_id: Filter by transaction ID
            updated_by: Filter by who last updated the dispute
            
        Returns:
            List[TransactionDispute]: List of matching transaction disputes
        """
        params = {
            "page_size": page_size
        }
        
        if detailed_status:
            params["detailed_status"] = detailed_status
            
        if from_created_at:
            if isinstance(from_created_at, datetime):
                from_created_at = from_created_at.isoformat()
            params["from_created_at"] = from_created_at
            
        if from_updated_at:
            if isinstance(from_updated_at, datetime):
                from_updated_at = from_updated_at.isoformat()
            params["from_updated_at"] = from_updated_at
            
        if page:
            params["page"] = page
            
        if reason:
            params["reason"] = reason
            
        if reference:
            params["reference"] = reference
            
        if status:
            params["status"] = status
            
        if to_created_at:
            if isinstance(to_created_at, datetime):
                to_created_at = to_created_at.isoformat()
            params["to_created_at"] = to_created_at
            
        if to_updated_at:
            if isinstance(to_updated_at, datetime):
                to_updated_at = to_updated_at.isoformat()
            params["to_updated_at"] = to_updated_at
            
        if transaction_id:
            params["transaction_id"] = transaction_id
            
        if updated_by:
            params["updated_by"] = updated_by
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("GET", self._build_url(), params=params)
            data = response.json()
            return [self.model_class.from_api_response(item) for item in data.get("items", [])]
        else:
            raise ValueError("Use list_with_filters for sync clients")
