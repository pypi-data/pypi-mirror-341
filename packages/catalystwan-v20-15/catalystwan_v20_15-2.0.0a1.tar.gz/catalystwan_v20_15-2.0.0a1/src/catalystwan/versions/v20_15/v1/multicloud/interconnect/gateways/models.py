# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

LicenseType = Literal["DIRECT", "PAYG", "PREPAID"]

EdgeGatewaySolution = Literal["MVE", "NE"]

EdgeType = Literal["ATT", "EQUINIX", "MEGAPORT"]


@dataclass
class ProcessResponse:
    # Procees Id of the task
    id: Optional[str] = _field(default=None)


@dataclass
class InterconnectConfigGroupSettings:
    # Config Group Id
    config_group_id: str = _field(metadata={"alias": "configGroupId"})
    # Config Group name
    config_group_name: str = _field(metadata={"alias": "configGroupName"})


@dataclass
class InterconnectMrfSettings:
    # Multi Region Fabric router role
    mrf_router_role: Optional[str] = _field(default=None, metadata={"alias": "mrfRouterRole"})
    # Multi Region Fabric Transport Gateway
    mrf_transport_gateway: Optional[bool] = _field(
        default=None, metadata={"alias": "mrfTransportGateway"}
    )
    # Network Hierarchy Region Id
    nhm_region_id: Optional[int] = _field(default=None, metadata={"alias": "nhmRegionId"})
    # Network Hierarchy Region name
    nhm_region_name: Optional[str] = _field(default=None, metadata={"alias": "nhmRegionName"})


@dataclass
class InterconnectGatewaySettings:
    instance_size: str = _field(metadata={"alias": "instanceSize"})
    software_image_id: str = _field(metadata={"alias": "softwareImageId"})
    edge_gateway_solution: Optional[EdgeGatewaySolution] = _field(
        default=None, metadata={"alias": "edgeGatewaySolution"}
    )
    edge_type: Optional[EdgeType] = _field(default=None, metadata={"alias": "edgeType"})
    # Assigned name of the Interconnect Gateway Custom Settings
    egw_custom_setting_name: Optional[str] = _field(
        default=None, metadata={"alias": "egwCustomSettingName"}
    )
    # Ip subnet pool assigned to the gateway
    ip_subnet_pool: Optional[str] = _field(default=None, metadata={"alias": "ipSubnetPool"})


@dataclass
class InterconnectGatewayExtended:
    device_uuid: str = _field(metadata={"alias": "deviceUuid"})
    edge_account_id: str = _field(metadata={"alias": "edgeAccountId"})
    edge_billing_account_id: str = _field(metadata={"alias": "edgeBillingAccountId"})
    edge_gateway_name: str = _field(metadata={"alias": "edgeGatewayName"})
    edge_type: str = _field(metadata={"alias": "edgeType"})
    ip_transit: str = _field(metadata={"alias": "ipTransit"})
    license_type: LicenseType = _field(
        metadata={"alias": "licenseType"}
    )  # pytype: disable=annotation-type-mismatch
    region: str
    region_id: str = _field(metadata={"alias": "regionId"})
    site_name: str = _field(metadata={"alias": "siteName"})
    config_group_settings: Optional[InterconnectConfigGroupSettings] = _field(
        default=None, metadata={"alias": "configGroupSettings"}
    )
    description: Optional[str] = _field(default=None)
    # BGP ASN assigned to Interconnect Gateway
    egw_bgp_asn: Optional[str] = _field(default=None, metadata={"alias": "egwBgpAsn"})
    ip_transit_id: Optional[str] = _field(default=None, metadata={"alias": "ipTransitId"})
    ip_transit_sku_id: Optional[str] = _field(default=None, metadata={"alias": "ipTransitSkuId"})
    # Custom Settings enabled for Interconnect Gateway
    is_custom_setting: Optional[bool] = _field(default=None, metadata={"alias": "isCustomSetting"})
    # License Sku Id of Interconnect Gateway
    license_sku_id: Optional[str] = _field(default=None, metadata={"alias": "licenseSkuId"})
    # Ip pool allocated to Interconnect Gateway for Loopback Interfaces
    loopback_cidr: Optional[str] = _field(default=None, metadata={"alias": "loopbackCidr"})
    mrf_settings: Optional[InterconnectMrfSettings] = _field(
        default=None, metadata={"alias": "mrfSettings"}
    )
    resource_state: Optional[str] = _field(default=None, metadata={"alias": "resourceState"})
    resource_state_message: Optional[str] = _field(
        default=None, metadata={"alias": "resourceStateMessage"}
    )
    resource_state_update_ts: Optional[str] = _field(
        default=None, metadata={"alias": "resourceStateUpdateTs"}
    )
    service_chain_attachments: Optional[str] = _field(
        default=None, metadata={"alias": "serviceChainAttachments"}
    )
    settings: Optional[InterconnectGatewaySettings] = _field(default=None)
