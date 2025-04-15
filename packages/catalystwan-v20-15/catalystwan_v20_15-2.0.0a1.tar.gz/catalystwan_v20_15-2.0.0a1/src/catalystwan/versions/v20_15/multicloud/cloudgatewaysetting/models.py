# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class CustomSettings:
    cloud_gateway_solution: Optional[str] = _field(
        default=None, metadata={"alias": "cloudGatewaySolution"}
    )
    cloud_type: Optional[str] = _field(default=None, metadata={"alias": "cloudType"})
    instance_size: Optional[str] = _field(default=None, metadata={"alias": "instanceSize"})
    ip_subnet_pool: Optional[str] = _field(default=None, metadata={"alias": "ipSubnetPool"})
    name: Optional[str] = _field(default=None)
    # Used for GCP Custom settings
    network_tier: Optional[str] = _field(default=None, metadata={"alias": "networkTier"})
    # Used for Azure/Azure GovCloud Custom settings
    sku_scale_unit: Optional[str] = _field(default=None, metadata={"alias": "skuScaleUnit"})
    software_image_id: Optional[str] = _field(default=None, metadata={"alias": "softwareImageId"})
    # Tunnel Count for AWS Connect based and branch connect
    tunnel_count: Optional[str] = _field(default=None, metadata={"alias": "tunnelCount"})
