# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

VariableOptionTypeDef = Literal["variable"]

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

Ipv4GatewayDef = Literal["dhcp", "nextHop", "null0"]

DefaultIpv4GatewayDef = Literal["nextHop"]

Ipv6RouteNatDef = Literal["NAT64", "NAT66"]

ServiceTypeDef = Literal["TE"]

VpnIpv4GatewayDef = Literal["dhcp", "nextHop", "null0"]

VpnDefaultIpv4GatewayDef = Literal["nextHop"]

VpnServiceTypeDef = Literal["TE"]

WanVpnIpv4GatewayDef = Literal["dhcp", "nextHop", "null0"]

WanVpnDefaultIpv4GatewayDef = Literal["nextHop"]

WanVpnServiceTypeDef = Literal["TE"]


@dataclass
class OneOfVpnIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVpnIdOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEnhanceEcmpKeyingOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEnhanceEcmpKeyingOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfEnhanceEcmpKeyingOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPrimaryDnsAddressIpv4OptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPrimaryDnsAddressIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPrimaryDnsAddressIpv4OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSecondaryDnsAddressIpv4OptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSecondaryDnsAddressIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSecondaryDnsAddressIpv4OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class DnsIpv4:
    primary_dns_address_ipv4: Optional[
        Union[
            OneOfPrimaryDnsAddressIpv4OptionsDef1,
            OneOfPrimaryDnsAddressIpv4OptionsDef2,
            OneOfPrimaryDnsAddressIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDnsAddressIpv4"})
    secondary_dns_address_ipv4: Optional[
        Union[
            OneOfSecondaryDnsAddressIpv4OptionsDef1,
            OneOfSecondaryDnsAddressIpv4OptionsDef2,
            OneOfSecondaryDnsAddressIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDnsAddressIpv4"})


@dataclass
class OneOfPrimaryDnsAddressIpv6OptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPrimaryDnsAddressIpv6OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPrimaryDnsAddressIpv6OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSecondaryDnsAddressIpv6OptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSecondaryDnsAddressIpv6OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSecondaryDnsAddressIpv6OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class DnsIpv6:
    primary_dns_address_ipv6: Optional[
        Union[
            OneOfPrimaryDnsAddressIpv6OptionsDef1,
            OneOfPrimaryDnsAddressIpv6OptionsDef2,
            OneOfPrimaryDnsAddressIpv6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDnsAddressIpv6"})
    secondary_dns_address_ipv6: Optional[
        Union[
            OneOfSecondaryDnsAddressIpv6OptionsDef1,
            OneOfSecondaryDnsAddressIpv6OptionsDef2,
            OneOfSecondaryDnsAddressIpv6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDnsAddressIpv6"})


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
class NewHostMapping:
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
    value: str


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

    ip_address: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None, metadata={"alias": "ipAddress"}
    )
    subnet_mask: Optional[Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]] = (
        _field(default=None, metadata={"alias": "subnetMask"})
    )


@dataclass
class Gateway:
    value: Optional[Any] = _field(default=None)


@dataclass
class OneOfIpv4NextHopAddressOptionsWithOutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4NextHopAddressOptionsWithOutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[Any, str]


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
class NextHop:
    address: Optional[
        Union[
            OneOfIpv4NextHopAddressOptionsWithOutDefault1,
            OneOfIpv4NextHopAddressOptionsWithOutDefault2,
        ]
    ] = _field(default=None)
    distance: Optional[
        Union[
            OneOfIpv4NextHopDistanceOptionsDef1,
            OneOfIpv4NextHopDistanceOptionsDef2,
            OneOfIpv4NextHopDistanceOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfIpv4GatewayDistanceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4GatewayDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv4GatewayDistanceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Ipv4Route1:
    gateway: Gateway
    # IPv4 Route Gateway Next Hop
    next_hop: List[NextHop] = _field(metadata={"alias": "nextHop"})
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            OneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)
    # Prefix
    prefix: Optional[Prefix] = _field(default=None)


@dataclass
class OneOfIpv4RouteGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4GatewayDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpv4RouteGatewayOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultIpv4GatewayDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Ipv4Route2:
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            OneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)
    gateway: Optional[Union[OneOfIpv4RouteGatewayOptionsDef1, OneOfIpv4RouteGatewayOptionsDef2]] = (
        _field(default=None)
    )
    # IPv4 Route Gateway Next Hop
    next_hop: Optional[List[NextHop]] = _field(default=None, metadata={"alias": "nextHop"})
    # Prefix
    prefix: Optional[Prefix] = _field(default=None)


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
class VpnNextHop:
    address: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        OneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class NextHopContainer:
    # IPv6 Route Gateway Next Hop
    next_hop: Optional[List[VpnNextHop]] = _field(default=None, metadata={"alias": "nextHop"})


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


@dataclass
class OneOfIpv6RouteNatOptionsWithoutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6RouteNatOptionsWithoutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv6RouteNatDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpRoute3:
    nat: Union[OneOfIpv6RouteNatOptionsWithoutDefault1, OneOfIpv6RouteNatOptionsWithoutDefault2]


@dataclass
class Ipv6Route:
    one_of_ip_route: Union[OneOfIpRoute1, OneOfIpRoute2, OneOfIpRoute3] = _field(
        metadata={"alias": "oneOfIpRoute"}
    )
    prefix: Union[OneOfIpv6RoutePrefixOptionsDef1, OneOfIpv6RoutePrefixOptionsDef2]


@dataclass
class OneOfServiceTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Service:
    service_type: OneOfServiceTypeOptionsDef = _field(metadata={"alias": "serviceType"})


@dataclass
class OneOfNat64V4PoolNameOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNat64V4PoolNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNat64V4PoolRangeStartOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNat64V4PoolRangeStartOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNat64V4PoolRangeEndOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNat64V4PoolRangeEndOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNat64V4PoolOverloadOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNat64V4PoolOverloadOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNat64V4PoolOverloadOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Nat64V4Pool:
    nat64_v4_pool_name: Union[OneOfNat64V4PoolNameOptionsDef1, OneOfNat64V4PoolNameOptionsDef2] = (
        _field(metadata={"alias": "nat64V4PoolName"})
    )
    nat64_v4_pool_overload: Union[
        OneOfNat64V4PoolOverloadOptionsDef1,
        OneOfNat64V4PoolOverloadOptionsDef2,
        OneOfNat64V4PoolOverloadOptionsDef3,
    ] = _field(metadata={"alias": "nat64V4PoolOverload"})
    nat64_v4_pool_range_end: Union[
        OneOfNat64V4PoolRangeEndOptionsDef1, OneOfNat64V4PoolRangeEndOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolRangeEnd"})
    nat64_v4_pool_range_start: Union[
        OneOfNat64V4PoolRangeStartOptionsDef1, OneOfNat64V4PoolRangeStartOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolRangeStart"})


@dataclass
class VpnData:
    enhance_ecmp_keying: Union[
        OneOfEnhanceEcmpKeyingOptionsDef1,
        OneOfEnhanceEcmpKeyingOptionsDef2,
        OneOfEnhanceEcmpKeyingOptionsDef3,
    ] = _field(metadata={"alias": "enhanceEcmpKeying"})
    vpn_id: Union[OneOfVpnIdOptionsDef1, OneOfVpnIdOptionsDef2] = _field(
        metadata={"alias": "vpnId"}
    )
    dns_ipv4: Optional[DnsIpv4] = _field(default=None, metadata={"alias": "dnsIpv4"})
    dns_ipv6: Optional[DnsIpv6] = _field(default=None, metadata={"alias": "dnsIpv6"})
    # IPv4 Static Route
    ipv4_route: Optional[List[Union[Ipv4Route1, Ipv4Route2]]] = _field(
        default=None, metadata={"alias": "ipv4Route"}
    )
    # IPv6 Static Route
    ipv6_route: Optional[List[Ipv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    # NAT64 V4 Pool
    nat64_v4_pool: Optional[List[Nat64V4Pool]] = _field(
        default=None, metadata={"alias": "nat64V4Pool"}
    )
    new_host_mapping: Optional[List[NewHostMapping]] = _field(
        default=None, metadata={"alias": "newHostMapping"}
    )
    # Service
    service: Optional[List[Service]] = _field(default=None)


@dataclass
class Payload:
    """
    WAN VPN profile parcel schema for POST request
    """

    data: VpnData
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
    # WAN VPN profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanTransportWanVpnPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateWanVpnProfileParcelForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class WanVpnData:
    enhance_ecmp_keying: Union[
        OneOfEnhanceEcmpKeyingOptionsDef1,
        OneOfEnhanceEcmpKeyingOptionsDef2,
        OneOfEnhanceEcmpKeyingOptionsDef3,
    ] = _field(metadata={"alias": "enhanceEcmpKeying"})
    vpn_id: Union[OneOfVpnIdOptionsDef1, OneOfVpnIdOptionsDef2] = _field(
        metadata={"alias": "vpnId"}
    )
    dns_ipv4: Optional[DnsIpv4] = _field(default=None, metadata={"alias": "dnsIpv4"})
    dns_ipv6: Optional[DnsIpv6] = _field(default=None, metadata={"alias": "dnsIpv6"})
    # IPv4 Static Route
    ipv4_route: Optional[List[Union[Ipv4Route1, Ipv4Route2]]] = _field(
        default=None, metadata={"alias": "ipv4Route"}
    )
    # IPv6 Static Route
    ipv6_route: Optional[List[Ipv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    # NAT64 V4 Pool
    nat64_v4_pool: Optional[List[Nat64V4Pool]] = _field(
        default=None, metadata={"alias": "nat64V4Pool"}
    )
    new_host_mapping: Optional[List[NewHostMapping]] = _field(
        default=None, metadata={"alias": "newHostMapping"}
    )
    # Service
    service: Optional[List[Service]] = _field(default=None)


@dataclass
class CreateWanVpnProfileParcelForTransportPostRequest:
    """
    WAN VPN profile parcel schema for POST request
    """

    data: WanVpnData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class VpnOneOfVpnIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfPrimaryDnsAddressIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfSecondaryDnsAddressIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnDnsIpv4:
    primary_dns_address_ipv4: Optional[
        Union[
            OneOfPrimaryDnsAddressIpv4OptionsDef1,
            VpnOneOfPrimaryDnsAddressIpv4OptionsDef2,
            OneOfPrimaryDnsAddressIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDnsAddressIpv4"})
    secondary_dns_address_ipv4: Optional[
        Union[
            OneOfSecondaryDnsAddressIpv4OptionsDef1,
            VpnOneOfSecondaryDnsAddressIpv4OptionsDef2,
            OneOfSecondaryDnsAddressIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDnsAddressIpv4"})


@dataclass
class VpnDnsIpv6:
    primary_dns_address_ipv6: Optional[
        Union[
            OneOfPrimaryDnsAddressIpv6OptionsDef1,
            OneOfPrimaryDnsAddressIpv6OptionsDef2,
            OneOfPrimaryDnsAddressIpv6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDnsAddressIpv6"})
    secondary_dns_address_ipv6: Optional[
        Union[
            OneOfSecondaryDnsAddressIpv6OptionsDef1,
            OneOfSecondaryDnsAddressIpv6OptionsDef2,
            OneOfSecondaryDnsAddressIpv6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDnsAddressIpv6"})


@dataclass
class VpnOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnPrefix:
    """
    Prefix
    """

    ip_address: Optional[Union[OneOfIpV4AddressOptionsDef1, VpnOneOfIpV4AddressOptionsDef2]] = (
        _field(default=None, metadata={"alias": "ipAddress"})
    )
    subnet_mask: Optional[Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]] = (
        _field(default=None, metadata={"alias": "subnetMask"})
    )


@dataclass
class VpnOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnNextHop:
    address: Optional[
        Union[
            OneOfIpv4NextHopAddressOptionsWithOutDefault1,
            OneOfIpv4NextHopAddressOptionsWithOutDefault2,
        ]
    ] = _field(default=None)
    distance: Optional[
        Union[
            OneOfIpv4NextHopDistanceOptionsDef1,
            VpnOneOfIpv4NextHopDistanceOptionsDef2,
            OneOfIpv4NextHopDistanceOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class VpnOneOfIpv4GatewayDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnIpv4Route1:
    gateway: Gateway
    # IPv4 Route Gateway Next Hop
    next_hop: List[WanVpnNextHop] = _field(metadata={"alias": "nextHop"})
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            VpnOneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)
    # Prefix
    prefix: Optional[VpnPrefix] = _field(default=None)


@dataclass
class WanVpnOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WanVpnPrefix:
    """
    Prefix
    """

    ip_address: Optional[Union[OneOfIpV4AddressOptionsDef1, WanVpnOneOfIpV4AddressOptionsDef2]] = (
        _field(default=None, metadata={"alias": "ipAddress"})
    )
    subnet_mask: Optional[Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]] = (
        _field(default=None, metadata={"alias": "subnetMask"})
    )


@dataclass
class VpnOneOfIpv4RouteGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnIpv4GatewayDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnOneOfIpv4RouteGatewayOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnDefaultIpv4GatewayDef  # pytype: disable=annotation-type-mismatch


@dataclass
class WanVpnOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportWanVpnNextHop:
    address: Optional[
        Union[
            OneOfIpv4NextHopAddressOptionsWithOutDefault1,
            OneOfIpv4NextHopAddressOptionsWithOutDefault2,
        ]
    ] = _field(default=None)
    distance: Optional[
        Union[
            OneOfIpv4NextHopDistanceOptionsDef1,
            WanVpnOneOfIpv4NextHopDistanceOptionsDef2,
            OneOfIpv4NextHopDistanceOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class WanVpnOneOfIpv4GatewayDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnIpv4Route2:
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            WanVpnOneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)
    gateway: Optional[
        Union[VpnOneOfIpv4RouteGatewayOptionsDef1, VpnOneOfIpv4RouteGatewayOptionsDef2]
    ] = _field(default=None)
    # IPv4 Route Gateway Next Hop
    next_hop: Optional[List[TransportWanVpnNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )
    # Prefix
    prefix: Optional[WanVpnPrefix] = _field(default=None)


@dataclass
class VpnOneOfIpv6NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanTransportWanVpnNextHop:
    address: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        VpnOneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class VpnNextHopContainer:
    # IPv6 Route Gateway Next Hop
    next_hop: Optional[List[SdwanTransportWanVpnNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )


@dataclass
class VpnOneOfIpRoute1:
    next_hop_container: VpnNextHopContainer = _field(metadata={"alias": "nextHopContainer"})


@dataclass
class VpnIpv6Route:
    one_of_ip_route: Union[VpnOneOfIpRoute1, OneOfIpRoute2, OneOfIpRoute3] = _field(
        metadata={"alias": "oneOfIpRoute"}
    )
    prefix: Union[OneOfIpv6RoutePrefixOptionsDef1, OneOfIpv6RoutePrefixOptionsDef2]


@dataclass
class VpnOneOfServiceTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnServiceTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnService:
    service_type: VpnOneOfServiceTypeOptionsDef = _field(metadata={"alias": "serviceType"})


@dataclass
class VpnOneOfNat64V4PoolNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfNat64V4PoolRangeStartOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfNat64V4PoolRangeEndOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnNat64V4Pool:
    nat64_v4_pool_name: Union[
        OneOfNat64V4PoolNameOptionsDef1, VpnOneOfNat64V4PoolNameOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolName"})
    nat64_v4_pool_overload: Union[
        OneOfNat64V4PoolOverloadOptionsDef1,
        OneOfNat64V4PoolOverloadOptionsDef2,
        OneOfNat64V4PoolOverloadOptionsDef3,
    ] = _field(metadata={"alias": "nat64V4PoolOverload"})
    nat64_v4_pool_range_end: Union[
        OneOfNat64V4PoolRangeEndOptionsDef1, VpnOneOfNat64V4PoolRangeEndOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolRangeEnd"})
    nat64_v4_pool_range_start: Union[
        OneOfNat64V4PoolRangeStartOptionsDef1, VpnOneOfNat64V4PoolRangeStartOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolRangeStart"})


@dataclass
class TransportWanVpnData:
    enhance_ecmp_keying: Union[
        OneOfEnhanceEcmpKeyingOptionsDef1,
        OneOfEnhanceEcmpKeyingOptionsDef2,
        OneOfEnhanceEcmpKeyingOptionsDef3,
    ] = _field(metadata={"alias": "enhanceEcmpKeying"})
    vpn_id: Union[VpnOneOfVpnIdOptionsDef1, OneOfVpnIdOptionsDef2] = _field(
        metadata={"alias": "vpnId"}
    )
    dns_ipv4: Optional[VpnDnsIpv4] = _field(default=None, metadata={"alias": "dnsIpv4"})
    dns_ipv6: Optional[VpnDnsIpv6] = _field(default=None, metadata={"alias": "dnsIpv6"})
    # IPv4 Static Route
    ipv4_route: Optional[List[Union[VpnIpv4Route1, VpnIpv4Route2]]] = _field(
        default=None, metadata={"alias": "ipv4Route"}
    )
    # IPv6 Static Route
    ipv6_route: Optional[List[VpnIpv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    # NAT64 V4 Pool
    nat64_v4_pool: Optional[List[VpnNat64V4Pool]] = _field(
        default=None, metadata={"alias": "nat64V4Pool"}
    )
    new_host_mapping: Optional[List[NewHostMapping]] = _field(
        default=None, metadata={"alias": "newHostMapping"}
    )
    # Service
    service: Optional[List[VpnService]] = _field(default=None)


@dataclass
class VpnPayload:
    """
    WAN VPN profile parcel schema for PUT request
    """

    data: TransportWanVpnData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanTransportWanVpnPayload:
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
    # WAN VPN profile parcel schema for PUT request
    payload: Optional[VpnPayload] = _field(default=None)


@dataclass
class EditWanVpnProfileParcelForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class WanVpnOneOfVpnIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnOneOfPrimaryDnsAddressIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WanVpnOneOfSecondaryDnsAddressIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WanVpnDnsIpv4:
    primary_dns_address_ipv4: Optional[
        Union[
            OneOfPrimaryDnsAddressIpv4OptionsDef1,
            WanVpnOneOfPrimaryDnsAddressIpv4OptionsDef2,
            OneOfPrimaryDnsAddressIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDnsAddressIpv4"})
    secondary_dns_address_ipv4: Optional[
        Union[
            OneOfSecondaryDnsAddressIpv4OptionsDef1,
            WanVpnOneOfSecondaryDnsAddressIpv4OptionsDef2,
            OneOfSecondaryDnsAddressIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDnsAddressIpv4"})


@dataclass
class WanVpnDnsIpv6:
    primary_dns_address_ipv6: Optional[
        Union[
            OneOfPrimaryDnsAddressIpv6OptionsDef1,
            OneOfPrimaryDnsAddressIpv6OptionsDef2,
            OneOfPrimaryDnsAddressIpv6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDnsAddressIpv6"})
    secondary_dns_address_ipv6: Optional[
        Union[
            OneOfSecondaryDnsAddressIpv6OptionsDef1,
            OneOfSecondaryDnsAddressIpv6OptionsDef2,
            OneOfSecondaryDnsAddressIpv6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDnsAddressIpv6"})


@dataclass
class TransportWanVpnOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportWanVpnPrefix:
    """
    Prefix
    """

    ip_address: Optional[
        Union[OneOfIpV4AddressOptionsDef1, TransportWanVpnOneOfIpV4AddressOptionsDef2]
    ] = _field(default=None, metadata={"alias": "ipAddress"})
    subnet_mask: Optional[Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]] = (
        _field(default=None, metadata={"alias": "subnetMask"})
    )


@dataclass
class TransportWanVpnOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdwanTransportWanVpnNextHop:
    address: Optional[
        Union[
            OneOfIpv4NextHopAddressOptionsWithOutDefault1,
            OneOfIpv4NextHopAddressOptionsWithOutDefault2,
        ]
    ] = _field(default=None)
    distance: Optional[
        Union[
            OneOfIpv4NextHopDistanceOptionsDef1,
            TransportWanVpnOneOfIpv4NextHopDistanceOptionsDef2,
            OneOfIpv4NextHopDistanceOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class TransportWanVpnOneOfIpv4GatewayDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnIpv4Route1:
    gateway: Gateway
    # IPv4 Route Gateway Next Hop
    next_hop: List[FeatureProfileSdwanTransportWanVpnNextHop] = _field(
        metadata={"alias": "nextHop"}
    )
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            TransportWanVpnOneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)
    # Prefix
    prefix: Optional[TransportWanVpnPrefix] = _field(default=None)


@dataclass
class SdwanTransportWanVpnOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanTransportWanVpnPrefix:
    """
    Prefix
    """

    ip_address: Optional[
        Union[OneOfIpV4AddressOptionsDef1, SdwanTransportWanVpnOneOfIpV4AddressOptionsDef2]
    ] = _field(default=None, metadata={"alias": "ipAddress"})
    subnet_mask: Optional[Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]] = (
        _field(default=None, metadata={"alias": "subnetMask"})
    )


@dataclass
class WanVpnOneOfIpv4RouteGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: WanVpnIpv4GatewayDef  # pytype: disable=annotation-type-mismatch


@dataclass
class WanVpnOneOfIpv4RouteGatewayOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: WanVpnDefaultIpv4GatewayDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanTransportWanVpnOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdwanTransportWanVpnNextHop:
    address: Optional[
        Union[
            OneOfIpv4NextHopAddressOptionsWithOutDefault1,
            OneOfIpv4NextHopAddressOptionsWithOutDefault2,
        ]
    ] = _field(default=None)
    distance: Optional[
        Union[
            OneOfIpv4NextHopDistanceOptionsDef1,
            SdwanTransportWanVpnOneOfIpv4NextHopDistanceOptionsDef2,
            OneOfIpv4NextHopDistanceOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class SdwanTransportWanVpnOneOfIpv4GatewayDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnIpv4Route2:
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            SdwanTransportWanVpnOneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)
    gateway: Optional[
        Union[WanVpnOneOfIpv4RouteGatewayOptionsDef1, WanVpnOneOfIpv4RouteGatewayOptionsDef2]
    ] = _field(default=None)
    # IPv4 Route Gateway Next Hop
    next_hop: Optional[List[V1FeatureProfileSdwanTransportWanVpnNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )
    # Prefix
    prefix: Optional[SdwanTransportWanVpnPrefix] = _field(default=None)


@dataclass
class WanVpnOneOfIpv6NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NextHop1:
    address: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        WanVpnOneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class WanVpnNextHopContainer:
    # IPv6 Route Gateway Next Hop
    next_hop: Optional[List[NextHop1]] = _field(default=None, metadata={"alias": "nextHop"})


@dataclass
class WanVpnOneOfIpRoute1:
    next_hop_container: WanVpnNextHopContainer = _field(metadata={"alias": "nextHopContainer"})


@dataclass
class WanVpnIpv6Route:
    one_of_ip_route: Union[WanVpnOneOfIpRoute1, OneOfIpRoute2, OneOfIpRoute3] = _field(
        metadata={"alias": "oneOfIpRoute"}
    )
    prefix: Union[OneOfIpv6RoutePrefixOptionsDef1, OneOfIpv6RoutePrefixOptionsDef2]


@dataclass
class WanVpnOneOfServiceTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: WanVpnServiceTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class WanVpnService:
    service_type: WanVpnOneOfServiceTypeOptionsDef = _field(metadata={"alias": "serviceType"})


@dataclass
class WanVpnOneOfNat64V4PoolNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WanVpnOneOfNat64V4PoolRangeStartOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WanVpnOneOfNat64V4PoolRangeEndOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WanVpnNat64V4Pool:
    nat64_v4_pool_name: Union[
        OneOfNat64V4PoolNameOptionsDef1, WanVpnOneOfNat64V4PoolNameOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolName"})
    nat64_v4_pool_overload: Union[
        OneOfNat64V4PoolOverloadOptionsDef1,
        OneOfNat64V4PoolOverloadOptionsDef2,
        OneOfNat64V4PoolOverloadOptionsDef3,
    ] = _field(metadata={"alias": "nat64V4PoolOverload"})
    nat64_v4_pool_range_end: Union[
        OneOfNat64V4PoolRangeEndOptionsDef1, WanVpnOneOfNat64V4PoolRangeEndOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolRangeEnd"})
    nat64_v4_pool_range_start: Union[
        OneOfNat64V4PoolRangeStartOptionsDef1, WanVpnOneOfNat64V4PoolRangeStartOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolRangeStart"})


@dataclass
class SdwanTransportWanVpnData:
    enhance_ecmp_keying: Union[
        OneOfEnhanceEcmpKeyingOptionsDef1,
        OneOfEnhanceEcmpKeyingOptionsDef2,
        OneOfEnhanceEcmpKeyingOptionsDef3,
    ] = _field(metadata={"alias": "enhanceEcmpKeying"})
    vpn_id: Union[WanVpnOneOfVpnIdOptionsDef1, OneOfVpnIdOptionsDef2] = _field(
        metadata={"alias": "vpnId"}
    )
    dns_ipv4: Optional[WanVpnDnsIpv4] = _field(default=None, metadata={"alias": "dnsIpv4"})
    dns_ipv6: Optional[WanVpnDnsIpv6] = _field(default=None, metadata={"alias": "dnsIpv6"})
    # IPv4 Static Route
    ipv4_route: Optional[List[Union[WanVpnIpv4Route1, WanVpnIpv4Route2]]] = _field(
        default=None, metadata={"alias": "ipv4Route"}
    )
    # IPv6 Static Route
    ipv6_route: Optional[List[WanVpnIpv6Route]] = _field(
        default=None, metadata={"alias": "ipv6Route"}
    )
    # NAT64 V4 Pool
    nat64_v4_pool: Optional[List[WanVpnNat64V4Pool]] = _field(
        default=None, metadata={"alias": "nat64V4Pool"}
    )
    new_host_mapping: Optional[List[NewHostMapping]] = _field(
        default=None, metadata={"alias": "newHostMapping"}
    )
    # Service
    service: Optional[List[WanVpnService]] = _field(default=None)


@dataclass
class EditWanVpnProfileParcelForTransportPutRequest:
    """
    WAN VPN profile parcel schema for PUT request
    """

    data: SdwanTransportWanVpnData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
