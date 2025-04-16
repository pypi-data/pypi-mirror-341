"""
Airwallex Python SDK.

A fully-featured SDK for interacting with the Airwallex API.
"""
from .client import AirwallexClient, AirwallexAsyncClient
from .exceptions import (
    AirwallexAPIError,
    AuthenticationError,
    RateLimitError,
    ResourceNotFoundError,
    ValidationError,
    ServerError
)

# Import models
from .models import AirwallexModel
from .models.account import Account as AccountModel
from .models.payment import Payment as PaymentModel
from .models.beneficiary import Beneficiary as BeneficiaryModel
from .models.invoice import Invoice as InvoiceModel, InvoiceItem
from .models.financial_transaction import FinancialTransaction as FinancialTransactionModel
from .models.fx import FXConversion, FXQuote
from .models.account_detail import (
    AccountDetailModel, AccountCreateRequest, AccountUpdateRequest,
    Amendment, AmendmentCreateRequest, WalletInfo, TermsAndConditionsRequest
)

# Issuing API Models
from .models.issuing_authorization import Authorization as IssuingAuthorizationModel
from .models.issuing_cardholder import Cardholder as IssuingCardholderModel
from .models.issuing_card import Card as IssuingCardModel, CardDetails
from .models.issuing_digital_wallet_token import DigitalWalletToken as IssuingDigitalWalletTokenModel
from .models.issuing_transaction_dispute import TransactionDispute as IssuingTransactionDisputeModel
from .models.issuing_transaction import Transaction as IssuingTransactionModel
from .models.issuing_config import IssuingConfig as IssuingConfigModel

__all__ = [
    "AirwallexClient",
    "AirwallexAsyncClient",
    "AirwallexAPIError",
    "AuthenticationError",
    "RateLimitError",
    "ResourceNotFoundError",
    "ValidationError",
    "ServerError",
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
    "IssuingAuthorizationModel",
    "IssuingCardholderModel",
    "IssuingCardModel",
    "CardDetails",
    "IssuingDigitalWalletTokenModel",
    "IssuingTransactionDisputeModel",
    "IssuingTransactionModel",
    "IssuingConfigModel",
]

__version__ = "0.2.0"