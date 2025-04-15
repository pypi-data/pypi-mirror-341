# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

CloudTypeParam = Literal["AWS", "AWS_GOVCLOUD", "AZURE", "AZURE_GOVCLOUD", "GCP"]


@dataclass
class DeviceInfoExtendedResponse:
    cloud_gateway_name: Optional[str] = _field(default=None, metadata={"alias": "cloudGatewayName"})
    config_status_message: Optional[str] = _field(
        default=None, metadata={"alias": "configStatusMessage"}
    )
    configured_system_ip: Optional[str] = _field(
        default=None, metadata={"alias": "configuredSystemIP"}
    )
    device_model: Optional[str] = _field(default=None, metadata={"alias": "device-model"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "device-type"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "host-name"})
    last_updated: Optional[int] = _field(default=None, metadata={"alias": "lastUpdated"})
    local_system_ip: Optional[str] = _field(default=None, metadata={"alias": "local-system-ip"})
    reachability: Optional[str] = _field(default=None)
    site_id: Optional[str] = _field(default=None, metadata={"alias": "site-id"})
    status: Optional[str] = _field(default=None)
    system_ip: Optional[str] = _field(default=None, metadata={"alias": "system-ip"})
    uptime_date: Optional[int] = _field(default=None, metadata={"alias": "uptime-date"})
    uuid: Optional[str] = _field(default=None)
    version: Optional[str] = _field(default=None)
