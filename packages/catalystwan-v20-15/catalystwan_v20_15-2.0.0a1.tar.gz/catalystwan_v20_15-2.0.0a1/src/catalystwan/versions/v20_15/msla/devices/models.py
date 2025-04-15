# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class GetSingleMslaDevicePayload:
    configured_system_ip: Optional[str] = _field(
        default=None, metadata={"alias": "configuredSystemIP"}
    )
    device_model: Optional[str] = _field(default=None, metadata={"alias": "deviceModel"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "hostName"})
    hsec_compatible: Optional[str] = _field(default=None, metadata={"alias": "hsecCompatible"})
    hsec_status: Optional[str] = _field(default=None, metadata={"alias": "hsecStatus"})
    license_status: Optional[str] = _field(default=None, metadata={"alias": "License_status"})
    license_type: Optional[str] = _field(default=None, metadata={"alias": "licenseType"})
    licenses: Optional[List[str]] = _field(default=None)
    msla: Optional[str] = _field(default=None)
    sa_account: Optional[str] = _field(default=None, metadata={"alias": "saAccount"})
    sa_namme: Optional[str] = _field(default=None, metadata={"alias": "saNamme"})
    subscription_id: Optional[List[str]] = _field(default=None)
    tag: Optional[List[str]] = _field(default=None)
    template_name: Optional[str] = _field(default=None, metadata={"alias": "templateName"})
    uuid: Optional[str] = _field(default=None, metadata={"alias": "UUID"})
    va_account: Optional[List[str]] = _field(default=None, metadata={"alias": "vaAccount"})
    va_name: Optional[str] = _field(default=None, metadata={"alias": "vaName"})


@dataclass
class GetMslaDevicesPayload:
    data: Optional[List[GetSingleMslaDevicePayload]] = _field(default=None)


@dataclass
class ReleaseLicensesRequest:
    # List of device UUIDs
    devices: Optional[List[str]] = _field(default=None)


@dataclass
class GetDeviceLicensesInner:
    billing_model: Optional[str] = _field(default=None)
    billing_type: Optional[str] = _field(default=None)
    display_name: Optional[str] = _field(default=None)
    end_date: Optional[str] = _field(default=None)
    in_use: Optional[str] = _field(default=None, metadata={"alias": "inUse"})
    license_category: Optional[str] = _field(default=None)
    license_type: Optional[str] = _field(default=None)
    saname: Optional[str] = _field(default=None)
    start_date: Optional[str] = _field(default=None)
    subscription_id: Optional[str] = _field(default=None)
    tag: Optional[str] = _field(default=None)
    vaname: Optional[str] = _field(default=None)
