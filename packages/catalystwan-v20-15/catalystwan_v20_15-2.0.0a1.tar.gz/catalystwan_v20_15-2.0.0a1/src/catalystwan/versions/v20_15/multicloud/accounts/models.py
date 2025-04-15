# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class GetAccounts:
    account_id: Optional[str] = _field(default=None, metadata={"alias": "accountId"})
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    client_email: Optional[str] = _field(default=None, metadata={"alias": "clientEmail"})
    cloud_gateway_enabled: Optional[bool] = _field(
        default=None, metadata={"alias": "cloudGatewayEnabled"}
    )
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    cred_type: Optional[str] = _field(default=None, metadata={"alias": "credType"})
    description: Optional[str] = _field(default=None)
    gcp_billing_id: Optional[str] = _field(default=None, metadata={"alias": "gcpBillingId"})
    private_key_id: Optional[str] = _field(default=None, metadata={"alias": "privateKeyId"})
    region_list: Optional[str] = _field(default=None, metadata={"alias": "regionList"})
    service_discovery_enabled: Optional[bool] = _field(
        default=None, metadata={"alias": "serviceDiscoveryEnabled"}
    )


@dataclass
class PostAccountsResponse:
    account_id: Optional[str] = _field(default=None, metadata={"alias": "accountId"})
    account_name: Optional[str] = _field(default=None, metadata={"alias": "accountName"})
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    region_list: Optional[str] = _field(default=None, metadata={"alias": "regionList"})


@dataclass
class AwsIamCredentials:
    external_id: str = _field(metadata={"alias": "externalId"})
    role_arn: str = _field(metadata={"alias": "roleArn"})


@dataclass
class AwsKeyCredentials:
    api_key: str = _field(metadata={"alias": "apiKey"})
    secret_key: str = _field(metadata={"alias": "secretKey"})


@dataclass
class AzureCredentials:
    client_id: str = _field(metadata={"alias": "clientId"})
    cloud_tenant_id: str = _field(metadata={"alias": "cloudTenantId"})
    secret_key: str = _field(metadata={"alias": "secretKey"})
    subscription_id: str = _field(metadata={"alias": "subscriptionId"})


@dataclass
class GcpCredentials:
    auth_provider_x509_cert_url: str
    auth_uri: str
    client_email: str
    client_id: str
    client_x509_cert_url: str
    private_key: str
    private_key_id: str
    project_id: str
    token_uri: str
    type_: str = _field(metadata={"alias": "type"})


@dataclass
class PostAccounts:
    account_name: str = _field(metadata={"alias": "accountName"})
    azure_credentials: AzureCredentials = _field(metadata={"alias": "azureCredentials"})
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    gcp_credentials: GcpCredentials = _field(metadata={"alias": "gcpCredentials"})
    account_id: Optional[str] = _field(default=None, metadata={"alias": "accountId"})
    aws_iam_credentials: Optional[AwsIamCredentials] = _field(
        default=None, metadata={"alias": "awsIamCredentials"}
    )
    aws_key_credentials: Optional[AwsKeyCredentials] = _field(
        default=None, metadata={"alias": "awsKeyCredentials"}
    )
    cloud_gateway_enabled: Optional[str] = _field(
        default=None, metadata={"alias": "cloudGatewayEnabled"}
    )
    description: Optional[str] = _field(default=None)
    gcp_billing_id: Optional[str] = _field(default=None, metadata={"alias": "gcpBillingId"})
    kubernetes_discovery_enabled: Optional[str] = _field(
        default=None, metadata={"alias": "kubernetesDiscoveryEnabled"}
    )
    service_discovery_enabled: Optional[str] = _field(
        default=None, metadata={"alias": "serviceDiscoveryEnabled"}
    )


@dataclass
class PutAccounts:
    account_id: str = _field(metadata={"alias": "accountId"})
    account_name: str = _field(metadata={"alias": "accountName"})
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    cloud_gateway_enabled: Optional[str] = _field(
        default=None, metadata={"alias": "cloudGatewayEnabled"}
    )
    description: Optional[str] = _field(default=None)
    gcp_billing_id: Optional[str] = _field(default=None, metadata={"alias": "gcpBillingId"})
    kubernetes_discovery_enabled: Optional[str] = _field(
        default=None, metadata={"alias": "kubernetesDiscoveryEnabled"}
    )
    service_discovery_enabled: Optional[str] = _field(
        default=None, metadata={"alias": "serviceDiscoveryEnabled"}
    )
