# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class ApiKey:
    """
    API secret information
    """

    vip_object_type: Optional[str] = _field(default=None, metadata={"alias": "vipObjectType"})
    vip_type: Optional[str] = _field(default=None, metadata={"alias": "vipType"})
    vip_value: Optional[str] = _field(default=None, metadata={"alias": "vipValue"})
    vip_variable_name: Optional[str] = _field(default=None, metadata={"alias": "vipVariableName"})


@dataclass
class ApiSecret:
    """
    API key information
    """

    vip_needs_encryption: Optional[bool] = _field(
        default=None, metadata={"alias": "vipNeedsEncryption"}
    )
    vip_object_type: Optional[str] = _field(default=None, metadata={"alias": "vipObjectType"})
    vip_type: Optional[str] = _field(default=None, metadata={"alias": "vipType"})
    vip_value: Optional[str] = _field(default=None, metadata={"alias": "vipValue"})
    vip_variable_name: Optional[str] = _field(default=None, metadata={"alias": "vipVariableName"})


@dataclass
class OrgId:
    """
    Org ID
    """

    vip_object_type: Optional[str] = _field(default=None, metadata={"alias": "vipObjectType"})
    vip_type: Optional[str] = _field(default=None, metadata={"alias": "vipType"})
    vip_value: Optional[str] = _field(default=None, metadata={"alias": "vipValue"})
    vip_variable_name: Optional[str] = _field(default=None, metadata={"alias": "vipVariableName"})


@dataclass
class Umbrella:
    """
    Umbrella object
    """

    # API secret information
    api_key: Optional[ApiKey] = _field(default=None, metadata={"alias": "api-key"})
    # API secret information
    api_key_v2: Optional[ApiKey] = _field(default=None, metadata={"alias": "api-key-v2"})
    # API key information
    api_secret: Optional[ApiSecret] = _field(default=None, metadata={"alias": "api-secret"})
    # API key information
    api_secret_v2: Optional[ApiSecret] = _field(default=None, metadata={"alias": "api-secret-v2"})
    # Org ID
    org_id: Optional[OrgId] = _field(default=None, metadata={"alias": "org-id"})


@dataclass
class FeatureTemplateType:
    """
    Response from metaDataType API
    """

    # Umbrella object
    umbrella: Optional[Umbrella] = _field(default=None)
