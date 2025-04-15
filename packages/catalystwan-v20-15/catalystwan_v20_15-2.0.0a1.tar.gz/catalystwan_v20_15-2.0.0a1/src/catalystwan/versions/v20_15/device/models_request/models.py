# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DeviceCpuCount:
    attribute_field: Optional[str] = _field(default=None, metadata={"alias": "attributeField"})
    enable: Optional[bool] = _field(default=None)


@dataclass
class DeviceInterface:
    day0: Optional[List[str]] = _field(default=None)
    lan: Optional[List[str]] = _field(default=None)
    mgmt: Optional[List[str]] = _field(default=None)
    wan: Optional[List[str]] = _field(default=None)


@dataclass
class DeviceModelsData:
    cpu_count_attribute: Optional[DeviceCpuCount] = _field(
        default=None, metadata={"alias": "cpuCountAttribute"}
    )
    device_class: Optional[str] = _field(default=None, metadata={"alias": "deviceClass"})
    device_type: Optional[str] = _field(default=None, metadata={"alias": "deviceType"})
    display_name: Optional[str] = _field(default=None, metadata={"alias": "displayName"})
    interfaces: Optional[DeviceInterface] = _field(default=None)
    is_cli_supported: Optional[bool] = _field(default=None, metadata={"alias": "isCliSupported"})
    name: Optional[str] = _field(default=None)
    onboard_cert: Optional[bool] = _field(default=None, metadata={"alias": "onboardCert"})
    template_class: Optional[str] = _field(default=None, metadata={"alias": "templateClass"})
    template_supported: Optional[bool] = _field(
        default=None, metadata={"alias": "templateSupported"}
    )


@dataclass
class DeviceResponseHeader:
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})


@dataclass
class DeviceModelsResponse:
    data: Optional[List[DeviceModelsData]] = _field(default=None)
    header: Optional[DeviceResponseHeader] = _field(default=None)
