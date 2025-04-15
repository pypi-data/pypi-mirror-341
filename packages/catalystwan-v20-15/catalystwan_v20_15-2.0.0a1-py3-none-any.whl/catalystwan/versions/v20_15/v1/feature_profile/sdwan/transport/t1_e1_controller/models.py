# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

TypeDef = Literal["e1", "t1"]

VariableOptionTypeDef = Literal["variable"]

Value = Literal["T1"]

ControllerTxExListFramingT1 = Literal["esf", "sf"]

DefaultOptionTypeDef = Literal["default"]

ControllerTxExListLinecodeT1 = Literal["ami", "b8zs"]

T1E1ControllerValue = Literal["E1"]

ControllerTxExListFramingE1 = Literal["crc4", "no-crc4"]

ControllerTxExListLinecodeE1 = Literal["ami", "hdb3"]

ControllerTxExListClockSource = Literal["internal", "line", "loop-timed", "network"]

ControllerTxExListLineModeDef = Literal["primary", "secondary"]

TransportT1E1ControllerValue = Literal["short"]

ControllerTxExListShortDef = Literal["110ft", "220ft", "330ft", "440ft", "550ft", "660ft"]

SdwanTransportT1E1ControllerValue = Literal["long"]

ControllerTxExListLongDef = Literal["-15db", "-22.5db", "-7.5db", "0db"]


@dataclass
class OneOfTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSlotOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSlotOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Name:
    """
    Card Type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListFramingOptionsT11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ControllerTxExListFramingT1  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListFramingOptionsT12:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfControllerTxExListFramingOptionsT13:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListLinecodeOptionsT11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ControllerTxExListLinecodeT1  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListLinecodeOptionsT12:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfControllerTxExListLinecodeOptionsT13:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class T1:
    # Card Type
    name: Name
    framing: Optional[
        Union[
            OneOfControllerTxExListFramingOptionsT11,
            OneOfControllerTxExListFramingOptionsT12,
            OneOfControllerTxExListFramingOptionsT13,
        ]
    ] = _field(default=None)
    linecode: Optional[
        Union[
            OneOfControllerTxExListLinecodeOptionsT11,
            OneOfControllerTxExListLinecodeOptionsT12,
            OneOfControllerTxExListLinecodeOptionsT13,
        ]
    ] = _field(default=None)


@dataclass
class Basic1:
    t1: T1 = _field(metadata={"alias": "T1"})


@dataclass
class T1E1ControllerName:
    """
    Card Type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: T1E1ControllerValue  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListFramingOptionsE11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ControllerTxExListFramingE1  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListFramingOptionsE12:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfControllerTxExListFramingOptionsE13:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListLinecodeOptionsE11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ControllerTxExListLinecodeE1  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListLinecodeOptionsE12:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfControllerTxExListLinecodeOptionsE13:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class E1:
    # Card Type
    name: T1E1ControllerName
    framing: Optional[
        Union[
            OneOfControllerTxExListFramingOptionsE11,
            OneOfControllerTxExListFramingOptionsE12,
            OneOfControllerTxExListFramingOptionsE13,
        ]
    ] = _field(default=None)
    linecode: Optional[
        Union[
            OneOfControllerTxExListLinecodeOptionsE11,
            OneOfControllerTxExListLinecodeOptionsE12,
            OneOfControllerTxExListLinecodeOptionsE13,
        ]
    ] = _field(default=None)


@dataclass
class Basic2:
    e1: E1 = _field(metadata={"alias": "E1"})


@dataclass
class Cable:
    length_long: Optional[Any] = _field(default=None, metadata={"alias": "lengthLong"})


@dataclass
class OneOfControllerTxExListClockSourceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ControllerTxExListClockSource  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListClockSourceOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListLineModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ControllerTxExListLineModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListLineModeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfControllerTxExListLineModeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfControllerTxExListDescriptionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfControllerTxExListDescriptionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListChannelGroupNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfControllerTxExListChannelGroupNumberOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfControllerTxExListChannelGroupTimeslotsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfControllerTxExListChannelGroupTimeslotsOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class ChannelGroup:
    number: Union[
        OneOfControllerTxExListChannelGroupNumberOptionsDef1,
        OneOfControllerTxExListChannelGroupNumberOptionsDef2,
    ]
    timeslots: Union[
        OneOfControllerTxExListChannelGroupTimeslotsOptionsDef1,
        OneOfControllerTxExListChannelGroupTimeslotsOptionsDef2,
    ]


