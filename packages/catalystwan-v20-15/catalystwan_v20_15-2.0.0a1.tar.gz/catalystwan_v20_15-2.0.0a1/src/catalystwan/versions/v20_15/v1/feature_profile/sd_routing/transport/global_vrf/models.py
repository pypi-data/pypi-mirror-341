# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

Ipv4SubnetMaskDef = Literal[
    "0.0.0.0",
    "128.0.0.0",
    "192.0.0.0",
    "224.0.0.0",
    "240.0.0.0",
    "248.0.0.0",
    "252.0.0.0",
    "254.0.0.0",
    "255.0.0.0",
    "255.128.0.0",
    "255.192.0.0",
    "255.224.0.0",
    "255.240.0.0",
    "255.252.0.0",
    "255.254.0.0",
    "255.255.0.0",
    "255.255.128.0",
    "255.255.192.0",
    "255.255.224.0",
    "255.255.240.0",
    "255.255.248.0",
    "255.255.252.0",
    "255.255.254.0",
    "255.255.255.0",
    "255.255.255.128",
    "255.255.255.192",
    "255.255.255.224",
    "255.255.255.240",
    "255.255.255.248",
    "255.255.255.252",
    "255.255.255.254",
    "255.255.255.255",
]

StaticNatDirectionDef = Literal["inside", "outside"]

NatPortForwardProtocolDef = Literal["TCP", "UDP"]

SourceTypeDef = Literal["acl", "route-map"]

NatTypeDef = Literal["interface", "pool"]


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpAddressOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class Dns:
    ip_address: Union[OneOfIpAddressOptionsDef1, OneOfIpAddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )


@dataclass
class OneOfHostNameOptionsWithoutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHostNameOptionsWithoutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfListOfIpOptionsWithoutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfListOfIpOptionsWithoutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[Any, Any]]


@dataclass
class HostMapping:
    host_name: Union[OneOfHostNameOptionsWithoutDefault1, OneOfHostNameOptionsWithoutDefault2] = (
        _field(metadata={"alias": "hostName"})
    )
    list_of_ip: Union[OneOfListOfIpOptionsWithoutDefault1, OneOfListOfIpOptionsWithoutDefault2] = (
        _field(metadata={"alias": "listOfIp"})
    )


@dataclass
class OneOfIpV4AddressOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfIpV4SubnetMaskOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4SubnetMaskOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4SubnetMaskDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Prefix:
    """
    Prefix
    """

    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class OneOfIpV4AddressOptionsWithoutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4AddressOptionsWithoutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfIpv4NextHopDistanceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv4NextHopDistanceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RefId:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRefIdOptionsDef1:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class OneOfRefIdOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class NextHop:
    address: Union[OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        OneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]
    tracker_id: Union[OneOfRefIdOptionsDef1, OneOfRefIdOptionsDef2] = _field(
        metadata={"alias": "trackerId"}
    )


@dataclass
class NextHopContainer:
    # IPv4 Route Gateway Next Hop
    next_hop: List[NextHop] = _field(metadata={"alias": "nextHop"})


@dataclass
class OneOfIpRoute1:
    next_hop_container: NextHopContainer = _field(metadata={"alias": "nextHopContainer"})


