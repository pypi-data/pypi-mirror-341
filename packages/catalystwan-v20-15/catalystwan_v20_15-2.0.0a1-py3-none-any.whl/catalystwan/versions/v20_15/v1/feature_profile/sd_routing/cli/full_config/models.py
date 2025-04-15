# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Optional


@dataclass
class FullConfigData:
    fullconfig: str


@dataclass
class Payload:
    """
    Full Config profile parcel schema for POST request
    """

    data: FullConfigData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data:
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
    # Full Config profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingCliFullConfigPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingCliConfigGroupFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CliFullConfigData:
    fullconfig: str


@dataclass
class CreateSdroutingCliConfigGroupFeaturePostRequest:
    """
    Full Config profile parcel schema for POST request
    """

    data: CliFullConfigData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingCliFullConfigData:
    fullconfig: str


@dataclass
class FullConfigPayload:
    """
    Full Config profile parcel schema for PUT request
    """

    data: SdRoutingCliFullConfigData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingCliFullConfigPayload:
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
    # Full Config profile parcel schema for PUT request
    payload: Optional[FullConfigPayload] = _field(default=None)


@dataclass
class EditSdroutingCliConfigGroupFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class FeatureProfileSdRoutingCliFullConfigData:
    fullconfig: str


@dataclass
class EditSdroutingCliConfigGroupFeaturePutRequest:
    """
    Full Config profile parcel schema for PUT request
    """

    data: FeatureProfileSdRoutingCliFullConfigData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