@dataclass
class ControllerTxExList1:
    # Basic Config
    basic: Union[Basic1, Basic2]
    cable: Optional[Cable] = _field(default=None)
    # Channel Group List
    channel_group: Optional[List[ChannelGroup]] = _field(
        default=None, metadata={"alias": "channelGroup"}
    )
    clock_source: Optional[
        Union[
            OneOfControllerTxExListClockSourceOptionsDef1,
            OneOfControllerTxExListClockSourceOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "clockSource"})
    description: Optional[
        Union[
            OneOfControllerTxExListDescriptionOptionsDef1,
            OneOfControllerTxExListDescriptionOptionsDef2,
            OneOfControllerTxExListDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    line_mode: Optional[
        Union[
            OneOfControllerTxExListLineModeOptionsDef1,
            OneOfControllerTxExListLineModeOptionsDef2,
            OneOfControllerTxExListLineModeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lineMode"})


@dataclass
class DefaultOptionNoDefaultDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Cable1:
    cable_length: Optional[DefaultOptionNoDefaultDef] = _field(
        default=None, metadata={"alias": "cableLength"}
    )


@dataclass
class CableLength:
    """
    Cable Config
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportT1E1ControllerValue  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListShortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ControllerTxExListShortDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListShortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Cable2:
    # Cable Config
    cable_length: Optional[CableLength] = _field(default=None, metadata={"alias": "cableLength"})
    length_short: Optional[
        Union[OneOfControllerTxExListShortOptionsDef1, OneOfControllerTxExListShortOptionsDef2]
    ] = _field(default=None, metadata={"alias": "lengthShort"})


@dataclass
class T1E1ControllerCableLength:
    """
    Cable Config
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanTransportT1E1ControllerValue  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListLongOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ControllerTxExListLongDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerTxExListLongOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Cable3:
    # Cable Config
    cable_length: Optional[T1E1ControllerCableLength] = _field(
        default=None, metadata={"alias": "cableLength"}
    )
    length_long: Optional[
        Union[OneOfControllerTxExListLongOptionsDef1, OneOfControllerTxExListLongOptionsDef2]
    ] = _field(default=None, metadata={"alias": "lengthLong"})


@dataclass
class ControllerTxExList2:
    # Basic Config
    basic: Union[Basic1, Basic2]
    # Cable Config
    cable: Optional[Union[Cable1, Cable2, Cable3]] = _field(default=None)
    # Channel Group List
    channel_group: Optional[List[ChannelGroup]] = _field(
        default=None, metadata={"alias": "channelGroup"}
    )
    clock_source: Optional[
        Union[
            OneOfControllerTxExListClockSourceOptionsDef1,
            OneOfControllerTxExListClockSourceOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "clockSource"})
    description: Optional[
        Union[
            OneOfControllerTxExListDescriptionOptionsDef1,
            OneOfControllerTxExListDescriptionOptionsDef2,
            OneOfControllerTxExListDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    line_mode: Optional[
        Union[
            OneOfControllerTxExListLineModeOptionsDef1,
            OneOfControllerTxExListLineModeOptionsDef2,
            OneOfControllerTxExListLineModeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lineMode"})


@dataclass
class T1E1ControllerData:
    # Controller tx-ex List
    controller_tx_ex_list: List[Union[ControllerTxExList1, ControllerTxExList2]] = _field(
        metadata={"alias": "controllerTxExList"}
    )
    slot: Union[OneOfSlotOptionsDef1, OneOfSlotOptionsDef2]
    type_: OneOfTypeOptionsDef = _field(metadata={"alias": "type"})


@dataclass
class Payload:
    """
    T1E1Controller profile parcel schema for POST/PUT request
    """

    data: T1E1ControllerData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


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
    # T1E1Controller profile parcel schema for POST/PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanTransportT1E1ControllerPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateT1E1ControllerProfileParcelForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class TransportT1E1ControllerData:
    # Controller tx-ex List
    controller_tx_ex_list: List[Union[ControllerTxExList1, ControllerTxExList2]] = _field(
        metadata={"alias": "controllerTxExList"}
    )
    slot: Union[OneOfSlotOptionsDef1, OneOfSlotOptionsDef2]
    type_: OneOfTypeOptionsDef = _field(metadata={"alias": "type"})


@dataclass
class CreateT1E1ControllerProfileParcelForTransportPostRequest:
    """
    T1E1Controller profile parcel schema for POST/PUT request
    """

    data: TransportT1E1ControllerData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanTransportT1E1ControllerPayload:
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
    # T1E1Controller profile parcel schema for POST/PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditT1E1ControllerProfileParcelForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanTransportT1E1ControllerData:
    # Controller tx-ex List
    controller_tx_ex_list: List[Union[ControllerTxExList1, ControllerTxExList2]] = _field(
        metadata={"alias": "controllerTxExList"}
    )
    slot: Union[OneOfSlotOptionsDef1, OneOfSlotOptionsDef2]
    type_: OneOfTypeOptionsDef = _field(metadata={"alias": "type"})


@dataclass
class EditT1E1ControllerProfileParcelForTransportPutRequest:
    """
    T1E1Controller profile parcel schema for POST/PUT request
    """

    data: SdwanTransportT1E1ControllerData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