@dataclass
class OneOfIpv4V6RouteNull0OptionsWithoutVariable1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpv4V6RouteNull0OptionsWithoutVariable2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpRoute2:
    null0: Union[
        OneOfIpv4V6RouteNull0OptionsWithoutVariable1, OneOfIpv4V6RouteNull0OptionsWithoutVariable2
    ]
    distance: Optional[
        Union[
            OneOfIpv4NextHopDistanceOptionsDef1,
            OneOfIpv4NextHopDistanceOptionsDef2,
            OneOfIpv4NextHopDistanceOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfIpv4RouteDhcpOptionsWithoutVariable1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpv4RouteDhcpOptionsWithoutVariable2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpRoute3:
    dhcp: Union[
        OneOfIpv4RouteDhcpOptionsWithoutVariable1, OneOfIpv4RouteDhcpOptionsWithoutVariable2
    ]
    distance: Optional[
        Union[
            OneOfIpv4NextHopDistanceOptionsDef1,
            OneOfIpv4NextHopDistanceOptionsDef2,
            OneOfIpv4NextHopDistanceOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfVrfInterfaceNameOptionsNoDefaultDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVrfInterfaceNameOptionsNoDefaultDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class GlobalVrfNextHop:
    address: Union[OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        OneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


@dataclass
class IpStaticRouteInterface:
    interface_name: Union[
        OneOfVrfInterfaceNameOptionsNoDefaultDef1, OneOfVrfInterfaceNameOptionsNoDefaultDef2
    ] = _field(metadata={"alias": "interfaceName"})
    next_hop: Optional[List[GlobalVrfNextHop]] = _field(default=None, metadata={"alias": "nextHop"})


@dataclass
class InterfaceContainer:
    ip_static_route_interface: List[IpStaticRouteInterface] = _field(
        metadata={"alias": "ipStaticRouteInterface"}
    )


@dataclass
class OneOfIpRoute4:
    interface_container: InterfaceContainer = _field(metadata={"alias": "interfaceContainer"})


@dataclass
class Ipv4Route:
    one_of_ip_route: Union[OneOfIpRoute1, OneOfIpRoute2, OneOfIpRoute3, OneOfIpRoute4] = _field(
        metadata={"alias": "oneOfIpRoute"}
    )
    # Prefix
    prefix: Prefix


@dataclass
class OneOfIpv6RoutePrefixOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6RoutePrefixOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6NextHopAddressOptionsWithOutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6NextHopAddressOptionsWithOutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6NextHopDistanceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv6NextHopDistanceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfNextHop:
    address: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        OneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class GlobalVrfNextHopContainer:
    # IPv6 Route Gateway Next Hop
    next_hop: Optional[List[TransportGlobalVrfNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )


@dataclass
class GlobalVrfOneOfIpRoute1:
    next_hop_container: GlobalVrfNextHopContainer = _field(metadata={"alias": "nextHopContainer"})


@dataclass
class GlobalVrfOneOfIpRoute2:
    null0: Union[
        OneOfIpv4V6RouteNull0OptionsWithoutVariable1, OneOfIpv4V6RouteNull0OptionsWithoutVariable2
    ]


@dataclass
class SdRoutingTransportGlobalVrfNextHop:
    address: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        OneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class Ipv6StaticRouteInterface:
    interface_name: Union[
        OneOfVrfInterfaceNameOptionsNoDefaultDef1, OneOfVrfInterfaceNameOptionsNoDefaultDef2
    ] = _field(metadata={"alias": "interfaceName"})
    next_hop: Optional[List[SdRoutingTransportGlobalVrfNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )


@dataclass
class GlobalVrfInterfaceContainer:
    ipv6_static_route_interface: List[Ipv6StaticRouteInterface] = _field(
        metadata={"alias": "ipv6StaticRouteInterface"}
    )


@dataclass
class GlobalVrfOneOfIpRoute3:
    interface_container: GlobalVrfInterfaceContainer = _field(
        metadata={"alias": "interfaceContainer"}
    )


@dataclass
class Ipv6Route:
    one_of_ip_route: Union[
        GlobalVrfOneOfIpRoute1, GlobalVrfOneOfIpRoute2, GlobalVrfOneOfIpRoute3
    ] = _field(metadata={"alias": "oneOfIpRoute"})
    prefix: Union[OneOfIpv6RoutePrefixOptionsDef1, OneOfIpv6RoutePrefixOptionsDef2]


@dataclass
class OneOfOnBooleanDefaultFalseNoVariableOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultFalseNoVariableOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDirectionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: StaticNatDirectionDef


@dataclass
class NatInterfaces:
    direction: OneOfDirectionOptionsDef
    interface: Union[
        OneOfVrfInterfaceNameOptionsNoDefaultDef1, OneOfVrfInterfaceNameOptionsNoDefaultDef2
    ]


@dataclass
class StaticNat:
    direction: OneOfDirectionOptionsDef
    source_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "sourceIp"}
    )
    translate_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "translateIp"}
    )
    route_map_id: Optional[Union[OneOfRefIdOptionsDef1, OneOfRefIdOptionsDef2]] = _field(
        default=None, metadata={"alias": "routeMapId"}
    )


@dataclass
class OneOfPrefixLengthOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPrefixLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class StaticNatSubnet:
    direction: OneOfDirectionOptionsDef
    prefix_length: Union[OneOfPrefixLengthOptionsDef1, OneOfPrefixLengthOptionsDef2] = _field(
        metadata={"alias": "prefixLength"}
    )
    source_ip_subnet: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "sourceIpSubnet"}
    )
    translate_ip_subnet: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "translateIpSubnet"}
    )


