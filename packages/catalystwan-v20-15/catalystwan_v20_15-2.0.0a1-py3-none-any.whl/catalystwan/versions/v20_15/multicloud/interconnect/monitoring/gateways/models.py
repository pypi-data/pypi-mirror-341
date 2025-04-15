# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class InterconnectGatewayMonitoring:
    device_uuid: str = _field(metadata={"alias": "deviceUuid"})
    edge_account_id: str = _field(metadata={"alias": "edgeAccountId"})
    edge_gateway_name: str = _field(metadata={"alias": "edgeGatewayName"})
    edge_type: str = _field(metadata={"alias": "edgeType"})
    region: str
    site_name: str = _field(metadata={"alias": "siteName"})
    description: Optional[str] = _field(default=None)
    edge_account_name: Optional[str] = _field(default=None, metadata={"alias": "edgeAccountName"})
    edge_gateway_id: Optional[str] = _field(default=None, metadata={"alias": "edgeGatewayId"})
    # Custom Settings enabled for Interconnect Gateway
    is_custom_setting: Optional[bool] = _field(default=None, metadata={"alias": "isCustomSetting"})
    resource_state: Optional[str] = _field(default=None, metadata={"alias": "resourceState"})
    status: Optional[str] = _field(default=None)
