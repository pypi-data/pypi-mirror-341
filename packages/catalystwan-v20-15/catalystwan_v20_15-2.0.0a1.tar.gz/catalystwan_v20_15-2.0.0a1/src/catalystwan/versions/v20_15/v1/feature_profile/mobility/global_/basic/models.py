# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional

GlobalOptionTypeDef = Literal["global"]

UserNameDef = Literal["admin"]

BasicUserNameDef = Literal["admin"]

GlobalBasicUserNameDef = Literal["admin"]


@dataclass
class OneOfUserNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UserNameDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUserPasswordOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Password should contain atleast 1 uppercase letter, 1 lowercase letter, 1 special character, 1 number and have minimum length of 8 characters and maximum length of 32 characters
    value: Any


@dataclass
class User:
    name: OneOfUserNameOptionsDef
    password: OneOfUserPasswordOptionsDef


@dataclass
class BasicData:
    # Create local login account
    user: List[User]


@dataclass
class Payload:
    """
    AON Basic profile parcel schema for POST request
    """

    data: BasicData
    name: str
    # Set the parcel description
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
    # AON Basic profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListMobilityGlobalBasicPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateBasicProfileParcelForMobilityPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GlobalBasicData:
    # Create local login account
    user: List[User]


@dataclass
class CreateBasicProfileParcelForMobilityPostRequest:
    """
    AON Basic profile parcel schema for POST request
    """

    data: GlobalBasicData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class BasicOneOfUserNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: BasicUserNameDef  # pytype: disable=annotation-type-mismatch


@dataclass
class BasicOneOfUserPasswordOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Password should contain atleast 1 uppercase letter, 1 lowercase letter, 1 special character, 1 number and have minimum length of 8 characters and maximum length of 32 characters
    value: Any


@dataclass
class BasicUser:
    name: BasicOneOfUserNameOptionsDef
    password: BasicOneOfUserPasswordOptionsDef


@dataclass
class MobilityGlobalBasicData:
    # Create local login account
    user: List[BasicUser]


@dataclass
class BasicPayload:
    """
    AON Basic profile parcel schema for PUT request
    """

    data: MobilityGlobalBasicData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleMobilityGlobalBasicPayload:
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
    # AON Basic profile parcel schema for PUT request
    payload: Optional[BasicPayload] = _field(default=None)


@dataclass
class EditBasicProfileParcelForMobilityPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GlobalBasicOneOfUserNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalBasicUserNameDef  # pytype: disable=annotation-type-mismatch


@dataclass
class GlobalBasicOneOfUserPasswordOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Password should contain atleast 1 uppercase letter, 1 lowercase letter, 1 special character, 1 number and have minimum length of 8 characters and maximum length of 32 characters
    value: Any


@dataclass
class GlobalBasicUser:
    name: GlobalBasicOneOfUserNameOptionsDef
    password: GlobalBasicOneOfUserPasswordOptionsDef


@dataclass
class FeatureProfileMobilityGlobalBasicData:
    # Create local login account
    user: List[GlobalBasicUser]


@dataclass
class EditBasicProfileParcelForMobilityPutRequest:
    """
    AON Basic profile parcel schema for PUT request
    """

    data: FeatureProfileMobilityGlobalBasicData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
