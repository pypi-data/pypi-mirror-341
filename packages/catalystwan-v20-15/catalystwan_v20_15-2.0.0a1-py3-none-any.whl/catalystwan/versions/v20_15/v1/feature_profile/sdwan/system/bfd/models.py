# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

ColorDef = Literal[
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

BfdColorDef = Literal[
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

SystemBfdColorDef = Literal[
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


@dataclass
class OneOfMultiplierOptions1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMultiplierOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMultiplierOptions3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPollIntervalOptions1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPollIntervalOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPollIntervalOptions3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDefaultDscpOptions1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDefaultDscpOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDefaultDscpOptions3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfColorOptions1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfColorOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfHelloIntervalOptions1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHelloIntervalOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHelloIntervalOptions3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfColorMultiplierOptions1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfColorMultiplierOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfColorMultiplierOptions3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPmtuDiscoveryOptions1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPmtuDiscoveryOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPmtuDiscoveryOptions3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfColorDscpOptions1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfColorDscpOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfColorDscpOptions3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Colors:
    color: Union[OneOfColorOptions1, OneOfColorOptions2]
    dscp: Union[OneOfColorDscpOptions1, OneOfColorDscpOptions2, OneOfColorDscpOptions3]
    hello_interval: Union[
        OneOfHelloIntervalOptions1, OneOfHelloIntervalOptions2, OneOfHelloIntervalOptions3
    ] = _field(metadata={"alias": "helloInterval"})
    multiplier: Union[
        OneOfColorMultiplierOptions1, OneOfColorMultiplierOptions2, OneOfColorMultiplierOptions3
    ]
    pmtu_discovery: Union[
        OneOfPmtuDiscoveryOptions1, OneOfPmtuDiscoveryOptions2, OneOfPmtuDiscoveryOptions3
    ] = _field(metadata={"alias": "pmtuDiscovery"})


@dataclass
class BfdData:
    default_dscp: Union[
        OneOfDefaultDscpOptions1, OneOfDefaultDscpOptions2, OneOfDefaultDscpOptions3
    ] = _field(metadata={"alias": "defaultDscp"})
    multiplier: Union[OneOfMultiplierOptions1, OneOfMultiplierOptions2, OneOfMultiplierOptions3]
    poll_interval: Union[
        OneOfPollIntervalOptions1, OneOfPollIntervalOptions2, OneOfPollIntervalOptions3
    ] = _field(metadata={"alias": "pollInterval"})
    # Set color that identifies the WAN transport tunnel
    colors: Optional[List[Colors]] = _field(default=None)


@dataclass
class Payload:
    """
    BFD profile parcel schema for POST request
    """

    data: BfdData
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
    # BFD profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanSystemBfdPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateBfdProfileParcelForSystemPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemBfdData:
    default_dscp: Union[
        OneOfDefaultDscpOptions1, OneOfDefaultDscpOptions2, OneOfDefaultDscpOptions3
    ] = _field(metadata={"alias": "defaultDscp"})
    multiplier: Union[OneOfMultiplierOptions1, OneOfMultiplierOptions2, OneOfMultiplierOptions3]
    poll_interval: Union[
        OneOfPollIntervalOptions1, OneOfPollIntervalOptions2, OneOfPollIntervalOptions3
    ] = _field(metadata={"alias": "pollInterval"})
    # Set color that identifies the WAN transport tunnel
    colors: Optional[List[Colors]] = _field(default=None)


@dataclass
class CreateBfdProfileParcelForSystemPostRequest:
    """
    BFD profile parcel schema for POST request
    """

    data: SystemBfdData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class BfdOneOfMultiplierOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BfdOneOfPollIntervalOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BfdOneOfDefaultDscpOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BfdOneOfColorOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: BfdColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class BfdOneOfHelloIntervalOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BfdOneOfColorMultiplierOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BfdOneOfColorDscpOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BfdColors:
    color: Union[OneOfColorOptions1, BfdOneOfColorOptions2]
    dscp: Union[OneOfColorDscpOptions1, BfdOneOfColorDscpOptions2, OneOfColorDscpOptions3]
    hello_interval: Union[
        OneOfHelloIntervalOptions1, BfdOneOfHelloIntervalOptions2, OneOfHelloIntervalOptions3
    ] = _field(metadata={"alias": "helloInterval"})
    multiplier: Union[
        OneOfColorMultiplierOptions1, BfdOneOfColorMultiplierOptions2, OneOfColorMultiplierOptions3
    ]
    pmtu_discovery: Union[
        OneOfPmtuDiscoveryOptions1, OneOfPmtuDiscoveryOptions2, OneOfPmtuDiscoveryOptions3
    ] = _field(metadata={"alias": "pmtuDiscovery"})


@dataclass
class SdwanSystemBfdData:
    default_dscp: Union[
        OneOfDefaultDscpOptions1, BfdOneOfDefaultDscpOptions2, OneOfDefaultDscpOptions3
    ] = _field(metadata={"alias": "defaultDscp"})
    multiplier: Union[OneOfMultiplierOptions1, BfdOneOfMultiplierOptions2, OneOfMultiplierOptions3]
    poll_interval: Union[
        OneOfPollIntervalOptions1, BfdOneOfPollIntervalOptions2, OneOfPollIntervalOptions3
    ] = _field(metadata={"alias": "pollInterval"})
    # Set color that identifies the WAN transport tunnel
    colors: Optional[List[BfdColors]] = _field(default=None)


@dataclass
class BfdPayload:
    """
    BFD profile parcel schema for PUT request
    """

    data: SdwanSystemBfdData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanSystemBfdPayload:
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
    # BFD profile parcel schema for PUT request
    payload: Optional[BfdPayload] = _field(default=None)


@dataclass
class EditBfdProfileParcelForSystemPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemBfdOneOfMultiplierOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBfdOneOfPollIntervalOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBfdOneOfDefaultDscpOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBfdOneOfColorOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemBfdColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemBfdOneOfHelloIntervalOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBfdOneOfColorMultiplierOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBfdOneOfColorDscpOptions2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBfdColors:
    color: Union[OneOfColorOptions1, SystemBfdOneOfColorOptions2]
    dscp: Union[OneOfColorDscpOptions1, SystemBfdOneOfColorDscpOptions2, OneOfColorDscpOptions3]
    hello_interval: Union[
        OneOfHelloIntervalOptions1, SystemBfdOneOfHelloIntervalOptions2, OneOfHelloIntervalOptions3
    ] = _field(metadata={"alias": "helloInterval"})
    multiplier: Union[
        OneOfColorMultiplierOptions1,
        SystemBfdOneOfColorMultiplierOptions2,
        OneOfColorMultiplierOptions3,
    ]
    pmtu_discovery: Union[
        OneOfPmtuDiscoveryOptions1, OneOfPmtuDiscoveryOptions2, OneOfPmtuDiscoveryOptions3
    ] = _field(metadata={"alias": "pmtuDiscovery"})


@dataclass
class FeatureProfileSdwanSystemBfdData:
    default_dscp: Union[
        OneOfDefaultDscpOptions1, SystemBfdOneOfDefaultDscpOptions2, OneOfDefaultDscpOptions3
    ] = _field(metadata={"alias": "defaultDscp"})
    multiplier: Union[
        OneOfMultiplierOptions1, SystemBfdOneOfMultiplierOptions2, OneOfMultiplierOptions3
    ]
    poll_interval: Union[
        OneOfPollIntervalOptions1, SystemBfdOneOfPollIntervalOptions2, OneOfPollIntervalOptions3
    ] = _field(metadata={"alias": "pollInterval"})
    # Set color that identifies the WAN transport tunnel
    colors: Optional[List[SystemBfdColors]] = _field(default=None)


@dataclass
class EditBfdProfileParcelForSystemPutRequest:
    """
    BFD profile parcel schema for PUT request
    """

    data: FeatureProfileSdwanSystemBfdData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
