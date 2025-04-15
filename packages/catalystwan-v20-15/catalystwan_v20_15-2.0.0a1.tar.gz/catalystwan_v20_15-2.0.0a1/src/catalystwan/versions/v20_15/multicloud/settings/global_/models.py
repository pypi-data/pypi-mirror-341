# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

CloudTypeParam = Literal["AWS", "AWS_GOVCLOUD", "AZURE", "AZURE_GOVCLOUD", "GCP"]


@dataclass
class MulticloudSystemSettings:
    enable_monitoring: Optional[bool] = _field(default=None, metadata={"alias": "enableMonitoring"})
    # Enable or disable Configuration Group for Gateways
    use_configuration_group: Optional[str] = _field(
        default=None, metadata={"alias": "useConfigurationGroup"}
    )


@dataclass
class GlobalSettings:
    # Used for GCP, AWS and AWS GovCloud Global settings
    cgw_bgp_asn_offset: str = _field(metadata={"alias": "cgwBgpAsnOffset"})
    cloud_gateway_solution: str = _field(metadata={"alias": "cloudGatewaySolution"})
    cloud_type: str = _field(metadata={"alias": "cloudType"})
    # Used for GCP, AWS and AWS GovCloud Global settings
    instance_size: str = _field(metadata={"alias": "instanceSize"})
    ip_subnet_pool: str = _field(metadata={"alias": "ipSubnetPool"})
    # Used for GCP, Azure and Azure GovCloud Global settings
    org_bgp_asn: str = _field(metadata={"alias": "orgBgpAsn"})
    # Used for Azure/Azure GovCloud Global settings
    sku_scale_unit: str = _field(metadata={"alias": "skuScaleUnit"})
    software_image_id: str = _field(metadata={"alias": "softwareImageId"})
    # Used for AWS/AWS GovCloud Global settings
    account_id: Optional[str] = _field(default=None, metadata={"alias": "accountId"})
    enable_auto_correct: Optional[str] = _field(
        default=None, metadata={"alias": "enableAutoCorrect"}
    )
    # Used for Azure Global settings
    enable_def_route_advertize: Optional[str] = _field(
        default=None, metadata={"alias": "enableDefRouteAdvertize"}
    )
    # Used for Azure Global settings
    enable_monitoring: Optional[str] = _field(default=None, metadata={"alias": "enableMonitoring"})
    enable_periodic_audit: Optional[str] = _field(
        default=None, metadata={"alias": "enablePeriodicAudit"}
    )
    intra_tag_comm: Optional[str] = _field(default=None, metadata={"alias": "intraTagComm"})
    # Used for GCP, AWS and AWS GovCloud Global settings
    map_tvpc: Optional[str] = _field(default=None, metadata={"alias": "mapTvpc"})
    multicloud_system_settings: Optional[MulticloudSystemSettings] = _field(
        default=None, metadata={"alias": "multicloudSystemSettings"}
    )
    name: Optional[str] = _field(default=None)
    # Used for GCP Global settings
    network_tier: Optional[str] = _field(default=None, metadata={"alias": "networkTier"})
    # Used for GCP Global settings
    policy_management: Optional[str] = _field(default=None, metadata={"alias": "policyManagement"})
    # Used for AWS/AWS GovCloud Global settings
    program_default_route: Optional[str] = _field(
        default=None, metadata={"alias": "programDefaultRoute"}
    )
    # Used for AWS/AWS GovCloud Global settings
    region: Optional[str] = _field(default=None)
    # Used for GCP Global settings
    service_dir_poll_timer: Optional[str] = _field(
        default=None, metadata={"alias": "serviceDirPollTimer"}
    )
    # Used for AWS/AWS GovCloud Global settings
    tunnel_count: Optional[str] = _field(default=None, metadata={"alias": "tunnelCount"})
    # Used for GCP, AWS and AWS GovCloud Global settings
    tunnel_type: Optional[str] = _field(default=None, metadata={"alias": "tunnelType"})


@dataclass
class Taskid:
    """
    Task id for polling status
    """

    id: Optional[str] = _field(default=None)
