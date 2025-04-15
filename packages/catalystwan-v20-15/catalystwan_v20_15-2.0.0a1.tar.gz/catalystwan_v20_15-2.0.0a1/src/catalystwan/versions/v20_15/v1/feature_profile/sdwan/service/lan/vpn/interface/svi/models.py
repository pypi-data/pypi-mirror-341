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

Ipv4VrrpTrackingObjectTrackActionDef = Literal["decrement", "shutdown"]

SviIpv4VrrpTrackingObjectTrackActionDef = Literal["decrement", "shutdown"]

InterfaceSviIpv4VrrpTrackingObjectTrackActionDef = Literal["decrement", "shutdown"]

VpnInterfaceSviIpv4VrrpTrackingObjectTrackActionDef = Literal["decrement", "shutdown"]

LanVpnInterfaceSviIpv4VrrpTrackingObjectTrackActionDef = Literal["decrement", "shutdown"]


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
class OneOfIfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIfNameOptionsDef2:
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
class OneOfIfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIfMtuOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


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
class AddressV4:
    """
    IpV4Address Primary
    """

    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class SecondaryAddressV4:
    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class OneOfDhcpHelperV4OptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfDhcpHelperV4OptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDhcpHelperV4OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Ipv4:
    """
    ipv4 Attributes
    """

    # IpV4Address Primary
    address_v4: AddressV4 = _field(metadata={"alias": "addressV4"})
    dhcp_helper_v4: Optional[
        Union[
            OneOfDhcpHelperV4OptionsDef1, OneOfDhcpHelperV4OptionsDef2, OneOfDhcpHelperV4OptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "dhcpHelperV4"})
    # Assign secondary IP addresses
    secondary_address_v4: Optional[List[SecondaryAddressV4]] = _field(
        default=None, metadata={"alias": "secondaryAddressV4"}
    )


@dataclass
class OneOfAddressV6OptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAddressV6OptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAddressV6OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSecondaryAddressV6AddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSecondaryAddressV6AddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSecondaryAddressV6AddressOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class SecondaryAddressV6:
    address: Union[
        OneOfSecondaryAddressV6AddressOptionsDef1,
        OneOfSecondaryAddressV6AddressOptionsDef2,
        OneOfSecondaryAddressV6AddressOptionsDef3,
    ]


@dataclass
class OneOfDhcpHelperV6AddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDhcpHelperV6AddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDhcpHelperV6VpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDhcpHelperV6VpnOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDhcpHelperV6VpnOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class DhcpHelperV6:
    address: Union[OneOfDhcpHelperV6AddressOptionsDef1, OneOfDhcpHelperV6AddressOptionsDef2]
    vpn: Optional[
        Union[
            OneOfDhcpHelperV6VpnOptionsDef1,
            OneOfDhcpHelperV6VpnOptionsDef2,
            OneOfDhcpHelperV6VpnOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class Ipv6:
    """
    Advanced Attributes
    """

    address_v6: Optional[
        Union[OneOfAddressV6OptionsDef1, OneOfAddressV6OptionsDef2, OneOfAddressV6OptionsDef3]
    ] = _field(default=None, metadata={"alias": "addressV6"})
    # DHCPv6 Helper
    dhcp_helper_v6: Optional[List[DhcpHelperV6]] = _field(
        default=None, metadata={"alias": "dhcpHelperV6"}
    )
    # Assign secondary IPv6 addresses
    secondary_address_v6: Optional[List[SecondaryAddressV6]] = _field(
        default=None, metadata={"alias": "secondaryAddressV6"}
    )


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
class AclQos:
    """
    ACL
    """

    ipv4_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclEgress"}
    )
    ipv4_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclIngress"}
    )
    ipv6_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6AclEgress"}
    )
    ipv6_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6AclIngress"}
    )


