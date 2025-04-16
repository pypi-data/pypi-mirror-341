"""
Models for the Airwallex Account Detail API.
"""
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import Field, EmailStr
from .base import AirwallexModel

class Address(AirwallexModel):
    """Model for an address."""
    address_line1: str = Field(..., description="Address line 1")
    address_line2: Optional[str] = Field(None, description="Address line 2")
    country_code: str = Field(..., description="Country code (ISO 3166-1 alpha-2)")
    postcode: str = Field(..., description="Postal code")
    state: Optional[str] = Field(None, description="State or province")
    suburb: Optional[str] = Field(None, description="Suburb or city")

class BusinessIdentifier(AirwallexModel):
    """Model for a business identifier."""
    country_code: str = Field(..., description="Country code (ISO 3166-1 alpha-2)")
    number: str = Field(..., description="Identifier number")
    type: str = Field(..., description="Identifier type (e.g., 'BRN')")

class EstimatedMonthlyRevenue(AirwallexModel):
    """Model for estimated monthly revenue."""
    amount: str = Field(..., description="Amount as string")
    currency: str = Field(..., description="Currency code (ISO 4217)")

class AccountUsage(AirwallexModel):
    """Model for account usage information."""
    estimated_monthly_revenue: EstimatedMonthlyRevenue = Field(..., description="Estimated monthly revenue")
    product_reference: List[str] = Field(..., description="List of product references")

class BusinessDocument(AirwallexModel):
    """Model for a business document."""
    description: Optional[str] = Field(None, description="Document description")
    file_id: str = Field(..., description="File ID")
    tag: str = Field(..., description="Document tag (e.g., 'BUSINESS_LICENSE')")

class BusinessDocuments(AirwallexModel):
    """Model for business documents."""
    business_documents: List[BusinessDocument] = Field(..., description="List of business documents")

class BusinessAttachments(AirwallexModel):
    """Model for business attachments."""
    business_documents: Optional[List[BusinessDocument]] = Field(None, description="List of business documents")

class BusinessDetails(AirwallexModel):
    """Model for business details."""
    account_usage: AccountUsage = Field(..., description="Account usage information")
    as_trustee: Optional[bool] = Field(None, description="Whether the business acts as a trustee")
    attachments: Optional[BusinessAttachments] = Field(None, description="Business attachments")
    business_address: Address = Field(..., description="Business address")
    business_identifiers: List[BusinessIdentifier] = Field(..., description="Business identifiers")
    business_name: str = Field(..., description="Business name")
    business_name_english: Optional[str] = Field(None, description="Business name in English")
    business_name_trading: Optional[str] = Field(None, description="Trading name of the business")
    business_start_date: Optional[str] = Field(None, description="Business start date (YYYY-MM-DD)")
    business_structure: str = Field(..., description="Business structure (e.g., 'COMPANY')")
    contact_number: Optional[str] = Field(None, description="Contact phone number")
    description_of_goods_or_services: Optional[str] = Field(None, description="Description of goods or services")
    explanation_for_high_risk_countries_exposure: Optional[str] = Field(None, description="Explanation for high risk countries exposure")
    has_nominee_shareholders: Optional[bool] = Field(None, description="Whether the business has nominee shareholders")
    industry_category_code: str = Field(..., description="Industry category code")
    no_shareholders_with_over_25percent: Optional[bool] = Field(None, description="Whether there are no shareholders with over 25% ownership")
    operating_country: List[str] = Field(..., description="Operating countries (ISO 3166-1 alpha-2 codes)")
    registration_address: Address = Field(..., description="Registration address")
    registration_address_english: Optional[Address] = Field(None, description="Registration address in English")
    state_of_incorporation: Optional[str] = Field(None, description="State of incorporation")
    url: Optional[str] = Field(None, description="Business website URL")

class DriversLicense(AirwallexModel):
    """Model for driver's license identification."""
    back_file_id: Optional[str] = Field(None, description="File ID for back of license")
    effective_at: str = Field(..., description="Effective date (YYYY-MM-DD)")
    expire_at: str = Field(..., description="Expiry date (YYYY-MM-DD)")
    front_file_id: str = Field(..., description="File ID for front of license")
    gender: Optional[str] = Field(None, description="Gender (e.g., 'F' for female)")
    issuing_state: Optional[str] = Field(None, description="Issuing state")
    number: str = Field(..., description="License number")
    version: Optional[str] = Field(None, description="License version")

