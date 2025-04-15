# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

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

NetworkRedundancyDef = Literal["hsrp", "off", "vrrp"]

DefaultNetworkRedundancyDef = Literal["off"]

TrackerActionDef = Literal["Decrement", "Shutdown"]

DuplexDef = Literal["auto", "full", "half"]

SpeedDef = Literal["10", "100", "1000", "10000", "2500"]

MediaTypeDef = Literal["auto-select", "rj45", "sfp"]


@dataclass
class OneOfShutdownOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfShutdownOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfShutdownOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


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
class OneOfDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDescriptionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDescriptionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDynamicDhcpDistanceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDynamicDhcpDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDynamicDhcpDistanceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Dynamic:
    dynamic_dhcp_distance: Union[
        OneOfDynamicDhcpDistanceOptionsDef1,
        OneOfDynamicDhcpDistanceOptionsDef2,
        OneOfDynamicDhcpDistanceOptionsDef3,
    ] = _field(metadata={"alias": "dynamicDhcpDistance"})


@dataclass
class IntfIpAddress1:
    dynamic: Dynamic


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
class OneOfIpV4AddressOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


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
class OneOfIpV4SubnetMaskOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class StaticIpV4AddressPrimary:
    """
    Static IpV4Address Primary
    """

    ip_address: Union[
        OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2, OneOfIpV4AddressOptionsDef3
    ] = _field(metadata={"alias": "ipAddress"})
    subnet_mask: Union[
        OneOfIpV4SubnetMaskOptionsDef1,
        OneOfIpV4SubnetMaskOptionsDef2,
        OneOfIpV4SubnetMaskOptionsDef3,
    ] = _field(metadata={"alias": "subnetMask"})


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
class OneOfIpV4SubnetMaskOptionsWithoutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4SubnetMaskOptionsWithoutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4SubnetMaskDef  # pytype: disable=annotation-type-mismatch


@dataclass
class StaticIpV4AddressSecondary:
    ip_address: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipAddress"})
    subnet_mask: Union[
        OneOfIpV4SubnetMaskOptionsWithoutDefault1, OneOfIpV4SubnetMaskOptionsWithoutDefault2
    ] = _field(metadata={"alias": "subnetMask"})


@dataclass
class Static:
    # Static IpV4Address Primary
    static_ip_v4_address_primary: StaticIpV4AddressPrimary = _field(
        metadata={"alias": "staticIpV4AddressPrimary"}
    )
    # Secondary IpV4 Addresses
    static_ip_v4_address_secondary: Optional[List[StaticIpV4AddressSecondary]] = _field(
        default=None, metadata={"alias": "staticIpV4AddressSecondary"}
    )


@dataclass
class IntfIpAddress2:
    static: Static


@dataclass
class OneOfListOfIpV4OptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfListOfIpV4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Any]


