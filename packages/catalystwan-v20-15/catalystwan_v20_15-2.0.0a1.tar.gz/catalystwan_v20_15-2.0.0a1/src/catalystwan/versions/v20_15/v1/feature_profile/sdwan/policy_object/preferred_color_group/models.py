# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

Value = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

EntriesPathPreferenceDef = Literal["all-paths", "direct-path", "multi-hop-path"]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse:
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})


@dataclass
class OneOfEntriesColorPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Value]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEntriesPathPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesPathPreferenceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PrimaryPreference1:
    color_preference: OneOfEntriesColorPreferenceOptionsDef = _field(
        metadata={"alias": "colorPreference"}
    )
    path_preference: Optional[OneOfEntriesPathPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "pathPreference"}
    )


@dataclass
class PrimaryPreference2:
    path_preference: OneOfEntriesPathPreferenceOptionsDef = _field(
        metadata={"alias": "pathPreference"}
    )
    color_preference: Optional[OneOfEntriesColorPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "colorPreference"}
    )


@dataclass
class SecondaryPreference:
    """
    Object with an color and path preference
    """

    color_preference: Optional[OneOfEntriesColorPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "colorPreference"}
    )
    path_preference: Optional[OneOfEntriesPathPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "pathPreference"}
    )


@dataclass
class TertiaryPreference:
    """
    Object with an color and path preference
    """

    color_preference: Optional[OneOfEntriesColorPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "colorPreference"}
    )
    path_preference: Optional[OneOfEntriesPathPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "pathPreference"}
    )


@dataclass
class Entries:
    # Object with an color and path preference
    primary_preference: Union[PrimaryPreference1, PrimaryPreference2] = _field(
        metadata={"alias": "primaryPreference"}
    )
    # Object with an color and path preference
    secondary_preference: Optional[SecondaryPreference] = _field(
        default=None, metadata={"alias": "secondaryPreference"}
    )
    # Object with an color and path preference
    tertiary_preference: Optional[TertiaryPreference] = _field(
        default=None, metadata={"alias": "tertiaryPreference"}
    )


@dataclass
class Data:
    # Preferred Color Group List
    entries: Optional[List[Entries]] = _field(default=None)


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest:
    """
    preferred-color-group profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class Payload:
    """
    preferred-color-group profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetDataPrefixProfileParcelForPolicyObjectGetResponse:
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # preferred-color-group profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)