class Passport(AirwallexModel):
    """Model for passport identification."""
    effective_at: str = Field(..., description="Effective date (YYYY-MM-DD)")
    expire_at: str = Field(..., description="Expiry date (YYYY-MM-DD)")
    front_file_id: str = Field(..., description="File ID for passport")
    mrz_line1: Optional[str] = Field(None, description="MRZ line 1")
    mrz_line2: Optional[str] = Field(None, description="MRZ line 2")
    number: str = Field(..., description="Passport number")

class PersonalId(AirwallexModel):
    """Model for personal ID identification."""
    back_file_id: Optional[str] = Field(None, description="File ID for back of ID")
    effective_at: str = Field(..., description="Effective date (YYYY-MM-DD)")
    expire_at: str = Field(..., description="Expiry date (YYYY-MM-DD)")
    front_file_id: str = Field(..., description="File ID for front of ID")
    number: str = Field(..., description="ID number")

class PrimaryIdentification(AirwallexModel):
    """Model for primary identification."""
    drivers_license: Optional[DriversLicense] = Field(None, description="Driver's license details")
    identification_type: str = Field(..., description="Identification type (e.g., 'PASSPORT')")
    issuing_country_code: str = Field(..., description="Issuing country code (ISO 3166-1 alpha-2)")
    passport: Optional[Passport] = Field(None, description="Passport details")
    personal_id: Optional[PersonalId] = Field(None, description="Personal ID details")

class Identifications(AirwallexModel):
    """Model for identifications."""
    primary: PrimaryIdentification = Field(..., description="Primary identification")

class BusinessPersonDocument(AirwallexModel):
    """Model for a business person document."""
    description: Optional[str] = Field(None, description="Document description")
    file_id: str = Field(..., description="File ID")
    tag: str = Field(..., description="Document tag")

class BusinessPersonAttachments(AirwallexModel):
    """Model for business person attachments."""
    business_person_documents: List[BusinessPersonDocument] = Field(..., description="List of business person documents")

class BusinessPersonDetails(AirwallexModel):
    """Model for business person details."""
    attachments: Optional[BusinessPersonAttachments] = Field(None, description="Business person attachments")
    date_of_birth: str = Field(..., description="Date of birth (YYYY-MM-DD)")
    email: EmailStr = Field(..., description="Email address")
    first_name: str = Field(..., description="First name")
    first_name_english: Optional[str] = Field(None, description="First name in English")
    identifications: Identifications = Field(..., description="Identifications")
    last_name: str = Field(..., description="Last name")
    last_name_english: Optional[str] = Field(None, description="Last name in English")
    middle_name: Optional[str] = Field(None, description="Middle name")
    middle_name_english: Optional[str] = Field(None, description="Middle name in English")
    mobile: Optional[str] = Field(None, description="Mobile phone number")
    residential_address: Optional[Address] = Field(None, description="Residential address")
    residential_address_english: Optional[Address] = Field(None, description="Residential address in English")
    role: str = Field(..., description="Role (e.g., 'DIRECTOR')")
    title: Optional[str] = Field(None, description="Title (e.g., 'Mr')")

class AdditionalFile(AirwallexModel):
    """Model for an additional file."""
    description: Optional[str] = Field(None, description="File description")
    file_id: str = Field(..., description="File ID")
    tag: str = Field(..., description="File tag")

class AccountAttachments(AirwallexModel):
    """Model for account attachments."""
    additional_files: Optional[List[AdditionalFile]] = Field(None, description="List of additional files")

class AccountDetails(AirwallexModel):
    """Model for account details."""
    attachments: Optional[AccountAttachments] = Field(None, description="Account attachments")
    business_details: BusinessDetails = Field(..., description="Business details")
    business_person_details: List[BusinessPersonDetails] = Field(..., description="Business person details")

class CustomerAgreements(AirwallexModel):
    """Model for customer agreements."""
    tnc_accepted: bool = Field(..., description="Whether terms and conditions are accepted")
    marketing_emails_opt_in: Optional[bool] = Field(None, description="Whether marketing emails are opted in")

class PrimaryContact(AirwallexModel):
    """Model for primary contact information."""
    email: EmailStr = Field(..., description="Email address")
    mobile: Optional[str] = Field(None, description="Mobile phone number")

class NextAction(AirwallexModel):
    """Model for next action information."""
    type: str = Field(..., description="Action type")
    message: Optional[str] = Field(None, description="Action message")

class Requirements(AirwallexModel):
    """Model for requirements information."""
    current_deadline: Optional[str] = Field(None, description="Current deadline (ISO 8601 format)")
    currently_due: List[str] = Field(..., description="List of currently due requirements")
    eventually_due: List[str] = Field(..., description="List of eventually due requirements")
    past_due: List[str] = Field(..., description="List of past due requirements")

