# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

TrackGroupBooleanDef = Literal["and", "or"]

DefaultOptionTypeDef = Literal["default"]

DefaultTrackGroupBooleanDef = Literal["or"]


@dataclass
class OneOfTrackerGroupNameOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerGroupNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RefId:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ParcelReferenceDef:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class TrackGroupRefDef:
    tracker_ref: ParcelReferenceDef = _field(metadata={"alias": "trackerRef"})


@dataclass
class OneOfTrackerBooleanOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerBooleanOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TrackGroupBooleanDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTrackerBooleanOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultTrackGroupBooleanDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Data:
    combine_boolean: Union[
        OneOfTrackerBooleanOptionsDef1,
        OneOfTrackerBooleanOptionsDef2,
        OneOfTrackerBooleanOptionsDef3,
    ] = _field(metadata={"alias": "combineBoolean"})
    tracker_group_name: Union[
        OneOfTrackerGroupNameOptionsDef1, OneOfTrackerGroupNameOptionsDef2
    ] = _field(metadata={"alias": "trackerGroupName"})
    # trackers ref list
    tracker_refs: List[TrackGroupRefDef] = _field(metadata={"alias": "trackerRefs"})


@dataclass
class Payload:
    """
    IPv6 TrackerGroup profile parcel schema for common request
    """

    data: Data
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetWanVpnInterfaceCellularAssociatedIpv6TrackerGroupParcelsForTransportGetResponse:
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # IPv6 TrackerGroup profile parcel schema for common request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetSingleSdwanTransportWanVpnInterfaceCellularIpv6TrackergroupPayload:
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # IPv6 TrackerGroup profile parcel schema for common request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EditWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPutRequest:
    """
    Profile Parcel POST Request schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPostRequest:
    """
    Profile Parcel POST Request schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)