@dataclass
class OneOfNatPortForwardProtocolOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatPortForwardProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NatPortForwardProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class NatPortForward:
    protocol: Union[OneOfNatPortForwardProtocolOptionsDef1, OneOfNatPortForwardProtocolOptionsDef2]
    source_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "sourceIp"}
    )
    source_port: Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2] = _field(
        metadata={"alias": "sourcePort"}
    )
    translate_port: Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2] = _field(
        metadata={"alias": "translatePort"}
    )
    translated_source_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "translatedSourceIp"}
    )


@dataclass
class NatType:
    value: Optional[Any] = _field(default=None)


@dataclass
class OneOfSourceTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SourceTypeDef


@dataclass
class ParcelReferenceDef:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class OneOfPoolNameOptionsNoDefaultDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPoolNameOptionsNoDefaultDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPrefixLengthWithoutDefaultOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPrefixLengthWithoutDefaultOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NatPool:
    """
    NAT Pool
    """

    pool_name: Union[OneOfPoolNameOptionsNoDefaultDef1, OneOfPoolNameOptionsNoDefaultDef2] = _field(
        metadata={"alias": "poolName"}
    )
    prefix_length: Union[
        OneOfPrefixLengthWithoutDefaultOptionsDef1, OneOfPrefixLengthWithoutDefaultOptionsDef2
    ] = _field(metadata={"alias": "prefixLength"})
    range_end: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "rangeEnd"}
    )
    range_start: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "rangeStart"}
    )
    overload: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class DynamicNat1:
    direction: OneOfDirectionOptionsDef
    egress_interface: Union[
        OneOfVrfInterfaceNameOptionsNoDefaultDef1, OneOfVrfInterfaceNameOptionsNoDefaultDef2
    ] = _field(metadata={"alias": "egressInterface"})
    nat_type: NatType = _field(metadata={"alias": "natType"})
    source_type: OneOfSourceTypeOptionsDef = _field(metadata={"alias": "sourceType"})
    ipv4_acl_id: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclId"}
    )
    # NAT Pool
    nat_pool: Optional[NatPool] = _field(default=None, metadata={"alias": "natPool"})
    route_map_id: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "routeMapId"}
    )


@dataclass
class OneOfNatTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NatTypeDef


@dataclass
class DynamicNat2:
    direction: OneOfDirectionOptionsDef
    nat_type: OneOfNatTypeOptionsDef = _field(metadata={"alias": "natType"})
    source_type: OneOfSourceTypeOptionsDef = _field(metadata={"alias": "sourceType"})
    egress_interface: Optional[
        Union[OneOfVrfInterfaceNameOptionsNoDefaultDef1, OneOfVrfInterfaceNameOptionsNoDefaultDef2]
    ] = _field(default=None, metadata={"alias": "egressInterface"})
    ipv4_acl_id: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclId"}
    )
    # NAT Pool
    nat_pool: Optional[NatPool] = _field(default=None, metadata={"alias": "natPool"})
    route_map_id: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "routeMapId"}
    )