class AccountDetailModel(AirwallexModel):
    """Model for an Airwallex account detail."""
    resource_name: str = "accounts"
    
    account_details: Optional[AccountDetails] = Field(None, description="Account details")
    created_at: str = Field(..., description="Account creation timestamp (ISO 8601 format)")
    customer_agreements: Optional[CustomerAgreements] = Field(None, description="Customer agreements")
    id: str = Field(..., description="Airwallex account ID")
    identifier: Optional[str] = Field(None, description="Platform identifier for the merchant")
    metadata: Optional[Dict[str, str]] = Field(None, description="Additional metadata")
    next_action: Optional[NextAction] = Field(None, description="Next action information")
    nickname: Optional[str] = Field(None, description="Human-friendly account name")
    primary_contact: Optional[PrimaryContact] = Field(None, description="Primary contact information")
    requirements: Optional[Requirements] = Field(None, description="Requirements information")
    status: str = Field(..., description="Account status (CREATED, SUBMITTED, ACTION_REQUIRED, ACTIVE, SUSPENDED)")
    view_type: Optional[str] = Field(None, description="View type information")

# Request Models
class AccountCreateRequest(AirwallexModel):
    """Model for account creation request."""
    account_details: Optional[AccountDetails] = Field(None, description="Account details")
    customer_agreements: Optional[CustomerAgreements] = Field(None, description="Customer agreements")
    identifier: Optional[str] = Field(None, description="Platform identifier for the merchant")
    metadata: Optional[Dict[str, str]] = Field(None, description="Additional metadata")
    nickname: Optional[str] = Field(None, description="Human-friendly account name")
    primary_contact: Optional[PrimaryContact] = Field(None, description="Primary contact information")

class AccountUpdateRequest(AirwallexModel):
    """Model for account update request."""
    account_details: Optional[AccountDetails] = Field(None, description="Account details")
    metadata: Optional[Dict[str, str]] = Field(None, description="Additional metadata")
    nickname: Optional[str] = Field(None, description="Human-friendly account name")

# Amendments
class StoreDetails(AirwallexModel):
    """Model for store details."""
    cross_border_transaction_percent: Optional[str] = Field(None, description="Cross-border transaction percentage")
    dispute_percent: Optional[str] = Field(None, description="Dispute percentage")
    employee_size: Optional[int] = Field(None, description="Employee size")
    estimated_transaction_volume: Optional[Dict[str, Any]] = Field(None, description="Estimated transaction volume")
    financial_statements: Optional[List[Dict[str, str]]] = Field(None, description="Financial statements")
    fulfillment_days: Optional[int] = Field(None, description="Fulfillment days")
    industry_code: Optional[str] = Field(None, description="Industry code")
    mcc: Optional[str] = Field(None, description="Merchant Category Code")
    operating_models: Optional[List[str]] = Field(None, description="Operating models")
    payment_distribution: Optional[List[Dict[str, Any]]] = Field(None, description="Payment distribution")

class Amendment(AirwallexModel):
    """Model for an account amendment."""
    resource_name: str = "account/amendments"
    
    id: str = Field(..., description="Amendment ID")
    primary_contact: Optional[PrimaryContact] = Field(None, description="Primary contact information")
    status: str = Field(..., description="Amendment status (PENDING, APPROVED, REJECTED)")
    store_details: Optional[StoreDetails] = Field(None, description="Store details")
    target: str = Field(..., description="Amendment target")

class AmendmentCreateRequest(AirwallexModel):
    """Model for amendment creation request."""
    primary_contact: Optional[PrimaryContact] = Field(None, description="Primary contact information")
    store_details: Optional[StoreDetails] = Field(None, description="Store details")
    target: str = Field(..., description="Amendment target")

# Wallet Info
class WalletInfo(AirwallexModel):
    """Model for wallet information."""
    resource_name: str = "account/wallet_info"
    
    account_name: str = Field(..., description="Account name")
    account_number: str = Field(..., description="Account number")

# Terms and Conditions Agreement
class DeviceData(AirwallexModel):
    """Model for device data."""
    ip_address: Optional[str] = Field(None, description="IP address")
    user_agent: Optional[str] = Field(None, description="User agent")

class TermsAndConditionsRequest(AirwallexModel):
    """Model for terms and conditions agreement request."""
    agreed_at: str = Field(..., description="Agreement timestamp (ISO 8601 format)")
    device_data: Optional[DeviceData] = Field(None, description="Device data")
    service_agreement_type: Optional[str] = Field("FULL", description="Service agreement type (FULL or RECIPIENT)")