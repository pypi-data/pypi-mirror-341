"""
Airwallex Beneficiary API.
"""
from typing import Dict, Any, List, Optional, Type, TypeVar, Union, cast
from ..models.beneficiary import Beneficiary as BeneficiaryModel, BeneficiaryCreateRequest, BeneficiaryUpdateRequest
from .base import AirwallexAPIBase

T = TypeVar("T", bound=BeneficiaryModel)


class Beneficiary(AirwallexAPIBase[BeneficiaryModel]):
    """
    Operations for Airwallex beneficiaries.
    
    Beneficiaries represent recipients of payments.
    """
    endpoint = "beneficiaries"
    model_class = cast(Type[BeneficiaryModel], BeneficiaryModel)
    
    def create_from_model(self, beneficiary: BeneficiaryCreateRequest) -> BeneficiaryModel:
        """
        Create a new beneficiary using a Pydantic model.
        
        Args:
            beneficiary: BeneficiaryCreateRequest model with beneficiary creation details.
            
        Returns:
            Beneficiary: The created beneficiary.
        """
        return self.create(beneficiary)
    
    async def create_from_model_async(self, beneficiary: BeneficiaryCreateRequest) -> BeneficiaryModel:
        """
        Create a new beneficiary using a Pydantic model asynchronously.
        
        Args:
            beneficiary: BeneficiaryCreateRequest model with beneficiary creation details.
            
        Returns:
            Beneficiary: The created beneficiary.
        """
        return await self.create_async(beneficiary)
    
    def update_from_model(self, beneficiary_id: str, beneficiary: BeneficiaryUpdateRequest) -> BeneficiaryModel:
        """
        Update a beneficiary using a Pydantic model.
        
        Args:
            beneficiary_id: The ID of the beneficiary to update.
            beneficiary: BeneficiaryUpdateRequest model with beneficiary update details.
            
        Returns:
            Beneficiary: The updated beneficiary.
        """
        return self.update(beneficiary_id, beneficiary)
    
    async def update_from_model_async(self, beneficiary_id: str, beneficiary: BeneficiaryUpdateRequest) -> BeneficiaryModel:
        """
        Update a beneficiary using a Pydantic model asynchronously.
        
        Args:
            beneficiary_id: The ID of the beneficiary to update.
            beneficiary: BeneficiaryUpdateRequest model with beneficiary update details.
            
        Returns:
            Beneficiary: The updated beneficiary.
        """
        return await self.update_async(beneficiary_id, beneficiary)
    
    def validate(self, beneficiary: BeneficiaryCreateRequest) -> Dict[str, Any]:
        """
        Validate a beneficiary without creating it.
        
        Args:
            beneficiary: BeneficiaryCreateRequest model with beneficiary details.
            
        Returns:
            Dict[str, Any]: Validation results.
        """
        url = self._build_url(suffix="validate")
        
        if not self.client.__class__.__name__.startswith('Async'):
            response = self.client._request("POST", url, json=beneficiary.to_api_dict())
            return response.json()
        else:
            raise ValueError("Use validate_async for async clients")
    
    async def validate_async(self, beneficiary: BeneficiaryCreateRequest) -> Dict[str, Any]:
        """
        Validate a beneficiary without creating it asynchronously.
        
        Args:
            beneficiary: BeneficiaryCreateRequest model with beneficiary details.
            
        Returns:
            Dict[str, Any]: Validation results.
        """
        url = self._build_url(suffix="validate")
        
        if self.client.__class__.__name__.startswith('Async'):
            response = await self.client._request("POST", url, json=beneficiary.to_api_dict())
            return response.json()
        else:
            raise ValueError("Use validate for sync clients")
    
    def deactivate(self, beneficiary_id: str) -> BeneficiaryModel:
        """
        Deactivate a beneficiary.
        
        Args:
            beneficiary_id: The ID of the beneficiary to deactivate.
            
        Returns:
            Beneficiary: The deactivated beneficiary.
        """
        update_request = BeneficiaryUpdateRequest(status="disabled")
        return self.update(beneficiary_id, update_request)
    
    async def deactivate_async(self, beneficiary_id: str) -> BeneficiaryModel:
        """
        Deactivate a beneficiary asynchronously.
        
        Args:
            beneficiary_id: The ID of the beneficiary to deactivate.
            
        Returns:
            Beneficiary: The deactivated beneficiary.
        """
        update_request = BeneficiaryUpdateRequest(status="disabled")
        return await self.update_async(beneficiary_id, update_request)
    
    def activate(self, beneficiary_id: str) -> BeneficiaryModel:
        """
        Activate a beneficiary.
        
        Args:
            beneficiary_id: The ID of the beneficiary to activate.
            
        Returns:
            Beneficiary: The activated beneficiary.
        """
        update_request = BeneficiaryUpdateRequest(status="active")
        return self.update(beneficiary_id, update_request)
    
    async def activate_async(self, beneficiary_id: str) -> BeneficiaryModel:
        """
        Activate a beneficiary asynchronously.
        
        Args:
            beneficiary_id: The ID of the beneficiary to activate.
            
        Returns:
            Beneficiary: The activated beneficiary.
        """
        update_request = BeneficiaryUpdateRequest(status="active")
        return await self.update_async(beneficiary_id, update_request)
