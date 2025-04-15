# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

EdgeGatewaySolution = Literal["MVE", "NE"]

EdgeType = Literal["ATT", "EQUINIX", "MEGAPORT"]


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