@dataclass
class OneOfArpAddrOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfArpAddrOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfArpMacOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfArpMacOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Arp:
    ip_address: Union[OneOfArpAddrOptionsDef1, OneOfArpAddrOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    mac_address: Union[OneOfArpMacOptionsDef1, OneOfArpMacOptionsDef2] = _field(
        metadata={"alias": "macAddress"}
    )


@dataclass
class OneOfIpv4VrrpGrpIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv4VrrpGrpIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4VrrpPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv4VrrpPriorityOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4VrrpPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv4VrrpTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv4VrrpTimerOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4VrrpTimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv4VrrpTrackOmpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpv4VrrpTrackOmpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4VrrpTrackOmpOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpv4VrrpTrackPrefixListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv4VrrpTrackPrefixListOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4VrrpTrackPrefixListOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


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
class OneOfIpv4VrrpIpv4SecondaryAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfIpv4VrrpIpv4SecondaryAddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class IpAddressSecondary:
    address: Union[
        OneOfIpv4VrrpIpv4SecondaryAddressOptionsDef1, OneOfIpv4VrrpIpv4SecondaryAddressOptionsDef2
    ]


@dataclass
class OneOfIpv4VrrpTlocChangePrefOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpv4VrrpTlocChangePrefOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class TlocPrefChangeValue:
    value: Optional[Any] = _field(default=None)


@dataclass
class OneOfIpv4VrrpTrackingObjectNameOptionsDef1:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpv4VrrpTrackingObjectNameOptionsDef2:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class OneOfIpv4VrrpTrackingObjectTrackActionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4VrrpTrackingObjectTrackActionDef


@dataclass
class OneOfIpv4VrrpTrackingObjectTrackActionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4VrrpTrackingObjectDecrementOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv4VrrpTrackingObjectDecrementOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class TrackingObject:
    track_action: Union[
        OneOfIpv4VrrpTrackingObjectTrackActionOptionsDef1,
        OneOfIpv4VrrpTrackingObjectTrackActionOptionsDef2,
    ] = _field(metadata={"alias": "trackAction"})
    tracker_id: Union[
        OneOfIpv4VrrpTrackingObjectNameOptionsDef1, OneOfIpv4VrrpTrackingObjectNameOptionsDef2
    ] = _field(metadata={"alias": "trackerId"})
    decrement_value: Optional[
        Union[
            OneOfIpv4VrrpTrackingObjectDecrementOptionsDef1,
            OneOfIpv4VrrpTrackingObjectDecrementOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "decrementValue"})


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
class Vrrp1:
    group_id: Union[OneOfIpv4VrrpGrpIdOptionsDef1, OneOfIpv4VrrpGrpIdOptionsDef2]
    ip_address: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipAddress"})
    priority: Union[
        OneOfIpv4VrrpPriorityOptionsDef1,
        OneOfIpv4VrrpPriorityOptionsDef2,
        OneOfIpv4VrrpPriorityOptionsDef3,
    ]
    timer: Union[
        OneOfIpv4VrrpTimerOptionsDef1, OneOfIpv4VrrpTimerOptionsDef2, OneOfIpv4VrrpTimerOptionsDef3
    ]
    tloc_pref_change: Union[
        OneOfIpv4VrrpTlocChangePrefOptionsDef1, OneOfIpv4VrrpTlocChangePrefOptionsDef2
    ] = _field(metadata={"alias": "tlocPrefChange"})
    track_omp: Union[
        OneOfIpv4VrrpTrackOmpOptionsDef1,
        OneOfIpv4VrrpTrackOmpOptionsDef2,
        OneOfIpv4VrrpTrackOmpOptionsDef3,
    ] = _field(metadata={"alias": "trackOmp"})
    follow_dual_router_ha_availability: Optional[
        Union[
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef1,
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "followDualRouterHAAvailability"})
    # VRRP Secondary IPV4 address
    ip_address_secondary: Optional[List[IpAddressSecondary]] = _field(
        default=None, metadata={"alias": "ipAddressSecondary"}
    )
    prefix_list: Optional[
        Union[
            OneOfIpv4VrrpTrackPrefixListOptionsDef1,
            OneOfIpv4VrrpTrackPrefixListOptionsDef2,
            OneOfIpv4VrrpTrackPrefixListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "prefixList"})
    tloc_pref_change_value: Optional[TlocPrefChangeValue] = _field(
        default=None, metadata={"alias": "tlocPrefChangeValue"}
    )
    # tracking object for VRRP configuration
    tracking_object: Optional[List[TrackingObject]] = _field(
        default=None, metadata={"alias": "trackingObject"}
    )


@dataclass
class OneOfIpv4VrrpValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv4VrrpValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Vrrp2:
    group_id: Union[OneOfIpv4VrrpGrpIdOptionsDef1, OneOfIpv4VrrpGrpIdOptionsDef2]
    ip_address: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipAddress"})
    priority: Union[
        OneOfIpv4VrrpPriorityOptionsDef1,
        OneOfIpv4VrrpPriorityOptionsDef2,
        OneOfIpv4VrrpPriorityOptionsDef3,
    ]
    timer: Union[
        OneOfIpv4VrrpTimerOptionsDef1, OneOfIpv4VrrpTimerOptionsDef2, OneOfIpv4VrrpTimerOptionsDef3
    ]
    tloc_pref_change: Union[
        OneOfIpv4VrrpTlocChangePrefOptionsDef1, OneOfIpv4VrrpTlocChangePrefOptionsDef2
    ] = _field(metadata={"alias": "tlocPrefChange"})
    track_omp: Union[
        OneOfIpv4VrrpTrackOmpOptionsDef1,
        OneOfIpv4VrrpTrackOmpOptionsDef2,
        OneOfIpv4VrrpTrackOmpOptionsDef3,
    ] = _field(metadata={"alias": "trackOmp"})
    follow_dual_router_ha_availability: Optional[
        Union[
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef1,
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "followDualRouterHAAvailability"})
    # VRRP Secondary IPV4 address
    ip_address_secondary: Optional[List[IpAddressSecondary]] = _field(
        default=None, metadata={"alias": "ipAddressSecondary"}
    )
    prefix_list: Optional[
        Union[
            OneOfIpv4VrrpTrackPrefixListOptionsDef1,
            OneOfIpv4VrrpTrackPrefixListOptionsDef2,
            OneOfIpv4VrrpTrackPrefixListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "prefixList"})
    tloc_pref_change_value: Optional[
        Union[OneOfIpv4VrrpValueOptionsDef1, OneOfIpv4VrrpValueOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tlocPrefChangeValue"})
    # tracking object for VRRP configuration
    tracking_object: Optional[List[TrackingObject]] = _field(
        default=None, metadata={"alias": "trackingObject"}
    )


@dataclass
class OneOfIpv6VrrpGrpIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv6VrrpGrpIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6VrrpPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv6VrrpPriorityOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6VrrpPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv6VrrpTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv6VrrpTimerOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6VrrpTimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv6VrrpTrackOmpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpv6VrrpTrackOmpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6VrrpTrackOmpOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpv6VrrpTrackPrefixListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6VrrpTrackPrefixListOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6VrrpTrackPrefixListOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


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
class SviIpv6:
    ipv6_link_local: Union[
        OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef1, OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef2
    ] = _field(metadata={"alias": "ipv6LinkLocal"})
    prefix: Optional[
        Union[
            OneOfIpv6VrrpIpv6PrefixOptionsDef1,
            OneOfIpv6VrrpIpv6PrefixOptionsDef2,
            OneOfIpv6VrrpIpv6PrefixOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfIpv6VrrpIpv6SecondaryPrefixOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6VrrpIpv6SecondaryPrefixOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Ipv6Secondary:
    prefix: Union[
        OneOfIpv6VrrpIpv6SecondaryPrefixOptionsDef1, OneOfIpv6VrrpIpv6SecondaryPrefixOptionsDef2
    ]


@dataclass
class VrrpIpv6:
    group_id: Union[OneOfIpv6VrrpGrpIdOptionsDef1, OneOfIpv6VrrpGrpIdOptionsDef2] = _field(
        metadata={"alias": "groupId"}
    )
    # IPv6 VRRP
    ipv6: List[SviIpv6]
    priority: Union[
        OneOfIpv6VrrpPriorityOptionsDef1,
        OneOfIpv6VrrpPriorityOptionsDef2,
        OneOfIpv6VrrpPriorityOptionsDef3,
    ]
    timer: Union[
        OneOfIpv6VrrpTimerOptionsDef1, OneOfIpv6VrrpTimerOptionsDef2, OneOfIpv6VrrpTimerOptionsDef3
    ]
    track_omp: Union[
        OneOfIpv6VrrpTrackOmpOptionsDef1,
        OneOfIpv6VrrpTrackOmpOptionsDef2,
        OneOfIpv6VrrpTrackOmpOptionsDef3,
    ] = _field(metadata={"alias": "trackOmp"})
    follow_dual_router_ha_availability: Optional[
        Union[
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef1,
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "followDualRouterHAAvailability"})
    # IPv6 Secondary IP address
    ipv6_secondary: Optional[List[Ipv6Secondary]] = _field(
        default=None, metadata={"alias": "ipv6Secondary"}
    )
    track_prefix_list: Optional[
        Union[
            OneOfIpv6VrrpTrackPrefixListOptionsDef1,
            OneOfIpv6VrrpTrackPrefixListOptionsDef2,
            OneOfIpv6VrrpTrackPrefixListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackPrefixList"})


@dataclass
class OneOfDhcpClientV6OptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDhcpClientV6OptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDhcpClientV6OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTcpMssOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTcpMssOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTcpMssOptionsDef3:
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
class OneOfIcmpRedirectDisableOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIcmpRedirectDisableOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIcmpRedirectDisableOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Advanced:
    """
    Advanced Attributes
    """

    arp_timeout: Union[
        OneOfArpTimeoutOptionsDef1, OneOfArpTimeoutOptionsDef2, OneOfArpTimeoutOptionsDef3
    ] = _field(metadata={"alias": "arpTimeout"})
    ip_directed_broadcast: Union[
        OneOfIpDirectedBroadcastOptionsDef1,
        OneOfIpDirectedBroadcastOptionsDef2,
        OneOfIpDirectedBroadcastOptionsDef3,
    ] = _field(metadata={"alias": "ipDirectedBroadcast"})
    icmp_redirect_disable: Optional[
        Union[
            OneOfIcmpRedirectDisableOptionsDef1,
            OneOfIcmpRedirectDisableOptionsDef2,
            OneOfIcmpRedirectDisableOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "icmpRedirectDisable"})
    tcp_mss: Optional[
        Union[OneOfTcpMssOptionsDef1, OneOfTcpMssOptionsDef2, OneOfTcpMssOptionsDef3]
    ] = _field(default=None, metadata={"alias": "tcpMss"})


@dataclass
class SviData:
    # Advanced Attributes
    advanced: Advanced
    interface_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    # ACL
    acl_qos: Optional[AclQos] = _field(default=None, metadata={"alias": "aclQos"})
    # Configure static ARP entries
    arp: Optional[List[Arp]] = _field(default=None)
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)
    dhcp_client_v6: Optional[
        Union[
            OneOfDhcpClientV6OptionsDef1, OneOfDhcpClientV6OptionsDef2, OneOfDhcpClientV6OptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "dhcpClientV6"})
    if_mtu: Optional[Union[OneOfIfMtuOptionsDef1, OneOfIfMtuOptionsDef2, OneOfIfMtuOptionsDef3]] = (
        _field(default=None, metadata={"alias": "ifMtu"})
    )
    ip_mtu: Optional[Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3]] = _field(
        default=None, metadata={"alias": "ipMtu"}
    )
    # ipv4 Attributes
    ipv4: Optional[Ipv4] = _field(default=None)
    # Advanced Attributes
    ipv6: Optional[Ipv6] = _field(default=None)
    # Enable ipv4 VRRP
    vrrp: Optional[List[Union[Vrrp1, Vrrp2]]] = _field(default=None)
    # Enable ipv6 VRRP
    vrrp_ipv6: Optional[List[VrrpIpv6]] = _field(default=None, metadata={"alias": "vrrpIpv6"})


@dataclass
class Payload:
    """
    LAN VPN Interface SVI profile parcel schema for POST request
    """

    data: SviData
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
    # LAN VPN Interface SVI profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanServiceLanVpnInterfaceSviPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateLanVpnInterfaceSviParcelForServicePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class InterfaceSviData:
    # Advanced Attributes
    advanced: Advanced
    interface_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    # ACL
    acl_qos: Optional[AclQos] = _field(default=None, metadata={"alias": "aclQos"})
    # Configure static ARP entries
    arp: Optional[List[Arp]] = _field(default=None)
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)
    dhcp_client_v6: Optional[
        Union[
            OneOfDhcpClientV6OptionsDef1, OneOfDhcpClientV6OptionsDef2, OneOfDhcpClientV6OptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "dhcpClientV6"})
    if_mtu: Optional[Union[OneOfIfMtuOptionsDef1, OneOfIfMtuOptionsDef2, OneOfIfMtuOptionsDef3]] = (
        _field(default=None, metadata={"alias": "ifMtu"})
    )
    ip_mtu: Optional[Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3]] = _field(
        default=None, metadata={"alias": "ipMtu"}
    )
    # ipv4 Attributes
    ipv4: Optional[Ipv4] = _field(default=None)
    # Advanced Attributes
    ipv6: Optional[Ipv6] = _field(default=None)
    # Enable ipv4 VRRP
    vrrp: Optional[List[Union[Vrrp1, Vrrp2]]] = _field(default=None)
    # Enable ipv6 VRRP
    vrrp_ipv6: Optional[List[VrrpIpv6]] = _field(default=None, metadata={"alias": "vrrpIpv6"})


@dataclass
class CreateLanVpnInterfaceSviParcelForServicePostRequest:
    """
    LAN VPN Interface SVI profile parcel schema for POST request
    """

    data: InterfaceSviData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class SviOneOfIfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SviOneOfDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SviOneOfIfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfIfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfDhcpHelperV4OptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class SviIpv4:
    """
    ipv4 Attributes
    """

    # IpV4Address Primary
    address_v4: AddressV4 = _field(metadata={"alias": "addressV4"})
    dhcp_helper_v4: Optional[
        Union[
            SviOneOfDhcpHelperV4OptionsDef1,
            OneOfDhcpHelperV4OptionsDef2,
            OneOfDhcpHelperV4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dhcpHelperV4"})
    # Assign secondary IP addresses
    secondary_address_v4: Optional[List[SecondaryAddressV4]] = _field(
        default=None, metadata={"alias": "secondaryAddressV4"}
    )


@dataclass
class SviSecondaryAddressV6:
    address: Union[
        OneOfSecondaryAddressV6AddressOptionsDef1,
        OneOfSecondaryAddressV6AddressOptionsDef2,
        OneOfSecondaryAddressV6AddressOptionsDef3,
    ]


@dataclass
class SviOneOfDhcpHelperV6VpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviDhcpHelperV6:
    address: Union[OneOfDhcpHelperV6AddressOptionsDef1, OneOfDhcpHelperV6AddressOptionsDef2]
    vpn: Optional[
        Union[
            SviOneOfDhcpHelperV6VpnOptionsDef1,
            OneOfDhcpHelperV6VpnOptionsDef2,
            OneOfDhcpHelperV6VpnOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class InterfaceSviIpv6:
    """
    Advanced Attributes
    """

    address_v6: Optional[
        Union[OneOfAddressV6OptionsDef1, OneOfAddressV6OptionsDef2, OneOfAddressV6OptionsDef3]
    ] = _field(default=None, metadata={"alias": "addressV6"})
    # DHCPv6 Helper
    dhcp_helper_v6: Optional[List[SviDhcpHelperV6]] = _field(
        default=None, metadata={"alias": "dhcpHelperV6"}
    )
    # Assign secondary IPv6 addresses
    secondary_address_v6: Optional[List[SviSecondaryAddressV6]] = _field(
        default=None, metadata={"alias": "secondaryAddressV6"}
    )


@dataclass
class SviOneOfArpMacOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SviArp:
    ip_address: Union[OneOfArpAddrOptionsDef1, OneOfArpAddrOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    mac_address: Union[SviOneOfArpMacOptionsDef1, OneOfArpMacOptionsDef2] = _field(
        metadata={"alias": "macAddress"}
    )


@dataclass
class SviOneOfIpv4VrrpGrpIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfIpv4VrrpPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfIpv4VrrpPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfIpv4VrrpTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfIpv4VrrpTimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfIpv4VrrpTrackPrefixListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SviIpAddressSecondary:
    address: Union[
        OneOfIpv4VrrpIpv4SecondaryAddressOptionsDef1, OneOfIpv4VrrpIpv4SecondaryAddressOptionsDef2
    ]


@dataclass
class SviOneOfIpv4VrrpTrackingObjectTrackActionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SviIpv4VrrpTrackingObjectTrackActionDef


@dataclass
class SviOneOfIpv4VrrpTrackingObjectDecrementOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviTrackingObject:
    track_action: Union[
        SviOneOfIpv4VrrpTrackingObjectTrackActionOptionsDef1,
        OneOfIpv4VrrpTrackingObjectTrackActionOptionsDef2,
    ] = _field(metadata={"alias": "trackAction"})
    tracker_id: Union[
        OneOfIpv4VrrpTrackingObjectNameOptionsDef1, OneOfIpv4VrrpTrackingObjectNameOptionsDef2
    ] = _field(metadata={"alias": "trackerId"})
    decrement_value: Optional[
        Union[
            SviOneOfIpv4VrrpTrackingObjectDecrementOptionsDef1,
            OneOfIpv4VrrpTrackingObjectDecrementOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "decrementValue"})


@dataclass
class SviVrrp1:
    group_id: Union[SviOneOfIpv4VrrpGrpIdOptionsDef1, OneOfIpv4VrrpGrpIdOptionsDef2]
    ip_address: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipAddress"})
    priority: Union[
        SviOneOfIpv4VrrpPriorityOptionsDef1,
        OneOfIpv4VrrpPriorityOptionsDef2,
        SviOneOfIpv4VrrpPriorityOptionsDef3,
    ]
    timer: Union[
        SviOneOfIpv4VrrpTimerOptionsDef1,
        OneOfIpv4VrrpTimerOptionsDef2,
        SviOneOfIpv4VrrpTimerOptionsDef3,
    ]
    tloc_pref_change: Union[
        OneOfIpv4VrrpTlocChangePrefOptionsDef1, OneOfIpv4VrrpTlocChangePrefOptionsDef2
    ] = _field(metadata={"alias": "tlocPrefChange"})
    track_omp: Union[
        OneOfIpv4VrrpTrackOmpOptionsDef1,
        OneOfIpv4VrrpTrackOmpOptionsDef2,
        OneOfIpv4VrrpTrackOmpOptionsDef3,
    ] = _field(metadata={"alias": "trackOmp"})
    follow_dual_router_ha_availability: Optional[
        Union[
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef1,
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "followDualRouterHAAvailability"})
    # VRRP Secondary IPV4 address
    ip_address_secondary: Optional[List[SviIpAddressSecondary]] = _field(
        default=None, metadata={"alias": "ipAddressSecondary"}
    )
    prefix_list: Optional[
        Union[
            SviOneOfIpv4VrrpTrackPrefixListOptionsDef1,
            OneOfIpv4VrrpTrackPrefixListOptionsDef2,
            OneOfIpv4VrrpTrackPrefixListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "prefixList"})
    tloc_pref_change_value: Optional[TlocPrefChangeValue] = _field(
        default=None, metadata={"alias": "tlocPrefChangeValue"}
    )
    # tracking object for VRRP configuration
    tracking_object: Optional[List[SviTrackingObject]] = _field(
        default=None, metadata={"alias": "trackingObject"}
    )


@dataclass
class InterfaceSviOneOfIpv4VrrpGrpIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfIpv4VrrpPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfIpv4VrrpPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfIpv4VrrpTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfIpv4VrrpTimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfIpv4VrrpTrackPrefixListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceSviIpAddressSecondary:
    address: Union[
        OneOfIpv4VrrpIpv4SecondaryAddressOptionsDef1, OneOfIpv4VrrpIpv4SecondaryAddressOptionsDef2
    ]


@dataclass
class SviOneOfIpv4VrrpValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfIpv4VrrpTrackingObjectTrackActionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceSviIpv4VrrpTrackingObjectTrackActionDef


@dataclass
class InterfaceSviOneOfIpv4VrrpTrackingObjectDecrementOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviTrackingObject:
    track_action: Union[
        InterfaceSviOneOfIpv4VrrpTrackingObjectTrackActionOptionsDef1,
        OneOfIpv4VrrpTrackingObjectTrackActionOptionsDef2,
    ] = _field(metadata={"alias": "trackAction"})
    tracker_id: Union[
        OneOfIpv4VrrpTrackingObjectNameOptionsDef1, OneOfIpv4VrrpTrackingObjectNameOptionsDef2
    ] = _field(metadata={"alias": "trackerId"})
    decrement_value: Optional[
        Union[
            InterfaceSviOneOfIpv4VrrpTrackingObjectDecrementOptionsDef1,
            OneOfIpv4VrrpTrackingObjectDecrementOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "decrementValue"})


@dataclass
class SviVrrp2:
    group_id: Union[InterfaceSviOneOfIpv4VrrpGrpIdOptionsDef1, OneOfIpv4VrrpGrpIdOptionsDef2]
    ip_address: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipAddress"})
    priority: Union[
        InterfaceSviOneOfIpv4VrrpPriorityOptionsDef1,
        OneOfIpv4VrrpPriorityOptionsDef2,
        InterfaceSviOneOfIpv4VrrpPriorityOptionsDef3,
    ]
    timer: Union[
        InterfaceSviOneOfIpv4VrrpTimerOptionsDef1,
        OneOfIpv4VrrpTimerOptionsDef2,
        InterfaceSviOneOfIpv4VrrpTimerOptionsDef3,
    ]
    tloc_pref_change: Union[
        OneOfIpv4VrrpTlocChangePrefOptionsDef1, OneOfIpv4VrrpTlocChangePrefOptionsDef2
    ] = _field(metadata={"alias": "tlocPrefChange"})
    track_omp: Union[
        OneOfIpv4VrrpTrackOmpOptionsDef1,
        OneOfIpv4VrrpTrackOmpOptionsDef2,
        OneOfIpv4VrrpTrackOmpOptionsDef3,
    ] = _field(metadata={"alias": "trackOmp"})
    follow_dual_router_ha_availability: Optional[
        Union[
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef1,
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "followDualRouterHAAvailability"})
    # VRRP Secondary IPV4 address
    ip_address_secondary: Optional[List[InterfaceSviIpAddressSecondary]] = _field(
        default=None, metadata={"alias": "ipAddressSecondary"}
    )
    prefix_list: Optional[
        Union[
            InterfaceSviOneOfIpv4VrrpTrackPrefixListOptionsDef1,
            OneOfIpv4VrrpTrackPrefixListOptionsDef2,
            OneOfIpv4VrrpTrackPrefixListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "prefixList"})
    tloc_pref_change_value: Optional[
        Union[SviOneOfIpv4VrrpValueOptionsDef1, OneOfIpv4VrrpValueOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tlocPrefChangeValue"})
    # tracking object for VRRP configuration
    tracking_object: Optional[List[InterfaceSviTrackingObject]] = _field(
        default=None, metadata={"alias": "trackingObject"}
    )


@dataclass
class SviOneOfIpv6VrrpGrpIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfIpv6VrrpPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfIpv6VrrpPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfIpv6VrrpTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfIpv6VrrpTimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfIpv6VrrpTrackPrefixListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnInterfaceSviIpv6:
    ipv6_link_local: Union[
        OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef1, OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef2
    ] = _field(metadata={"alias": "ipv6LinkLocal"})
    prefix: Optional[
        Union[
            OneOfIpv6VrrpIpv6PrefixOptionsDef1,
            OneOfIpv6VrrpIpv6PrefixOptionsDef2,
            OneOfIpv6VrrpIpv6PrefixOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class SviIpv6Secondary:
    prefix: Union[
        OneOfIpv6VrrpIpv6SecondaryPrefixOptionsDef1, OneOfIpv6VrrpIpv6SecondaryPrefixOptionsDef2
    ]


@dataclass
class SviVrrpIpv6:
    group_id: Union[SviOneOfIpv6VrrpGrpIdOptionsDef1, OneOfIpv6VrrpGrpIdOptionsDef2] = _field(
        metadata={"alias": "groupId"}
    )
    # IPv6 VRRP
    ipv6: List[VpnInterfaceSviIpv6]
    priority: Union[
        SviOneOfIpv6VrrpPriorityOptionsDef1,
        OneOfIpv6VrrpPriorityOptionsDef2,
        SviOneOfIpv6VrrpPriorityOptionsDef3,
    ]
    timer: Union[
        SviOneOfIpv6VrrpTimerOptionsDef1,
        OneOfIpv6VrrpTimerOptionsDef2,
        SviOneOfIpv6VrrpTimerOptionsDef3,
    ]
    track_omp: Union[
        OneOfIpv6VrrpTrackOmpOptionsDef1,
        OneOfIpv6VrrpTrackOmpOptionsDef2,
        OneOfIpv6VrrpTrackOmpOptionsDef3,
    ] = _field(metadata={"alias": "trackOmp"})
    follow_dual_router_ha_availability: Optional[
        Union[
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef1,
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "followDualRouterHAAvailability"})
    # IPv6 Secondary IP address
    ipv6_secondary: Optional[List[SviIpv6Secondary]] = _field(
        default=None, metadata={"alias": "ipv6Secondary"}
    )
    track_prefix_list: Optional[
        Union[
            SviOneOfIpv6VrrpTrackPrefixListOptionsDef1,
            OneOfIpv6VrrpTrackPrefixListOptionsDef2,
            OneOfIpv6VrrpTrackPrefixListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackPrefixList"})


@dataclass
class SviOneOfTcpMssOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfArpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviOneOfArpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SviAdvanced:
    """
    Advanced Attributes
    """

    arp_timeout: Union[
        SviOneOfArpTimeoutOptionsDef1, OneOfArpTimeoutOptionsDef2, SviOneOfArpTimeoutOptionsDef3
    ] = _field(metadata={"alias": "arpTimeout"})
    ip_directed_broadcast: Union[
        OneOfIpDirectedBroadcastOptionsDef1,
        OneOfIpDirectedBroadcastOptionsDef2,
        OneOfIpDirectedBroadcastOptionsDef3,
    ] = _field(metadata={"alias": "ipDirectedBroadcast"})
    icmp_redirect_disable: Optional[
        Union[
            OneOfIcmpRedirectDisableOptionsDef1,
            OneOfIcmpRedirectDisableOptionsDef2,
            OneOfIcmpRedirectDisableOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "icmpRedirectDisable"})
    tcp_mss: Optional[
        Union[SviOneOfTcpMssOptionsDef1, OneOfTcpMssOptionsDef2, OneOfTcpMssOptionsDef3]
    ] = _field(default=None, metadata={"alias": "tcpMss"})


@dataclass
class VpnInterfaceSviData:
    # Advanced Attributes
    advanced: SviAdvanced
    interface_name: Union[SviOneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    # ACL
    acl_qos: Optional[AclQos] = _field(default=None, metadata={"alias": "aclQos"})
    # Configure static ARP entries
    arp: Optional[List[SviArp]] = _field(default=None)
    description: Optional[
        Union[
            SviOneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
        ]
    ] = _field(default=None)
    dhcp_client_v6: Optional[
        Union[
            OneOfDhcpClientV6OptionsDef1, OneOfDhcpClientV6OptionsDef2, OneOfDhcpClientV6OptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "dhcpClientV6"})
    if_mtu: Optional[
        Union[SviOneOfIfMtuOptionsDef1, OneOfIfMtuOptionsDef2, SviOneOfIfMtuOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ifMtu"})
    ip_mtu: Optional[Union[SviOneOfMtuOptionsDef1, OneOfMtuOptionsDef2, SviOneOfMtuOptionsDef3]] = (
        _field(default=None, metadata={"alias": "ipMtu"})
    )
    # ipv4 Attributes
    ipv4: Optional[SviIpv4] = _field(default=None)
    # Advanced Attributes
    ipv6: Optional[InterfaceSviIpv6] = _field(default=None)
    # Enable ipv4 VRRP
    vrrp: Optional[List[Union[SviVrrp1, SviVrrp2]]] = _field(default=None)
    # Enable ipv6 VRRP
    vrrp_ipv6: Optional[List[SviVrrpIpv6]] = _field(default=None, metadata={"alias": "vrrpIpv6"})


@dataclass
class SviPayload:
    """
    LAN VPN Interface SVI profile parcel schema for PUT request
    """

    data: VpnInterfaceSviData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanServiceLanVpnInterfaceSviPayload:
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
    # LAN VPN Interface SVI profile parcel schema for PUT request
    payload: Optional[SviPayload] = _field(default=None)


@dataclass
class EditLanVpnInterfaceSviParcelForServicePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class InterfaceSviOneOfIfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceSviOneOfDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceSviOneOfIfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfIfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfDhcpHelperV4OptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class InterfaceSviIpv4:
    """
    ipv4 Attributes
    """

    # IpV4Address Primary
    address_v4: AddressV4 = _field(metadata={"alias": "addressV4"})
    dhcp_helper_v4: Optional[
        Union[
            InterfaceSviOneOfDhcpHelperV4OptionsDef1,
            OneOfDhcpHelperV4OptionsDef2,
            OneOfDhcpHelperV4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dhcpHelperV4"})
    # Assign secondary IP addresses
    secondary_address_v4: Optional[List[SecondaryAddressV4]] = _field(
        default=None, metadata={"alias": "secondaryAddressV4"}
    )


@dataclass
class InterfaceSviSecondaryAddressV6:
    address: Union[
        OneOfSecondaryAddressV6AddressOptionsDef1,
        OneOfSecondaryAddressV6AddressOptionsDef2,
        OneOfSecondaryAddressV6AddressOptionsDef3,
    ]


@dataclass
class InterfaceSviOneOfDhcpHelperV6VpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviDhcpHelperV6:
    address: Union[OneOfDhcpHelperV6AddressOptionsDef1, OneOfDhcpHelperV6AddressOptionsDef2]
    vpn: Optional[
        Union[
            InterfaceSviOneOfDhcpHelperV6VpnOptionsDef1,
            OneOfDhcpHelperV6VpnOptionsDef2,
            OneOfDhcpHelperV6VpnOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class LanVpnInterfaceSviIpv6:
    """
    Advanced Attributes
    """

    address_v6: Optional[
        Union[OneOfAddressV6OptionsDef1, OneOfAddressV6OptionsDef2, OneOfAddressV6OptionsDef3]
    ] = _field(default=None, metadata={"alias": "addressV6"})
    # DHCPv6 Helper
    dhcp_helper_v6: Optional[List[InterfaceSviDhcpHelperV6]] = _field(
        default=None, metadata={"alias": "dhcpHelperV6"}
    )
    # Assign secondary IPv6 addresses
    secondary_address_v6: Optional[List[InterfaceSviSecondaryAddressV6]] = _field(
        default=None, metadata={"alias": "secondaryAddressV6"}
    )


@dataclass
class InterfaceSviOneOfArpMacOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class InterfaceSviArp:
    ip_address: Union[OneOfArpAddrOptionsDef1, OneOfArpAddrOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    mac_address: Union[InterfaceSviOneOfArpMacOptionsDef1, OneOfArpMacOptionsDef2] = _field(
        metadata={"alias": "macAddress"}
    )


@dataclass
class VpnInterfaceSviOneOfIpv4VrrpGrpIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceSviOneOfIpv4VrrpPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceSviOneOfIpv4VrrpPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceSviOneOfIpv4VrrpTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceSviOneOfIpv4VrrpTimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceSviOneOfIpv4VrrpTrackPrefixListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnInterfaceSviIpAddressSecondary:
    address: Union[
        OneOfIpv4VrrpIpv4SecondaryAddressOptionsDef1, OneOfIpv4VrrpIpv4SecondaryAddressOptionsDef2
    ]


@dataclass
class VpnInterfaceSviOneOfIpv4VrrpTrackingObjectTrackActionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnInterfaceSviIpv4VrrpTrackingObjectTrackActionDef


@dataclass
class VpnInterfaceSviOneOfIpv4VrrpTrackingObjectDecrementOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceSviTrackingObject:
    track_action: Union[
        VpnInterfaceSviOneOfIpv4VrrpTrackingObjectTrackActionOptionsDef1,
        OneOfIpv4VrrpTrackingObjectTrackActionOptionsDef2,
    ] = _field(metadata={"alias": "trackAction"})
    tracker_id: Union[
        OneOfIpv4VrrpTrackingObjectNameOptionsDef1, OneOfIpv4VrrpTrackingObjectNameOptionsDef2
    ] = _field(metadata={"alias": "trackerId"})
    decrement_value: Optional[
        Union[
            VpnInterfaceSviOneOfIpv4VrrpTrackingObjectDecrementOptionsDef1,
            OneOfIpv4VrrpTrackingObjectDecrementOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "decrementValue"})


@dataclass
class InterfaceSviVrrp1:
    group_id: Union[VpnInterfaceSviOneOfIpv4VrrpGrpIdOptionsDef1, OneOfIpv4VrrpGrpIdOptionsDef2]
    ip_address: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipAddress"})
    priority: Union[
        VpnInterfaceSviOneOfIpv4VrrpPriorityOptionsDef1,
        OneOfIpv4VrrpPriorityOptionsDef2,
        VpnInterfaceSviOneOfIpv4VrrpPriorityOptionsDef3,
    ]
    timer: Union[
        VpnInterfaceSviOneOfIpv4VrrpTimerOptionsDef1,
        OneOfIpv4VrrpTimerOptionsDef2,
        VpnInterfaceSviOneOfIpv4VrrpTimerOptionsDef3,
    ]
    tloc_pref_change: Union[
        OneOfIpv4VrrpTlocChangePrefOptionsDef1, OneOfIpv4VrrpTlocChangePrefOptionsDef2
    ] = _field(metadata={"alias": "tlocPrefChange"})
    track_omp: Union[
        OneOfIpv4VrrpTrackOmpOptionsDef1,
        OneOfIpv4VrrpTrackOmpOptionsDef2,
        OneOfIpv4VrrpTrackOmpOptionsDef3,
    ] = _field(metadata={"alias": "trackOmp"})
    follow_dual_router_ha_availability: Optional[
        Union[
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef1,
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "followDualRouterHAAvailability"})
    # VRRP Secondary IPV4 address
    ip_address_secondary: Optional[List[VpnInterfaceSviIpAddressSecondary]] = _field(
        default=None, metadata={"alias": "ipAddressSecondary"}
    )
    prefix_list: Optional[
        Union[
            VpnInterfaceSviOneOfIpv4VrrpTrackPrefixListOptionsDef1,
            OneOfIpv4VrrpTrackPrefixListOptionsDef2,
            OneOfIpv4VrrpTrackPrefixListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "prefixList"})
    tloc_pref_change_value: Optional[TlocPrefChangeValue] = _field(
        default=None, metadata={"alias": "tlocPrefChangeValue"}
    )
    # tracking object for VRRP configuration
    tracking_object: Optional[List[VpnInterfaceSviTrackingObject]] = _field(
        default=None, metadata={"alias": "trackingObject"}
    )


@dataclass
class LanVpnInterfaceSviOneOfIpv4VrrpGrpIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnInterfaceSviOneOfIpv4VrrpPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnInterfaceSviOneOfIpv4VrrpPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnInterfaceSviOneOfIpv4VrrpTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnInterfaceSviOneOfIpv4VrrpTimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnInterfaceSviOneOfIpv4VrrpTrackPrefixListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanVpnInterfaceSviIpAddressSecondary:
    address: Union[
        OneOfIpv4VrrpIpv4SecondaryAddressOptionsDef1, OneOfIpv4VrrpIpv4SecondaryAddressOptionsDef2
    ]


@dataclass
class InterfaceSviOneOfIpv4VrrpValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnInterfaceSviOneOfIpv4VrrpTrackingObjectTrackActionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnInterfaceSviIpv4VrrpTrackingObjectTrackActionDef


@dataclass
class LanVpnInterfaceSviOneOfIpv4VrrpTrackingObjectDecrementOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnInterfaceSviTrackingObject:
    track_action: Union[
        LanVpnInterfaceSviOneOfIpv4VrrpTrackingObjectTrackActionOptionsDef1,
        OneOfIpv4VrrpTrackingObjectTrackActionOptionsDef2,
    ] = _field(metadata={"alias": "trackAction"})
    tracker_id: Union[
        OneOfIpv4VrrpTrackingObjectNameOptionsDef1, OneOfIpv4VrrpTrackingObjectNameOptionsDef2
    ] = _field(metadata={"alias": "trackerId"})
    decrement_value: Optional[
        Union[
            LanVpnInterfaceSviOneOfIpv4VrrpTrackingObjectDecrementOptionsDef1,
            OneOfIpv4VrrpTrackingObjectDecrementOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "decrementValue"})


@dataclass
class InterfaceSviVrrp2:
    group_id: Union[LanVpnInterfaceSviOneOfIpv4VrrpGrpIdOptionsDef1, OneOfIpv4VrrpGrpIdOptionsDef2]
    ip_address: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipAddress"})
    priority: Union[
        LanVpnInterfaceSviOneOfIpv4VrrpPriorityOptionsDef1,
        OneOfIpv4VrrpPriorityOptionsDef2,
        LanVpnInterfaceSviOneOfIpv4VrrpPriorityOptionsDef3,
    ]
    timer: Union[
        LanVpnInterfaceSviOneOfIpv4VrrpTimerOptionsDef1,
        OneOfIpv4VrrpTimerOptionsDef2,
        LanVpnInterfaceSviOneOfIpv4VrrpTimerOptionsDef3,
    ]
    tloc_pref_change: Union[
        OneOfIpv4VrrpTlocChangePrefOptionsDef1, OneOfIpv4VrrpTlocChangePrefOptionsDef2
    ] = _field(metadata={"alias": "tlocPrefChange"})
    track_omp: Union[
        OneOfIpv4VrrpTrackOmpOptionsDef1,
        OneOfIpv4VrrpTrackOmpOptionsDef2,
        OneOfIpv4VrrpTrackOmpOptionsDef3,
    ] = _field(metadata={"alias": "trackOmp"})
    follow_dual_router_ha_availability: Optional[
        Union[
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef1,
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "followDualRouterHAAvailability"})
    # VRRP Secondary IPV4 address
    ip_address_secondary: Optional[List[LanVpnInterfaceSviIpAddressSecondary]] = _field(
        default=None, metadata={"alias": "ipAddressSecondary"}
    )
    prefix_list: Optional[
        Union[
            LanVpnInterfaceSviOneOfIpv4VrrpTrackPrefixListOptionsDef1,
            OneOfIpv4VrrpTrackPrefixListOptionsDef2,
            OneOfIpv4VrrpTrackPrefixListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "prefixList"})
    tloc_pref_change_value: Optional[
        Union[InterfaceSviOneOfIpv4VrrpValueOptionsDef1, OneOfIpv4VrrpValueOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tlocPrefChangeValue"})
    # tracking object for VRRP configuration
    tracking_object: Optional[List[LanVpnInterfaceSviTrackingObject]] = _field(
        default=None, metadata={"alias": "trackingObject"}
    )


@dataclass
class InterfaceSviOneOfIpv6VrrpGrpIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfIpv6VrrpPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfIpv6VrrpPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfIpv6VrrpTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfIpv6VrrpTimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfIpv6VrrpTrackPrefixListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceLanVpnInterfaceSviIpv6:
    ipv6_link_local: Union[
        OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef1, OneOfIpv6VrrpIpv6Ipv6LinkLocalOptionsDef2
    ] = _field(metadata={"alias": "ipv6LinkLocal"})
    prefix: Optional[
        Union[
            OneOfIpv6VrrpIpv6PrefixOptionsDef1,
            OneOfIpv6VrrpIpv6PrefixOptionsDef2,
            OneOfIpv6VrrpIpv6PrefixOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class InterfaceSviIpv6Secondary:
    prefix: Union[
        OneOfIpv6VrrpIpv6SecondaryPrefixOptionsDef1, OneOfIpv6VrrpIpv6SecondaryPrefixOptionsDef2
    ]


@dataclass
class InterfaceSviVrrpIpv6:
    group_id: Union[InterfaceSviOneOfIpv6VrrpGrpIdOptionsDef1, OneOfIpv6VrrpGrpIdOptionsDef2] = (
        _field(metadata={"alias": "groupId"})
    )
    # IPv6 VRRP
    ipv6: List[ServiceLanVpnInterfaceSviIpv6]
    priority: Union[
        InterfaceSviOneOfIpv6VrrpPriorityOptionsDef1,
        OneOfIpv6VrrpPriorityOptionsDef2,
        InterfaceSviOneOfIpv6VrrpPriorityOptionsDef3,
    ]
    timer: Union[
        InterfaceSviOneOfIpv6VrrpTimerOptionsDef1,
        OneOfIpv6VrrpTimerOptionsDef2,
        InterfaceSviOneOfIpv6VrrpTimerOptionsDef3,
    ]
    track_omp: Union[
        OneOfIpv6VrrpTrackOmpOptionsDef1,
        OneOfIpv6VrrpTrackOmpOptionsDef2,
        OneOfIpv6VrrpTrackOmpOptionsDef3,
    ] = _field(metadata={"alias": "trackOmp"})
    follow_dual_router_ha_availability: Optional[
        Union[
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef1,
            OneOfOnBooleanDefaultTrueNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "followDualRouterHAAvailability"})
    # IPv6 Secondary IP address
    ipv6_secondary: Optional[List[InterfaceSviIpv6Secondary]] = _field(
        default=None, metadata={"alias": "ipv6Secondary"}
    )
    track_prefix_list: Optional[
        Union[
            InterfaceSviOneOfIpv6VrrpTrackPrefixListOptionsDef1,
            OneOfIpv6VrrpTrackPrefixListOptionsDef2,
            OneOfIpv6VrrpTrackPrefixListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackPrefixList"})


@dataclass
class InterfaceSviOneOfTcpMssOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfArpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviOneOfArpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceSviAdvanced:
    """
    Advanced Attributes
    """

    arp_timeout: Union[
        InterfaceSviOneOfArpTimeoutOptionsDef1,
        OneOfArpTimeoutOptionsDef2,
        InterfaceSviOneOfArpTimeoutOptionsDef3,
    ] = _field(metadata={"alias": "arpTimeout"})
    ip_directed_broadcast: Union[
        OneOfIpDirectedBroadcastOptionsDef1,
        OneOfIpDirectedBroadcastOptionsDef2,
        OneOfIpDirectedBroadcastOptionsDef3,
    ] = _field(metadata={"alias": "ipDirectedBroadcast"})
    icmp_redirect_disable: Optional[
        Union[
            OneOfIcmpRedirectDisableOptionsDef1,
            OneOfIcmpRedirectDisableOptionsDef2,
            OneOfIcmpRedirectDisableOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "icmpRedirectDisable"})
    tcp_mss: Optional[
        Union[InterfaceSviOneOfTcpMssOptionsDef1, OneOfTcpMssOptionsDef2, OneOfTcpMssOptionsDef3]
    ] = _field(default=None, metadata={"alias": "tcpMss"})


@dataclass
class LanVpnInterfaceSviData:
    # Advanced Attributes
    advanced: InterfaceSviAdvanced
    interface_name: Union[InterfaceSviOneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    # ACL
    acl_qos: Optional[AclQos] = _field(default=None, metadata={"alias": "aclQos"})
    # Configure static ARP entries
    arp: Optional[List[InterfaceSviArp]] = _field(default=None)
    description: Optional[
        Union[
            InterfaceSviOneOfDescriptionOptionsDef1,
            OneOfDescriptionOptionsDef2,
            OneOfDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    dhcp_client_v6: Optional[
        Union[
            OneOfDhcpClientV6OptionsDef1, OneOfDhcpClientV6OptionsDef2, OneOfDhcpClientV6OptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "dhcpClientV6"})
    if_mtu: Optional[
        Union[
            InterfaceSviOneOfIfMtuOptionsDef1,
            OneOfIfMtuOptionsDef2,
            InterfaceSviOneOfIfMtuOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifMtu"})
    ip_mtu: Optional[
        Union[InterfaceSviOneOfMtuOptionsDef1, OneOfMtuOptionsDef2, InterfaceSviOneOfMtuOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ipMtu"})
    # ipv4 Attributes
    ipv4: Optional[InterfaceSviIpv4] = _field(default=None)
    # Advanced Attributes
    ipv6: Optional[LanVpnInterfaceSviIpv6] = _field(default=None)
    # Enable ipv4 VRRP
    vrrp: Optional[List[Union[InterfaceSviVrrp1, InterfaceSviVrrp2]]] = _field(default=None)
    # Enable ipv6 VRRP
    vrrp_ipv6: Optional[List[InterfaceSviVrrpIpv6]] = _field(
        default=None, metadata={"alias": "vrrpIpv6"}
    )


@dataclass
class EditLanVpnInterfaceSviParcelForServicePutRequest:
    """
    LAN VPN Interface SVI profile parcel schema for PUT request
    """

    data: LanVpnInterfaceSviData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
