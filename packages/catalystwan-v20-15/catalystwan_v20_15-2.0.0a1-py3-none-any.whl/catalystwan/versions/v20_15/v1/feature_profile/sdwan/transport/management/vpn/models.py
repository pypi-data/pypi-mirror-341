# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

DefaultOptionTypeDef = Literal["default"]

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

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

VpnIpv4GatewayDef = Literal["dhcp", "nextHop", "null0"]

VpnDefaultIpv4GatewayDef = Literal["nextHop"]

ManagementVpnIpv4GatewayDef = Literal["dhcp", "nextHop", "null0"]

ManagementVpnDefaultIpv4GatewayDef = Literal["nextHop"]


@dataclass
class OneOfVpnIdOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVpnNameOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVpnNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVpnNameOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


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

    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
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
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        OneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


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
    # Prefix
    prefix: Prefix
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            OneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)


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
    gateway: Union[OneOfIpv4RouteGatewayOptionsDef1, OneOfIpv4RouteGatewayOptionsDef2]
    # Prefix
    prefix: Prefix
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            OneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)
    # IPv4 Route Gateway Next Hop
    next_hop: Optional[List[NextHop]] = _field(default=None, metadata={"alias": "nextHop"})


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
class VpnData:
    vpn_id: OneOfVpnIdOptionsDef = _field(metadata={"alias": "vpnId"})
    dns_ipv4: Optional[DnsIpv4] = _field(default=None, metadata={"alias": "dnsIpv4"})
    dns_ipv6: Optional[DnsIpv6] = _field(default=None, metadata={"alias": "dnsIpv6"})
    # IPv4 Static Route
    ipv4_route: Optional[List[Union[Ipv4Route1, Ipv4Route2]]] = _field(
        default=None, metadata={"alias": "ipv4Route"}
    )
    # IPv6 Static Route
    ipv6_route: Optional[List[Ipv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    name: Optional[
        Union[OneOfVpnNameOptionsDef1, OneOfVpnNameOptionsDef2, OneOfVpnNameOptionsDef3]
    ] = _field(default=None)
    new_host_mapping: Optional[List[NewHostMapping]] = _field(
        default=None, metadata={"alias": "newHostMapping"}
    )


@dataclass
class Payload:
    """
    Management Vpn Post Request schema
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
    # Management Vpn Post Request schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanTransportManagementVpnPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateManagementVpnProfileParcelForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ManagementVpnData:
    vpn_id: OneOfVpnIdOptionsDef = _field(metadata={"alias": "vpnId"})
    dns_ipv4: Optional[DnsIpv4] = _field(default=None, metadata={"alias": "dnsIpv4"})
    dns_ipv6: Optional[DnsIpv6] = _field(default=None, metadata={"alias": "dnsIpv6"})
    # IPv4 Static Route
    ipv4_route: Optional[List[Union[Ipv4Route1, Ipv4Route2]]] = _field(
        default=None, metadata={"alias": "ipv4Route"}
    )
    # IPv6 Static Route
    ipv6_route: Optional[List[Ipv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    name: Optional[
        Union[OneOfVpnNameOptionsDef1, OneOfVpnNameOptionsDef2, OneOfVpnNameOptionsDef3]
    ] = _field(default=None)
    new_host_mapping: Optional[List[NewHostMapping]] = _field(
        default=None, metadata={"alias": "newHostMapping"}
    )


@dataclass
class CreateManagementVpnProfileParcelForTransportPostRequest:
    """
    Management Vpn Post Request schema
    """

    data: ManagementVpnData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class VpnOneOfVpnIdOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
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

    ip_address: Union[OneOfIpV4AddressOptionsDef1, VpnOneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class VpnOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ManagementVpnNextHop:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        VpnOneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


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
    next_hop: List[ManagementVpnNextHop] = _field(metadata={"alias": "nextHop"})
    # Prefix
    prefix: VpnPrefix
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            VpnOneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class ManagementVpnOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ManagementVpnPrefix:
    """
    Prefix
    """

    ip_address: Union[OneOfIpV4AddressOptionsDef1, ManagementVpnOneOfIpV4AddressOptionsDef2] = (
        _field(metadata={"alias": "ipAddress"})
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
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
class ManagementVpnOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportManagementVpnNextHop:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        ManagementVpnOneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


@dataclass
class ManagementVpnOneOfIpv4GatewayDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnIpv4Route2:
    gateway: Union[VpnOneOfIpv4RouteGatewayOptionsDef1, VpnOneOfIpv4RouteGatewayOptionsDef2]
    # Prefix
    prefix: ManagementVpnPrefix
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            ManagementVpnOneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)
    # IPv4 Route Gateway Next Hop
    next_hop: Optional[List[TransportManagementVpnNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )


@dataclass
class VpnOneOfIpv6NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanTransportManagementVpnNextHop:
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
    next_hop: Optional[List[SdwanTransportManagementVpnNextHop]] = _field(
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
class TransportManagementVpnData:
    vpn_id: VpnOneOfVpnIdOptionsDef = _field(metadata={"alias": "vpnId"})
    dns_ipv4: Optional[VpnDnsIpv4] = _field(default=None, metadata={"alias": "dnsIpv4"})
    dns_ipv6: Optional[VpnDnsIpv6] = _field(default=None, metadata={"alias": "dnsIpv6"})
    # IPv4 Static Route
    ipv4_route: Optional[List[Union[VpnIpv4Route1, VpnIpv4Route2]]] = _field(
        default=None, metadata={"alias": "ipv4Route"}
    )
    # IPv6 Static Route
    ipv6_route: Optional[List[VpnIpv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    name: Optional[
        Union[OneOfVpnNameOptionsDef1, OneOfVpnNameOptionsDef2, OneOfVpnNameOptionsDef3]
    ] = _field(default=None)
    new_host_mapping: Optional[List[NewHostMapping]] = _field(
        default=None, metadata={"alias": "newHostMapping"}
    )


@dataclass
class VpnPayload:
    """
    Management Vpn Put Request schema
    """

    data: TransportManagementVpnData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanTransportManagementVpnPayload:
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
    # Management Vpn Put Request schema
    payload: Optional[VpnPayload] = _field(default=None)


@dataclass
class EditManagementVpnProfileParcelForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ManagementVpnOneOfVpnIdOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ManagementVpnOneOfPrimaryDnsAddressIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ManagementVpnOneOfSecondaryDnsAddressIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ManagementVpnDnsIpv4:
    primary_dns_address_ipv4: Optional[
        Union[
            OneOfPrimaryDnsAddressIpv4OptionsDef1,
            ManagementVpnOneOfPrimaryDnsAddressIpv4OptionsDef2,
            OneOfPrimaryDnsAddressIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDnsAddressIpv4"})
    secondary_dns_address_ipv4: Optional[
        Union[
            OneOfSecondaryDnsAddressIpv4OptionsDef1,
            ManagementVpnOneOfSecondaryDnsAddressIpv4OptionsDef2,
            OneOfSecondaryDnsAddressIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDnsAddressIpv4"})


@dataclass
class ManagementVpnDnsIpv6:
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
class TransportManagementVpnOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportManagementVpnPrefix:
    """
    Prefix
    """

    ip_address: Union[
        OneOfIpV4AddressOptionsDef1, TransportManagementVpnOneOfIpV4AddressOptionsDef2
    ] = _field(metadata={"alias": "ipAddress"})
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class TransportManagementVpnOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdwanTransportManagementVpnNextHop:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        TransportManagementVpnOneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


@dataclass
class TransportManagementVpnOneOfIpv4GatewayDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ManagementVpnIpv4Route1:
    gateway: Gateway
    # IPv4 Route Gateway Next Hop
    next_hop: List[FeatureProfileSdwanTransportManagementVpnNextHop] = _field(
        metadata={"alias": "nextHop"}
    )
    # Prefix
    prefix: TransportManagementVpnPrefix
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            TransportManagementVpnOneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class SdwanTransportManagementVpnOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanTransportManagementVpnPrefix:
    """
    Prefix
    """

    ip_address: Union[
        OneOfIpV4AddressOptionsDef1, SdwanTransportManagementVpnOneOfIpV4AddressOptionsDef2
    ] = _field(metadata={"alias": "ipAddress"})
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class ManagementVpnOneOfIpv4RouteGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ManagementVpnIpv4GatewayDef  # pytype: disable=annotation-type-mismatch


@dataclass
class ManagementVpnOneOfIpv4RouteGatewayOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ManagementVpnDefaultIpv4GatewayDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanTransportManagementVpnOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdwanTransportManagementVpnNextHop:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        SdwanTransportManagementVpnOneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


@dataclass
class SdwanTransportManagementVpnOneOfIpv4GatewayDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ManagementVpnIpv4Route2:
    gateway: Union[
        ManagementVpnOneOfIpv4RouteGatewayOptionsDef1, ManagementVpnOneOfIpv4RouteGatewayOptionsDef2
    ]
    # Prefix
    prefix: SdwanTransportManagementVpnPrefix
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            SdwanTransportManagementVpnOneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)
    # IPv4 Route Gateway Next Hop
    next_hop: Optional[List[V1FeatureProfileSdwanTransportManagementVpnNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )


@dataclass
class ManagementVpnOneOfIpv6NextHopDistanceOptionsDef2:
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
        ManagementVpnOneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class ManagementVpnNextHopContainer:
    # IPv6 Route Gateway Next Hop
    next_hop: Optional[List[NextHop1]] = _field(default=None, metadata={"alias": "nextHop"})


@dataclass
class ManagementVpnOneOfIpRoute1:
    next_hop_container: ManagementVpnNextHopContainer = _field(
        metadata={"alias": "nextHopContainer"}
    )


@dataclass
class ManagementVpnIpv6Route:
    one_of_ip_route: Union[ManagementVpnOneOfIpRoute1, OneOfIpRoute2, OneOfIpRoute3] = _field(
        metadata={"alias": "oneOfIpRoute"}
    )
    prefix: Union[OneOfIpv6RoutePrefixOptionsDef1, OneOfIpv6RoutePrefixOptionsDef2]


@dataclass
class SdwanTransportManagementVpnData:
    vpn_id: ManagementVpnOneOfVpnIdOptionsDef = _field(metadata={"alias": "vpnId"})
    dns_ipv4: Optional[ManagementVpnDnsIpv4] = _field(default=None, metadata={"alias": "dnsIpv4"})
    dns_ipv6: Optional[ManagementVpnDnsIpv6] = _field(default=None, metadata={"alias": "dnsIpv6"})
    # IPv4 Static Route
    ipv4_route: Optional[List[Union[ManagementVpnIpv4Route1, ManagementVpnIpv4Route2]]] = _field(
        default=None, metadata={"alias": "ipv4Route"}
    )
    # IPv6 Static Route
    ipv6_route: Optional[List[ManagementVpnIpv6Route]] = _field(
        default=None, metadata={"alias": "ipv6Route"}
    )
    name: Optional[
        Union[OneOfVpnNameOptionsDef1, OneOfVpnNameOptionsDef2, OneOfVpnNameOptionsDef3]
    ] = _field(default=None)
    new_host_mapping: Optional[List[NewHostMapping]] = _field(
        default=None, metadata={"alias": "newHostMapping"}
    )


@dataclass
class EditManagementVpnProfileParcelForTransportPutRequest:
    """
    Management Vpn Put Request schema
    """

    data: SdwanTransportManagementVpnData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
