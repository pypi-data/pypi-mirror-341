# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DevicesDetailsLicenses:
    billing_type: Optional[str] = _field(default=None, metadata={"alias": "billingType"})
    display_name: Optional[str] = _field(default=None, metadata={"alias": "displayName"})
    end_date: Optional[str] = _field(default=None, metadata={"alias": "endDate"})
    license_category: Optional[str] = _field(default=None, metadata={"alias": "licenseCategory"})
    license_type: Optional[str] = _field(default=None, metadata={"alias": "licenseType"})
    no0f_assigned_licenses: Optional[int] = _field(
        default=None, metadata={"alias": "no0fAssignedLicenses"}
    )
    sa_name: Optional[str] = _field(default=None, metadata={"alias": "saName"})
    start_date: Optional[str] = _field(default=None, metadata={"alias": "startDate"})
    subscription_id: Optional[str] = _field(default=None, metadata={"alias": "subscriptionId"})
    tag: Optional[str] = _field(default=None)
    va_name: Optional[str] = _field(default=None, metadata={"alias": "vaName"})


@dataclass
class DevicesDetailsDevices:
    compliance_status: Optional[str] = _field(default=None, metadata={"alias": "complianceStatus"})
    configured_system_ip: Optional[str] = _field(
        default=None, metadata={"alias": "configuredSystemIP"}
    )
    device_model: Optional[str] = _field(default=None, metadata={"alias": "deviceModel"})
    device_tags: Optional[List[str]] = _field(default=None, metadata={"alias": "deviceTags"})
    host_name: Optional[str] = _field(default=None, metadata={"alias": "hostName"})
    hsec_compatible: Optional[str] = _field(default=None, metadata={"alias": "hsecCompatible"})
    hsec_license_status: Optional[str] = _field(
        default=None, metadata={"alias": "hsecLicenseStatus"}
    )
    hsec_status: Optional[str] = _field(default=None, metadata={"alias": "hsecStatus"})
    in_compliant_reason: Optional[str] = _field(
        default=None, metadata={"alias": "inCompliantReason"}
    )
    licenses: Optional[List[DevicesDetailsLicenses]] = _field(default=None)
    no_of_tenants_on_boarded: Optional[int] = _field(
        default=None, metadata={"alias": "noOfTenantsOnBoarded"}
    )
    uuid: Optional[str] = _field(default=None)


@dataclass
class DevicesDetails:
    devices: Optional[List[DevicesDetailsDevices]] = _field(default=None)
