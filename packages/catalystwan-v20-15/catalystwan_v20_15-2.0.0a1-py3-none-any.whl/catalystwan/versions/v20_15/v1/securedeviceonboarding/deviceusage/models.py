# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class DeviceUsageDetails:
    # Name of the service provider.
    carrier_name: str = _field(metadata={"alias": "carrierName"})
    # Name of the communication plan.
    communication_plan: str = _field(metadata={"alias": "communicationPlan"})
    # Controller Id
    controller_id: str = _field(metadata={"alias": "controllerId"})
    # Current Data Usage.
    current_data_usage: str = _field(metadata={"alias": "currentDataUsage"})
    # Identifier of the eSIM device.
    iccid: str
    # Name of the rate plan.
    rate_plan: str = _field(metadata={"alias": "ratePlan"})
    # Rate plan type.
    rate_plan_type: str = _field(metadata={"alias": "ratePlanType"})
    # Slot Id
    slot_id: int = _field(metadata={"alias": "slotId"})
    # Details of any error encountered while retrieving device data usage
    error_details: Optional[str] = _field(default=None, metadata={"alias": "errorDetails"})
    # Bootstrap eSim Status
    esim_status: Optional[str] = _field(default=None, metadata={"alias": "esimStatus"})
    # Boolean flag that indicated if ICCID is on bootstrap account
    is_bootstrap: Optional[bool] = _field(default=None, metadata={"alias": "isBootstrap"})
    # Total data used by other eSIM devices.
    other_esims_data_usage: Optional[str] = _field(
        default=None, metadata={"alias": "otherEsimsDataUsage"}
    )
    # Rate plan usage limit.
    rate_plan_data_usage_limit: Optional[str] = _field(
        default=None, metadata={"alias": "ratePlanDataUsageLimit"}
    )
    # Total data usage
    total_data_usage: Optional[str] = _field(default=None, metadata={"alias": "totalDataUsage"})
    # Total value of current data usage and data used by other eSIM devices
    usage_threshold_warning: Optional[List[str]] = _field(
        default=None, metadata={"alias": "usageThresholdWarning"}
    )
