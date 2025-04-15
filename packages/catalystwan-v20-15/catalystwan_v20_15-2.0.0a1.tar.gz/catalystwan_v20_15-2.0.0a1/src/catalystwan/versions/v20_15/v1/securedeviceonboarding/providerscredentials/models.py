# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class AccountData:
    # Access Point Name
    apn: str
    # Authentication method.
    auth_method: str = _field(metadata={"alias": "authMethod"})
    # Name of the communication plan associated with default provider.
    comm_plan: str = _field(metadata={"alias": "commPlan"})
    # Data packet protocol version
    pdn_type: str = _field(metadata={"alias": "pdnType"})
    # Name of the rate plan associated with default provider.
    rate_plan: str = _field(metadata={"alias": "ratePlan"})
    # Password of the user.
    password: Optional[str] = _field(default=None)
    # User name.
    user: Optional[str] = _field(default=None)


@dataclass
class ProviderAccountDetails:
    #  ID  of the account associated with user using provider service.
    account_id: str = _field(metadata={"alias": "accountId"})
    # Name of the user registered to  the service.
    account_user_name: str = _field(metadata={"alias": "accountUserName"})
    # API key for the provider service.
    api_key: str = _field(metadata={"alias": "apiKey"})
    # Name of the service provider.
    carrier_name: str = _field(metadata={"alias": "carrierName"})
    # Boolean value which indicates whether the provider is the default provider .
    is_default: bool = _field(metadata={"alias": "isDefault"})
    # Boolean value which indicates if the account user accepts account provider's terms and conditions if they exist.
    accept_terms_and_conditions: Optional[bool] = _field(
        default=None, metadata={"alias": "acceptTermsAndConditions"}
    )
    account_data: Optional[AccountData] = _field(default=None, metadata={"alias": "accountData"})