@dataclass
class NatAttributesIpv4:
    """
    NAT Attributes Ipv4
    """

    nat_enable: Union[
        OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
        OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
    ] = _field(metadata={"alias": "natEnable"})
    # NAT Attributes Ipv4
    dynamic_nat: Optional[List[Union[DynamicNat1, DynamicNat2]]] = _field(
        default=None, metadata={"alias": "dynamicNat"}
    )
    # nat interfaces
    nat_interfaces: Optional[List[NatInterfaces]] = _field(
        default=None, metadata={"alias": "natInterfaces"}
    )
    # NAT Port Forward
    nat_port_forward: Optional[List[NatPortForward]] = _field(
        default=None, metadata={"alias": "natPortForward"}
    )
    # static NAT
    static_nat: Optional[List[StaticNat]] = _field(default=None, metadata={"alias": "staticNat"})
    # static NAT Subnet
    static_nat_subnet: Optional[List[StaticNatSubnet]] = _field(
        default=None, metadata={"alias": "staticNatSubnet"}
    )


@dataclass
class GlobalVrfData:
    enhance_ecmp_keying: Union[
        OneOfOnBooleanDefaultFalseOptionsDef1,
        OneOfOnBooleanDefaultFalseOptionsDef2,
        OneOfOnBooleanDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "enhanceEcmpKeying"})
    dns: Optional[List[Dns]] = _field(default=None)
    host_mapping: Optional[List[HostMapping]] = _field(
        default=None, metadata={"alias": "hostMapping"}
    )
    # IPv4 Static Route
    ipv4_route: Optional[List[Ipv4Route]] = _field(default=None, metadata={"alias": "ipv4Route"})
    # IPv6 Static Route
    ipv6_route: Optional[List[Ipv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    # NAT Attributes Ipv4
    nat_attributes_ipv4: Optional[NatAttributesIpv4] = _field(
        default=None, metadata={"alias": "natAttributesIpv4"}
    )


@dataclass
class Payload:
    """
    SD-Routing Global VRF feature schema
    """

    data: GlobalVrfData
    name: str
    # Set the feature description
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
    # SD-Routing Global VRF feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingTransportGlobalVrfPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingTransportGlobalVrfFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class TransportGlobalVrfData:
    enhance_ecmp_keying: Union[
        OneOfOnBooleanDefaultFalseOptionsDef1,
        OneOfOnBooleanDefaultFalseOptionsDef2,
        OneOfOnBooleanDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "enhanceEcmpKeying"})
    dns: Optional[List[Dns]] = _field(default=None)
    host_mapping: Optional[List[HostMapping]] = _field(
        default=None, metadata={"alias": "hostMapping"}
    )
    # IPv4 Static Route
    ipv4_route: Optional[List[Ipv4Route]] = _field(default=None, metadata={"alias": "ipv4Route"})
    # IPv6 Static Route
    ipv6_route: Optional[List[Ipv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    # NAT Attributes Ipv4
    nat_attributes_ipv4: Optional[NatAttributesIpv4] = _field(
        default=None, metadata={"alias": "natAttributesIpv4"}
    )


@dataclass
class CreateSdroutingTransportGlobalVrfFeaturePostRequest:
    """
    SD-Routing Global VRF feature schema
    """

    data: TransportGlobalVrfData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingTransportGlobalVrfPayload:
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
    # SD-Routing Global VRF feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingTransportGlobalVrfFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingTransportGlobalVrfData:
    enhance_ecmp_keying: Union[
        OneOfOnBooleanDefaultFalseOptionsDef1,
        OneOfOnBooleanDefaultFalseOptionsDef2,
        OneOfOnBooleanDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "enhanceEcmpKeying"})
    dns: Optional[List[Dns]] = _field(default=None)
    host_mapping: Optional[List[HostMapping]] = _field(
        default=None, metadata={"alias": "hostMapping"}
    )
    # IPv4 Static Route
    ipv4_route: Optional[List[Ipv4Route]] = _field(default=None, metadata={"alias": "ipv4Route"})
    # IPv6 Static Route
    ipv6_route: Optional[List[Ipv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    # NAT Attributes Ipv4
    nat_attributes_ipv4: Optional[NatAttributesIpv4] = _field(
        default=None, metadata={"alias": "natAttributesIpv4"}
    )


@dataclass
class EditSdroutingTransportGlobalVrfFeaturePutRequest:
    """
    SD-Routing Global VRF feature schema
    """

    data: SdRoutingTransportGlobalVrfData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
