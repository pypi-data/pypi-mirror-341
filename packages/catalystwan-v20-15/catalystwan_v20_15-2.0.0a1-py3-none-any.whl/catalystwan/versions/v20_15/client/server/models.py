# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class ClientServerResponseData:
    capabilities: Optional[List[str]] = _field(default=None)
    cloudx: Optional[str] = _field(default=None)
    csrf_token: Optional[str] = _field(default=None, metadata={"alias": "CSRFToken"})
    description: Optional[str] = _field(default=None)
    disable_full_config_push: Optional[bool] = _field(
        default=None, metadata={"alias": "disableFullConfigPush"}
    )
    enable_server_events: Optional[bool] = _field(
        default=None, metadata={"alias": "enableServerEvents"}
    )
    external_user: Optional[bool] = _field(default=None, metadata={"alias": "externalUser"})
    general_template: Optional[bool] = _field(default=None, metadata={"alias": "generalTemplate"})
    is_rbac_vpn_user: Optional[bool] = _field(default=None, metadata={"alias": "isRbacVpnUser"})
    is_saml_user: Optional[bool] = _field(default=None, metadata={"alias": "isSamlUser"})
    is_ui_allowed: Optional[bool] = _field(default=None, metadata={"alias": "isUiAllowed"})
    locale: Optional[str] = _field(default=None)
    platform_version: Optional[str] = _field(default=None, metadata={"alias": "platformVersion"})
    reverseproxy: Optional[str] = _field(default=None)
    roles: Optional[List[str]] = _field(default=None)
    server: Optional[str] = _field(default=None)
    tenancy_mode: Optional[str] = _field(default=None, metadata={"alias": "tenancyMode"})
    tenant_id: Optional[str] = _field(default=None, metadata={"alias": "tenantId"})
    user: Optional[str] = _field(default=None)
    user_mode: Optional[str] = _field(default=None, metadata={"alias": "userMode"})
    view_mode: Optional[str] = _field(default=None, metadata={"alias": "viewMode"})
    vmanage_mode: Optional[str] = _field(default=None, metadata={"alias": "vmanageMode"})
    vpns: Optional[List[str]] = _field(default=None)
    vsession_id: Optional[str] = _field(default=None, metadata={"alias": "VsessionId"})


@dataclass
class ClientServerResponseHeader:
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})


@dataclass
class ClientServerInfoResponse:
    data: Optional[ClientServerResponseData] = _field(default=None)
    header: Optional[ClientServerResponseHeader] = _field(default=None)
