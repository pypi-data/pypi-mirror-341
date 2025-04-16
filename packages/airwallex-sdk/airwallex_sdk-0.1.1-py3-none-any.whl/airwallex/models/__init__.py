"""
Pydantic models for the Airwallex API.
"""
from .base import AirwallexModel
from .account import Account as AccountModel
from .payment import Payment as PaymentModel
from .beneficiary import Beneficiary as BeneficiaryModel
from .invoice import Invoice as InvoiceModel, InvoiceItem
from .financial_transaction import FinancialTransaction as FinancialTransactionModel
from .fx import FXConversion, FXQuote
from .account_detail import (
    AccountDetailModel, AccountCreateRequest, AccountUpdateRequest,
    Amendment, AmendmentCreateRequest, WalletInfo, TermsAndConditionsRequest
)

# Issuing API Models
from .issuing_common import (
    Address,
    Name,
    Merchant,
    RiskDetails,
    DeviceInformation,
    TransactionUsage,
    DeliveryDetails,
    HasMoreResponse
)
from .issuing_authorization import Authorization as IssuingAuthorizationModel
from .issuing_cardholder import Cardholder as IssuingCardholderModel
from .issuing_card import Card as IssuingCardModel, CardDetails
from .issuing_digital_wallet_token import DigitalWalletToken as IssuingDigitalWalletTokenModel
from .issuing_transaction_dispute import TransactionDispute as IssuingTransactionDisputeModel
from .issuing_transaction import Transaction as IssuingTransactionModel
from .issuing_config import IssuingConfig as IssuingConfigModel

__all__ = [
    "AirwallexModel",
    "AccountModel",
    "PaymentModel",
    "BeneficiaryModel",
    "InvoiceModel",
    "InvoiceItem",
    "FinancialTransactionModel",
    "FXConversion",
    "FXQuote",
    "AccountDetailModel",
    "AccountCreateRequest",
    "AccountUpdateRequest",
    "Amendment", 
    "AmendmentCreateRequest", 
    "WalletInfo", 
    "TermsAndConditionsRequest",
    # Issuing API
    "Address",
    "Name",
    "Merchant",
    "RiskDetails",
    "DeviceInformation",
    "TransactionUsage",
    "DeliveryDetails",
    "HasMoreResponse",
    "IssuingAuthorizationModel",
    "IssuingCardholderModel",
    "IssuingCardModel",
    "CardDetails",
    "IssuingDigitalWalletTokenModel",
    "IssuingTransactionDisputeModel",
    "IssuingTransactionModel",
    "IssuingConfigModel",
]