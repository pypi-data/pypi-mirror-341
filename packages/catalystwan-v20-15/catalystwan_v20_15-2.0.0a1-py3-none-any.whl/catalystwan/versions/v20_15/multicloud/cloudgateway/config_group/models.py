# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Optional


@dataclass
class PostCgwConfigGroupResponseProfiles:
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    description: Optional[str] = _field(default=None)
    id: Optional[str] = _field(default=None)
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    name: Optional[str] = _field(default=None)
    profile_parcel_count: Optional[str] = _field(
        default=None, metadata={"alias": "profileParcelCount"}
    )
    solution: Optional[str] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class PostCgwConfigGroupResponse:
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    description: Optional[str] = _field(default=None)
    devices: Optional[List[str]] = _field(default=None)
    full_config_cli: Optional[bool] = _field(default=None, metadata={"alias": "fullConfigCli"})
    id: Optional[str] = _field(default=None)
    ios_config_cli: Optional[bool] = _field(default=None, metadata={"alias": "iosConfigCli"})
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    name: Optional[str] = _field(default=None)
    number_of_devices: Optional[int] = _field(default=None, metadata={"alias": "numberOfDevices"})
    number_of_devices_up_to_date: Optional[int] = _field(
        default=None, metadata={"alias": "numberOfDevicesUpToDate"}
    )
    origin: Optional[str] = _field(default=None)
    profiles: Optional[List[PostCgwConfigGroupResponseProfiles]] = _field(default=None)
    solution: Optional[str] = _field(default=None)
    source: Optional[str] = _field(default=None)
    state: Optional[str] = _field(default=None)
    topology: Optional[str] = _field(default=None)
    version: Optional[int] = _field(default=None)


@dataclass
class MultiCloudGatewaysConfiggroupBody:
    config_group_name: str = _field(metadata={"alias": "configGroupName"})
    config_group_solution: Optional[str] = _field(
        default=None, metadata={"alias": "configGroupSolution"}
    )
