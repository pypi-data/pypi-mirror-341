# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Dict, List, Literal, Optional

Solution = Literal[
    "cellulargateway", "common", "mobility", "nfvirtual", "sd-routing", "sdwan", "service-insertion"
]

ProfileType = Literal["global"]

PolicyGroupSolution = Literal["sd-routing", "sdwan"]

V1PolicyGroupSolution = Literal["sd-routing", "sdwan"]


@dataclass
class FeatureProfile:
    """
    List of devices UUIDs associated with this group
    """

    # Name of the feature Profile. Must be unique.
    name: str
    # Solution of the feature Profile.
    solution: str
    # Type of the feature Profile.
    type_: str = _field(metadata={"alias": "type"})
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the feature Profile.
    description: Optional[str] = _field(default=None)
    # System generated unique identifier of the feature profile in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    # Number of Parcels attached with Feature Profile
    profile_parcel_count: Optional[int] = _field(
        default=None, metadata={"alias": "profileParcelCount"}
    )


@dataclass
class PolicyGroup:
    # Name of the  Group. Must be unique.
    name: str
    # Specify one of the device platform solution
    solution: Solution  # pytype: disable=annotation-type-mismatch
    #  Group Deployment state
    state: str
    #  Group Version Flag
    version: int
    copy_info: Optional[str] = _field(default=None, metadata={"alias": "copyInfo"})
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the  Group.
    description: Optional[str] = _field(default=None)
    devices: Optional[List[str]] = _field(default=None)
    # System generated unique identifier of the  Group in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    number_of_devices: Optional[int] = _field(default=None, metadata={"alias": "numberOfDevices"})
    number_of_devices_up_to_date: Optional[int] = _field(
        default=None, metadata={"alias": "numberOfDevicesUpToDate"}
    )
    origin: Optional[str] = _field(default=None)
    origin_info: Optional[Dict[str, str]] = _field(default=None, metadata={"alias": "originInfo"})
    # List of devices UUIDs associated with this group
    profiles: Optional[List[FeatureProfile]] = _field(default=None)
    # Source of group
    source: Optional[str] = _field(default=None)


@dataclass
class ProfileObjDef:
    id: str
    profile_type: ProfileType = _field(
        metadata={"alias": "profileType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class CreatePolicyGroupPostResponse:
    """
    Policy Group POST Response schema
    """

    id: str
    # (Optional - only applicable for AON) List of profile ids that belongs to the policy group
    profiles: Optional[List[ProfileObjDef]] = _field(default=None)


@dataclass
class ProfileIdObjDef:
    id: str


@dataclass
class FromPolicyGroupDef:
    copy: str


@dataclass
class CreatePolicyGroupPostRequest:
    """
    Policy Group POST Request schema
    """

    description: str
    name: str
    solution: PolicyGroupSolution  # pytype: disable=annotation-type-mismatch
    from_policy_group: Optional[FromPolicyGroupDef] = _field(
        default=None, metadata={"alias": "fromPolicyGroup"}
    )
    # list of profile ids that belongs to the policy group
    profiles: Optional[List[ProfileIdObjDef]] = _field(default=None)


@dataclass
class PolicyGroupProfileObjDef:
    id: str
    profile_type: ProfileType = _field(
        metadata={"alias": "profileType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class EditPolicyGroupPutResponse:
    """
    Policy Group PUT Response schema
    """

    id: str
    # (Optional - only applicable for AON) List of profile ids that belongs to the Policy group
    profiles: Optional[List[PolicyGroupProfileObjDef]] = _field(default=None)


@dataclass
class PolicyGroupProfileIdObjDef:
    id: str


@dataclass
class EditPolicyGroupPutRequest:
    """
    Policy Group PUT Request schema
    """

    description: str
    name: str
    solution: V1PolicyGroupSolution  # pytype: disable=annotation-type-mismatch
    # list of profile ids that belongs to the policy group
    profiles: Optional[List[PolicyGroupProfileIdObjDef]] = _field(default=None)
