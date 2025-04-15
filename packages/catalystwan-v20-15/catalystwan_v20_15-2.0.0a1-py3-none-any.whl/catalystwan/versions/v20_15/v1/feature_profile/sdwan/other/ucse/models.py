# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

SharedLomTypeDef = Literal["console", "failover", "ge1", "ge2", "ge3", "te2", "te3"]

SharedFailOverTypeDef = Literal["ge2", "te2"]

VariableOptionTypeDef = Literal["variable"]


@dataclass
class OneOfBayOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSlotOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfOnBooleanDefaultTrueNoVariableOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultTrueNoVariableOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfSharedLomOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SharedLomTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSharedFailOverOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SharedFailOverTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SharedLom:
    fail_over_type: Optional[OneOfSharedFailOverOptionsDef] = _field(
        default=None, metadata={"alias": "failOverType"}
    )
    lom_type: Optional[OneOfSharedLomOptionsDef] = _field(
        default=None, metadata={"alias": "lomType"}
    )


@dataclass
class AccessPort:
    dedicated: Optional[
        Union[
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef1,
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef2,
        ]
    ] = _field(default=None)
    shared_lom: Optional[SharedLom] = _field(default=None, metadata={"alias": "sharedLom"})


@dataclass
class OneOfIpv4PrefixOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv4PrefixOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDefaultGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfDefaultGatewayOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDefaultGatewayOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Ip:
    address: Union[OneOfIpv4PrefixOptionsDef1, OneOfIpv4PrefixOptionsDef2]
    default_gateway: Union[
        OneOfDefaultGatewayOptionsDef1,
        OneOfDefaultGatewayOptionsDef2,
        OneOfDefaultGatewayOptionsDef3,
    ] = _field(metadata={"alias": "defaultGateway"})


@dataclass
class OneOfVlanIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVlanIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVlanIdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPriorityOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Vlan:
    priority: Optional[
        Union[OneOfPriorityOptionsDef1, OneOfPriorityOptionsDef2, OneOfPriorityOptionsDef3]
    ] = _field(default=None)
    vlan_id: Optional[
        Union[OneOfVlanIdOptionsDef1, OneOfVlanIdOptionsDef2, OneOfVlanIdOptionsDef3]
    ] = _field(default=None, metadata={"alias": "vlanId"})


@dataclass
class Imc:
    access_port: Optional[AccessPort] = _field(default=None, metadata={"alias": "access-port"})
    ip: Optional[Ip] = _field(default=None)
    vlan: Optional[Vlan] = _field(default=None)


@dataclass
class OneOfInterfaceNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceNameOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Onel3DefaultOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfaceUcseInterfaceVpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceUcseInterfaceVpnOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceUcseInterfaceVpnOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Interface:
    if_name: Union[
        OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2, OneOfInterfaceNameOptionsDef3
    ] = _field(metadata={"alias": "ifName"})
    address: Optional[Union[OneOfIpv4PrefixOptionsDef1, OneOfIpv4PrefixOptionsDef2]] = _field(
        default=None
    )
    l3: Optional[Onel3DefaultOptionsDef] = _field(default=None)
    ucse_interface_vpn: Optional[
        Union[
            OneOfInterfaceUcseInterfaceVpnOptionsDef1,
            OneOfInterfaceUcseInterfaceVpnOptionsDef2,
            OneOfInterfaceUcseInterfaceVpnOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ucseInterfaceVpn"})


@dataclass
class UcseData:
    bay: OneOfBayOptionsDef
    slot: OneOfSlotOptionsDef
    imc: Optional[Imc] = _field(default=None)
    # Interface name: GigabitEthernet0/<>/<> when present
    interface: Optional[List[Interface]] = _field(default=None)


@dataclass
class Payload:
    """
    ucse profile feature schema for  request
    """

    data: UcseData
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
    # ucse profile feature schema for  request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanOtherUcsePayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateUcseProfileFeatureForOtherPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OtherUcseData:
    bay: OneOfBayOptionsDef
    slot: OneOfSlotOptionsDef
    imc: Optional[Imc] = _field(default=None)
    # Interface name: GigabitEthernet0/<>/<> when present
    interface: Optional[List[Interface]] = _field(default=None)


@dataclass
class CreateUcseProfileFeatureForOtherPostRequest:
    """
    ucse profile feature schema for  request
    """

    data: OtherUcseData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanOtherUcsePayload:
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
    # ucse profile feature schema for  request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditUcseProfileFeatureForOtherPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanOtherUcseData:
    bay: OneOfBayOptionsDef
    slot: OneOfSlotOptionsDef
    imc: Optional[Imc] = _field(default=None)
    # Interface name: GigabitEthernet0/<>/<> when present
    interface: Optional[List[Interface]] = _field(default=None)


@dataclass
class EditUcseProfileFeatureForOtherPutRequest:
    """
    ucse profile feature schema for  request
    """

    data: SdwanOtherUcseData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
