# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class InlineResponse20013TopologyCriteria:
    # Name of attribute type
    attribute: Optional[str] = _field(default=None)
    # Value of attribute
    value: Optional[str] = _field(default=None)


@dataclass
class InlineResponse20013TopologyUnsupportedFeatures:
    # Config-Group Parcel Id
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    # Config-Group Parcel Type
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})


@dataclass
class InlineResponse20013TopologyDevices:
    criteria: Optional[InlineResponse20013TopologyCriteria] = _field(default=None)
    unsupported_features: Optional[InlineResponse20013TopologyUnsupportedFeatures] = _field(
        default=None, metadata={"alias": "unsupportedFeatures"}
    )


@dataclass
class InlineResponse20013Topology:
    devices: Optional[List[InlineResponse20013TopologyDevices]] = _field(default=None)


@dataclass
class InlineResponse20013:
    topology: Optional[InlineResponse20013Topology] = _field(default=None)
