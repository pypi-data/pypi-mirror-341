"""
Airwallex Financial Transaction API.
"""
from typing import Dict, Any, List, Optional, Type, TypeVar, Union, cast
from datetime import datetime
from ..models.financial_transaction import FinancialTransaction
from .base import AirwallexAPIBase

T = TypeVar("T", bound=FinancialTransaction)


class FinancialTransaction(AirwallexAPIBase[FinancialTransaction]):
    """
    Operations for Airwallex financial transactions.
    
    Financial transactions represent the transactions that contributed to the Airwallex account balance.
    """
    endpoint = "financial_transactions"
    model_class = cast(Type[FinancialTransaction], FinancialTransaction)
    
    def list_with_filters(
        self, 
        batch_id: Optional[str] = None,
        currency: Optional[str] = None,
        from_created_at: Optional[Union[str, datetime]] = None,
        to_created_at: Optional[Union[str, datetime]] = None,
        source_id: Optional[str] = None,
        status: Optional[str] = None,
        page_num: int = 0,
        page_size: int = 100
    ) -> List[FinancialTransaction]:
        """
        List financial transactions with filtering options.
        
        Args:
            batch_id: Filter by batch ID
            currency: Filter by currency (3-letter ISO-4217 code)
            from_created_at: Filter by creation date (start, inclusive)
            to_created_at: Filter by creation date (end, inclusive)
            source_id: Filter by source ID
            status: Filter by status (PENDING, SETTLED)
            page_num: Page number (0-indexed) for pagination
            page_size: Number of transactions per page (max 1000)
            
        Returns:
            List[FinancialTransaction]: List of matching financial transactions
        """
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if batch_id:
            params["batch_id"] = batch_id
        
        if currency:
            params["currency"] = currency
        
        if source_id:
            params["source_id"] = source_id
        
        if status:
            params["status"] = status
        
        if from_created_at:
            params["from_created_at"] = from_created_at
        
        if to_created_at:
            params["to_created_at"] = to_created_at
        
        return self.list(**params)
    
    async def list_with_filters_async(
        self, 
        batch_id: Optional[str] = None,
        currency: Optional[str] = None,
        from_created_at: Optional[Union[str, datetime]] = None,
        to_created_at: Optional[Union[str, datetime]] = None,
        source_id: Optional[str] = None,
        status: Optional[str] = None,
        page_num: int = 0,
        page_size: int = 100
    ) -> List[FinancialTransaction]:
        """
        List financial transactions with filtering options asynchronously.
        
        Args:
            batch_id: Filter by batch ID
            currency: Filter by currency (3-letter ISO-4217 code)
            from_created_at: Filter by creation date (start, inclusive)
            to_created_at: Filter by creation date (end, inclusive)
            source_id: Filter by source ID
            status: Filter by status (PENDING, SETTLED)
            page_num: Page number (0-indexed) for pagination
            page_size: Number of transactions per page (max 1000)
            
        Returns:
            List[FinancialTransaction]: List of matching financial transactions
        """
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if batch_id:
            params["batch_id"] = batch_id
        
        if currency:
            params["currency"] = currency
        
        if source_id:
            params["source_id"] = source_id
        
        if status:
            params["status"] = status
        
        if from_created_at:
            params["from_created_at"] = from_created_at
        
        if to_created_at:
            params["to_created_at"] = to_created_at
        
        return await self.list_async(**params)