@dataclass
class OneOfListOfIpV4OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class DhcpClient:
    """
    Enable DHCPv6
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpv6PrefixGlobalVariableWithoutDefault1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6PrefixGlobalVariableWithoutDefault2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class SecondaryIpV6Address:
    address: Union[
        OneOfIpv6PrefixGlobalVariableWithoutDefault1, OneOfIpv6PrefixGlobalVariableWithoutDefault2
    ]


@dataclass
class EthernetDynamic:
    # Enable DHCPv6
    dhcp_client: DhcpClient = _field(metadata={"alias": "dhcpClient"})
    # secondary IPv6 addresses
    secondary_ip_v6_address: Optional[List[SecondaryIpV6Address]] = _field(
        default=None, metadata={"alias": "secondaryIpV6Address"}
    )


@dataclass
class IntfIpV6Address1:
    dynamic: EthernetDynamic


@dataclass
class OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class PrimaryIpV6Address:
    """
    Static IpV6Address Primary
    """

    address: Union[
        OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef1,
        OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef2,
        OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef3,
    ]


@dataclass
class EthernetStatic:
    # Static IpV6Address Primary
    primary_ip_v6_address: Optional[PrimaryIpV6Address] = _field(
        default=None, metadata={"alias": "primaryIpV6Address"}
    )
    # Static secondary IPv6 addresses
    secondary_ip_v6_address: Optional[List[SecondaryIpV6Address]] = _field(
        default=None, metadata={"alias": "secondaryIpV6Address"}
    )


@dataclass
class IntfIpV6Address2:
    static: EthernetStatic


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
class Acl:
    """
    ACL
    """

    ipv4_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclEgress"}
    )
    ipv4_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclIngress"}
    )


@dataclass
class OneOfMacAddressOptionsNoDefaultDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfMacAddressOptionsNoDefaultDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Arp:
    ip_address: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipAddress"})
    mac_address: Union[OneOfMacAddressOptionsNoDefaultDef1, OneOfMacAddressOptionsNoDefaultDef2] = (
        _field(metadata={"alias": "macAddress"})
    )


@dataclass
class OneOfEnableBfdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfEnableBfdOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfEnableBfdOptionsDef3:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTransmitIntervalOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTransmitIntervalOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTransmitIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMinRecvIntervalOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMinRecvIntervalOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMinRecvIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMultiplierOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMultiplierOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMultiplierOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Bfd:
    """
    Configure BFD
    """

    min_recv_interval: Optional[
        Union[
            OneOfMinRecvIntervalOptionsDef1,
            OneOfMinRecvIntervalOptionsDef2,
            OneOfMinRecvIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "minRecvInterval"})
    multiplier: Optional[
        Union[OneOfMultiplierOptionsDef1, OneOfMultiplierOptionsDef2, OneOfMultiplierOptionsDef3]
    ] = _field(default=None)
    transmit_interval: Optional[
        Union[
            OneOfTransmitIntervalOptionsDef1,
            OneOfTransmitIntervalOptionsDef2,
            OneOfTransmitIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "transmitInterval"})


@dataclass
class OneOfNetworkRedundancyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NetworkRedundancyDef


@dataclass
class OneOfNetworkRedundancyOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultNetworkRedundancyDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfGroupIdOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfGroupIdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVrrpPriorityOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVrrpPriorityOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVrrpPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVrrpTimerOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVrrpTimerOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVrrpTimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class IpAddressSecondary:
    ip_address: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipAddress"})
    subnet_mask: Union[
        OneOfIpV4SubnetMaskOptionsWithoutDefault1, OneOfIpV4SubnetMaskOptionsWithoutDefault2
    ] = _field(metadata={"alias": "subnetMask"})


@dataclass
class OneOfMinPreemptDelayOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMinPreemptDelayOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMinPreemptDelayOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTrackerActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TrackerActionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDecrementValueOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDecrementValueOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TrackingObject:
    tracker_action: OneOfTrackerActionOptionsDef = _field(metadata={"alias": "trackerAction"})
    tracker_id: ParcelReferenceDef = _field(metadata={"alias": "trackerId"})
    decrement_value: Optional[
        Union[OneOfDecrementValueOptionsDef1, OneOfDecrementValueOptionsDef2]
    ] = _field(default=None, metadata={"alias": "decrementValue"})


@dataclass
class Vrrp:
    """
    Enable VRRP
    """

    group_id: Union[OneOfGroupIdOptionsDef1, OneOfGroupIdOptionsDef2]
    ip_address: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipAddress"})
    priority: Union[
        OneOfVrrpPriorityOptionsDef1, OneOfVrrpPriorityOptionsDef2, OneOfVrrpPriorityOptionsDef3
    ]
    timer: Union[OneOfVrrpTimerOptionsDef1, OneOfVrrpTimerOptionsDef2, OneOfVrrpTimerOptionsDef3]
    # VRRP Secondary Ip Addresses
    ip_address_secondary: Optional[List[IpAddressSecondary]] = _field(
        default=None, metadata={"alias": "ipAddressSecondary"}
    )
    min_preempt_delay: Optional[
        Union[
            OneOfMinPreemptDelayOptionsDef1,
            OneOfMinPreemptDelayOptionsDef2,
            OneOfMinPreemptDelayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "minPreemptDelay"})
    # Tracking object for VRRP configuration
    tracking_object: Optional[List[TrackingObject]] = _field(
        default=None, metadata={"alias": "trackingObject"}
    )


@dataclass
class OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpv6VrrpIpv6PrefixOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6VrrpIpv6PrefixOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6VrrpIpv6PrefixOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class VrrpIpv6:
    """
    Enable VRRP Ipv6
    """

    group_id: Union[OneOfGroupIdOptionsDef1, OneOfGroupIdOptionsDef2] = _field(
        metadata={"alias": "groupId"}
    )
    ipv6_link_local: Union[
        OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef1,
        OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef2,
        OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef3,
    ] = _field(metadata={"alias": "ipv6LinkLocal"})
    priority: Union[
        OneOfVrrpPriorityOptionsDef1, OneOfVrrpPriorityOptionsDef2, OneOfVrrpPriorityOptionsDef3
    ]
    timer: Union[OneOfVrrpTimerOptionsDef1, OneOfVrrpTimerOptionsDef2, OneOfVrrpTimerOptionsDef3]
    ipv6_prefix: Optional[
        Union[
            OneOfIpv6VrrpIpv6PrefixOptionsDef1,
            OneOfIpv6VrrpIpv6PrefixOptionsDef2,
            OneOfIpv6VrrpIpv6PrefixOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipv6Prefix"})
    min_preempt_delay: Optional[
        Union[
            OneOfMinPreemptDelayOptionsDef1,
            OneOfMinPreemptDelayOptionsDef2,
            OneOfMinPreemptDelayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "minPreemptDelay"})


@dataclass
class OneOfHsrpPriorityOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHsrpPriorityOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHsrpPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHsrpHelloTimerOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHsrpHelloTimerOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHsrpHelloTimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHsrpHoldTimerOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHsrpHoldTimerOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHsrpHoldTimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHsrpReloadPreemptDelayOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHsrpReloadPreemptDelayOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHsrpReloadPreemptDelayOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfHsrpMd5AuthKeyOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHsrpMd5AuthKeyOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfHsrpMd5AuthKeyOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class SecondaryAddress:
    address: Optional[
        Union[OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2]
    ] = _field(default=None)


@dataclass
class Hsrp:
    """
    Enable HSRP
    """

    group_id: Union[OneOfGroupIdOptionsDef1, OneOfGroupIdOptionsDef2] = _field(
        metadata={"alias": "groupId"}
    )
    ip_address: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipAddress"})
    priority: Union[
        OneOfHsrpPriorityOptionsDef1, OneOfHsrpPriorityOptionsDef2, OneOfHsrpPriorityOptionsDef3
    ]
    hello_timer: Optional[
        Union[
            OneOfHsrpHelloTimerOptionsDef1,
            OneOfHsrpHelloTimerOptionsDef2,
            OneOfHsrpHelloTimerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "helloTimer"})
    hold_timer: Optional[
        Union[
            OneOfHsrpHoldTimerOptionsDef1,
            OneOfHsrpHoldTimerOptionsDef2,
            OneOfHsrpHoldTimerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "holdTimer"})
    md5_auth_key: Optional[
        Union[
            OneOfHsrpMd5AuthKeyOptionsDef1,
            OneOfHsrpMd5AuthKeyOptionsDef2,
            OneOfHsrpMd5AuthKeyOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "md5AuthKey"})
    min_preempt_delay: Optional[
        Union[
            OneOfMinPreemptDelayOptionsDef1,
            OneOfMinPreemptDelayOptionsDef2,
            OneOfMinPreemptDelayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "minPreemptDelay"})
    reload_preempt_delay: Optional[
        Union[
            OneOfHsrpReloadPreemptDelayOptionsDef1,
            OneOfHsrpReloadPreemptDelayOptionsDef2,
            OneOfHsrpReloadPreemptDelayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "reloadPreemptDelay"})
    # HSRP Secondary Ip Address
    secondary_address: Optional[List[SecondaryAddress]] = _field(
        default=None, metadata={"alias": "secondaryAddress"}
    )
    # Tracking object for HSRP configuration
    tracking_object: Optional[List[TrackingObject]] = _field(
        default=None, metadata={"alias": "trackingObject"}
    )


@dataclass
class OneOfIpv6HsrpIpv6AutoConfigOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpv6HsrpIpv6AutoConfigOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6HsrpIpv6AutoConfigOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class HsrpIpv6:
    """
    Enable HSRP Ipv6
    """

    autoconfig: Union[
        OneOfIpv6HsrpIpv6AutoConfigOptionsDef1,
        OneOfIpv6HsrpIpv6AutoConfigOptionsDef2,
        OneOfIpv6HsrpIpv6AutoConfigOptionsDef3,
    ]
    group_id: Union[OneOfGroupIdOptionsDef1, OneOfGroupIdOptionsDef2] = _field(
        metadata={"alias": "groupId"}
    )
    priority: Union[
        OneOfHsrpPriorityOptionsDef1, OneOfHsrpPriorityOptionsDef2, OneOfHsrpPriorityOptionsDef3
    ]
    hello_timer: Optional[
        Union[
            OneOfHsrpHelloTimerOptionsDef1,
            OneOfHsrpHelloTimerOptionsDef2,
            OneOfHsrpHelloTimerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "helloTimer"})
    hold_timer: Optional[
        Union[
            OneOfHsrpHoldTimerOptionsDef1,
            OneOfHsrpHoldTimerOptionsDef2,
            OneOfHsrpHoldTimerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "holdTimer"})
    ipv6_link_local: Optional[
        Union[
            OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef1,
            OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef2,
            OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipv6LinkLocal"})
    ipv6_prefix: Optional[
        Union[
            OneOfIpv6VrrpIpv6PrefixOptionsDef1,
            OneOfIpv6VrrpIpv6PrefixOptionsDef2,
            OneOfIpv6VrrpIpv6PrefixOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipv6Prefix"})
    md5_auth_key: Optional[
        Union[
            OneOfHsrpMd5AuthKeyOptionsDef1,
            OneOfHsrpMd5AuthKeyOptionsDef2,
            OneOfHsrpMd5AuthKeyOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "md5AuthKey"})
    min_preempt_delay: Optional[
        Union[
            OneOfMinPreemptDelayOptionsDef1,
            OneOfMinPreemptDelayOptionsDef2,
            OneOfMinPreemptDelayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "minPreemptDelay"})
    reload_preempt_delay: Optional[
        Union[
            OneOfHsrpReloadPreemptDelayOptionsDef1,
            OneOfHsrpReloadPreemptDelayOptionsDef2,
            OneOfHsrpReloadPreemptDelayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "reloadPreemptDelay"})


@dataclass
class OneOfOnBooleanDefaultTrueOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOnBooleanDefaultTrueOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultTrueOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDuplexOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DuplexDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDuplexOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDuplexOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfMacAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfMacAddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMacAddressOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMtuOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIntrfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIntrfMtuOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIntrfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTcpMssAdjustOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTcpMssAdjustOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSpeedOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SpeedDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSpeedOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSpeedOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfArpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfArpTimeoutOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfArpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAutonegotiateOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAutonegotiateOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAutonegotiateOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfMediaTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: MediaTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfMediaTypeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMediaTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLoadIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfLoadIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLoadIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpDirectedBroadcastOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpDirectedBroadcastOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpDirectedBroadcastOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Advanced:
    """
    Advanced Attributes
    """

    arp_timeout: Optional[
        Union[OneOfArpTimeoutOptionsDef1, OneOfArpTimeoutOptionsDef2, OneOfArpTimeoutOptionsDef3]
    ] = _field(default=None, metadata={"alias": "arpTimeout"})
    autonegotiate: Optional[
        Union[
            OneOfAutonegotiateOptionsDef1,
            OneOfAutonegotiateOptionsDef2,
            OneOfAutonegotiateOptionsDef3,
        ]
    ] = _field(default=None)
    duplex: Optional[
        Union[OneOfDuplexOptionsDef1, OneOfDuplexOptionsDef2, OneOfDuplexOptionsDef3]
    ] = _field(default=None)
    icmp_redirect_disable: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "icmpRedirectDisable"})
    intrf_mtu: Optional[
        Union[OneOfIntrfMtuOptionsDef1, OneOfIntrfMtuOptionsDef2, OneOfIntrfMtuOptionsDef3]
    ] = _field(default=None, metadata={"alias": "intrfMtu"})
    ip_directed_broadcast: Optional[
        Union[
            OneOfIpDirectedBroadcastOptionsDef1,
            OneOfIpDirectedBroadcastOptionsDef2,
            OneOfIpDirectedBroadcastOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipDirectedBroadcast"})
    ip_mtu: Optional[Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3]] = _field(
        default=None, metadata={"alias": "ipMtu"}
    )
    load_interval: Optional[
        Union[
            OneOfLoadIntervalOptionsDef1, OneOfLoadIntervalOptionsDef2, OneOfLoadIntervalOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "loadInterval"})
    mac_address: Optional[
        Union[OneOfMacAddressOptionsDef1, OneOfMacAddressOptionsDef2, OneOfMacAddressOptionsDef3]
    ] = _field(default=None, metadata={"alias": "macAddress"})
    media_type: Optional[
        Union[OneOfMediaTypeOptionsDef1, OneOfMediaTypeOptionsDef2, OneOfMediaTypeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "mediaType"})
    speed: Optional[Union[OneOfSpeedOptionsDef1, OneOfSpeedOptionsDef2, OneOfSpeedOptionsDef3]] = (
        _field(default=None)
    )
    tcp_mss: Optional[
        Union[
            OneOfTcpMssAdjustOptionsDef1, OneOfTcpMssAdjustOptionsDef2, OneOfTcpMssAdjustOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "tcpMss"})


@dataclass
class EthernetData:
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    interface_name: Union[OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    # ACL
    acl: Optional[Acl] = _field(default=None)
    # Advanced Attributes
    advanced: Optional[Advanced] = _field(default=None)
    # Configure ARP entries
    arp: Optional[List[Arp]] = _field(default=None)
    # Configure BFD
    bfd: Optional[Bfd] = _field(default=None)
    dhcp_helper: Optional[
        Union[OneOfListOfIpV4OptionsDef1, OneOfListOfIpV4OptionsDef2, OneOfListOfIpV4OptionsDef3]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    enable_bfd: Optional[
        Union[OneOfEnableBfdOptionsDef1, OneOfEnableBfdOptionsDef2, OneOfEnableBfdOptionsDef3]
    ] = _field(default=None, metadata={"alias": "enableBfd"})
    # Enable HSRP
    hsrp: Optional[Hsrp] = _field(default=None)
    # Enable HSRP Ipv6
    hsrp_ipv6: Optional[HsrpIpv6] = _field(default=None, metadata={"alias": "hsrpIpv6"})
    intf_ip_address: Optional[Union[IntfIpAddress1, IntfIpAddress2]] = _field(
        default=None, metadata={"alias": "intfIpAddress"}
    )
    intf_ip_v6_address: Optional[Union[IntfIpV6Address1, IntfIpV6Address2]] = _field(
        default=None, metadata={"alias": "intfIpV6Address"}
    )
    network_redundancy: Optional[
        Union[OneOfNetworkRedundancyOptionsDef1, OneOfNetworkRedundancyOptionsDef2]
    ] = _field(default=None, metadata={"alias": "networkRedundancy"})
    # Enable VRRP
    vrrp: Optional[Vrrp] = _field(default=None)
    # Enable VRRP Ipv6
    vrrp_ipv6: Optional[VrrpIpv6] = _field(default=None, metadata={"alias": "vrrpIpv6"})


@dataclass
class Payload:
    """
    SD-Routing Service LAN Interface Ethernet feature schema for request
    """

    data: EthernetData
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
    # SD-Routing Service LAN Interface Ethernet feature schema for request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingServiceVrfLanInterfaceEthernetPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingServiceVrfInterfaceEthernetParcelForServicePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class InterfaceEthernetData:
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    interface_name: Union[OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    # ACL
    acl: Optional[Acl] = _field(default=None)
    # Advanced Attributes
    advanced: Optional[Advanced] = _field(default=None)
    # Configure ARP entries
    arp: Optional[List[Arp]] = _field(default=None)
    # Configure BFD
    bfd: Optional[Bfd] = _field(default=None)
    dhcp_helper: Optional[
        Union[OneOfListOfIpV4OptionsDef1, OneOfListOfIpV4OptionsDef2, OneOfListOfIpV4OptionsDef3]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    enable_bfd: Optional[
        Union[OneOfEnableBfdOptionsDef1, OneOfEnableBfdOptionsDef2, OneOfEnableBfdOptionsDef3]
    ] = _field(default=None, metadata={"alias": "enableBfd"})
    # Enable HSRP
    hsrp: Optional[Hsrp] = _field(default=None)
    # Enable HSRP Ipv6
    hsrp_ipv6: Optional[HsrpIpv6] = _field(default=None, metadata={"alias": "hsrpIpv6"})
    intf_ip_address: Optional[Union[IntfIpAddress1, IntfIpAddress2]] = _field(
        default=None, metadata={"alias": "intfIpAddress"}
    )
    intf_ip_v6_address: Optional[Union[IntfIpV6Address1, IntfIpV6Address2]] = _field(
        default=None, metadata={"alias": "intfIpV6Address"}
    )
    network_redundancy: Optional[
        Union[OneOfNetworkRedundancyOptionsDef1, OneOfNetworkRedundancyOptionsDef2]
    ] = _field(default=None, metadata={"alias": "networkRedundancy"})
    # Enable VRRP
    vrrp: Optional[Vrrp] = _field(default=None)
    # Enable VRRP Ipv6
    vrrp_ipv6: Optional[VrrpIpv6] = _field(default=None, metadata={"alias": "vrrpIpv6"})


@dataclass
class CreateSdroutingServiceVrfInterfaceEthernetParcelForServicePostRequest:
    """
    SD-Routing Service LAN Interface Ethernet feature schema for request
    """

    data: InterfaceEthernetData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingServiceVrfLanInterfaceEthernetPayload:
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
    # SD-Routing Service LAN Interface Ethernet feature schema for request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingServiceVrfInterfaceEthernetParcelForServicePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class VrfInterfaceEthernetData:
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    interface_name: Union[OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    # ACL
    acl: Optional[Acl] = _field(default=None)
    # Advanced Attributes
    advanced: Optional[Advanced] = _field(default=None)
    # Configure ARP entries
    arp: Optional[List[Arp]] = _field(default=None)
    # Configure BFD
    bfd: Optional[Bfd] = _field(default=None)
    dhcp_helper: Optional[
        Union[OneOfListOfIpV4OptionsDef1, OneOfListOfIpV4OptionsDef2, OneOfListOfIpV4OptionsDef3]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    enable_bfd: Optional[
        Union[OneOfEnableBfdOptionsDef1, OneOfEnableBfdOptionsDef2, OneOfEnableBfdOptionsDef3]
    ] = _field(default=None, metadata={"alias": "enableBfd"})
    # Enable HSRP
    hsrp: Optional[Hsrp] = _field(default=None)
    # Enable HSRP Ipv6
    hsrp_ipv6: Optional[HsrpIpv6] = _field(default=None, metadata={"alias": "hsrpIpv6"})
    intf_ip_address: Optional[Union[IntfIpAddress1, IntfIpAddress2]] = _field(
        default=None, metadata={"alias": "intfIpAddress"}
    )
    intf_ip_v6_address: Optional[Union[IntfIpV6Address1, IntfIpV6Address2]] = _field(
        default=None, metadata={"alias": "intfIpV6Address"}
    )
    network_redundancy: Optional[
        Union[OneOfNetworkRedundancyOptionsDef1, OneOfNetworkRedundancyOptionsDef2]
    ] = _field(default=None, metadata={"alias": "networkRedundancy"})
    # Enable VRRP
    vrrp: Optional[Vrrp] = _field(default=None)
    # Enable VRRP Ipv6
    vrrp_ipv6: Optional[VrrpIpv6] = _field(default=None, metadata={"alias": "vrrpIpv6"})


@dataclass
class EditSdroutingServiceVrfInterfaceEthernetParcelForServicePutRequest:
    """
    SD-Routing Service LAN Interface Ethernet feature schema for request
    """

    data: VrfInterfaceEthernetData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
