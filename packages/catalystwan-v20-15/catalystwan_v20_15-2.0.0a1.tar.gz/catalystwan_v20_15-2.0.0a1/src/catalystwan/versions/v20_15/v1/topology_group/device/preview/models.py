# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Optional


@dataclass
class GetTopologyGroupDeviceConfigurationPreviewPostResponse:
    """
    topology Group preview Response schema
    """

    existing_config: str = _field(metadata={"alias": "existingConfig"})
    new_config: str = _field(metadata={"alias": "newConfig"})
    unsupported_parcels: Optional[List[Any]] = _field(
        default=None, metadata={"alias": "unsupportedParcels"}
    )


@dataclass
class GetTopologyGroupDeviceConfigurationPreviewPostRequest:
    """
    Preview POST request Schema
    """

    # Preview vSmart configuration with Topology Group config removed
    deactivate_topology: Optional[bool] = _field(
        default=None, metadata={"alias": "deactivateTopology"}
    )
