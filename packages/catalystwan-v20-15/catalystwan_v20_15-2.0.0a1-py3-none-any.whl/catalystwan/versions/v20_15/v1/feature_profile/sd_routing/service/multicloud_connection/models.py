# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

ExtensionsParcelTypeDef = Literal[
    "vrf",
    "vrf/lan/interface/ethernet",
    "vrf/lan/interface/gre",
    "vrf/lan/interface/ipsec",
    "vrf/routing/bgp",
]

DefaultOptionTypeDef = Literal["default"]

Value = Literal["disable-peer", "warning-only"]

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

Ipv4AddressFamilyRedistributeProtocolDef = Literal["connected", "nat", "ospf", "ospfv3", "static"]

Ipv6AddressFamilyRedistributeProtocolDef = Literal["connected", "ospf", "static"]

Ipv6RouteNatDef = Literal["NAT64", "NAT66"]

MulticloudConnectionExtensionsParcelTypeDef = Literal[
    "ivrf",
    "vrf/lan/interface/ethernet",
    "vrf/lan/interface/gre",
    "vrf/lan/interface/ipsec",
    "vrf/routing/bgp",
]

MulticloudConnectionIpv4AddressFamilyRedistributeProtocolDef = Literal[
    "connected", "nat", "ospf", "ospfv3", "static"
]

MulticloudConnectionIpv6AddressFamilyRedistributeProtocolDef = Literal[
    "connected", "ospf", "static"
]

ServiceMulticloudConnectionExtensionsParcelTypeDef = Literal[
    "ivrf",
    "vrf/lan/interface/ethernet",
    "vrf/lan/interface/gre",
    "vrf/lan/interface/ipsec",
    "vrf/routing/bgp",
]

ServiceMulticloudConnectionIpv4AddressFamilyRedistributeProtocolDef = Literal[
    "connected", "nat", "ospf", "ospfv3", "static"
]

ServiceMulticloudConnectionIpv6AddressFamilyRedistributeProtocolDef = Literal[
    "connected", "ospf", "static"
]


@dataclass
class VariableOptionTypeObjectDef:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfExtensionsParcelTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ExtensionsParcelTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfExtensionsParcelTypeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfExtensionsParcelIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfExtensionsParcelIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


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
class OneOfNeighborDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNeighborDescriptionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNeighborDescriptionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


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
class OneOfAsNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfAsNumOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLocalAsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfLocalAsOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLocalAsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfKeepaliveOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfKeepaliveOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHoldtimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHoldtimeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


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
class OneOfNeighborEbgpMultihopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborEbgpMultihopOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNeighborEbgpMultihopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNeighborPasswordOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNeighborPasswordOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNeighborAsNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAsNumberOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNeighborAsNumberOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class LanIpv4NeighborAfTypeDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class PolicyType:
    """
    Neighbor received maximum prefix policy is disabled.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class NeighborMaxPrefixConfigDef1:
    # Neighbor received maximum prefix policy is disabled.
    policy_type: PolicyType = _field(metadata={"alias": "policyType"})


@dataclass
class MulticloudConnectionPolicyType:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class NeighborMaxPrefixConfigDef2:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    policy_type: MulticloudConnectionPolicyType = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef1, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    restart_interval: Union[
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1,
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2,
    ] = _field(metadata={"alias": "restartInterval"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class ServiceMulticloudConnectionPolicyType:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class NeighborMaxPrefixConfigDef3:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: ServiceMulticloudConnectionPolicyType = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef1, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class OneOfRoutePolicyNameOptionsDef1:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class RefId:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRoutePolicyNameOptionsDef2:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class AddressFamily:
    family_type: LanIpv4NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[NeighborMaxPrefixConfigDef1, NeighborMaxPrefixConfigDef2, NeighborMaxPrefixConfigDef3]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class Neighbor:
    address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]
    remote_as: Union[OneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "remoteAs"}
    )
    # Set BGP address family
    address_family: Optional[List[AddressFamily]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            OneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            OneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            OneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            OneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    holdtime: Optional[Union[OneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2]] = _field(
        default=None
    )
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[Union[OneOfKeepaliveOptionsDef1, OneOfKeepaliveOptionsDef2]] = _field(
        default=None
    )
    local_as: Optional[
        Union[OneOfLocalAsOptionsDef1, OneOfLocalAsOptionsDef2, OneOfLocalAsOptionsDef3]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            OneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    send_label: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendLabel"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfIpv6AddrGlobalVariableOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6AddrGlobalVariableOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class LanIpv6NeighborAfTypeDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class MulticloudConnectionAddressFamily:
    family_type: LanIpv6NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[NeighborMaxPrefixConfigDef1, NeighborMaxPrefixConfigDef2, NeighborMaxPrefixConfigDef3]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class Ipv6Neighbor:
    address: Union[OneOfIpv6AddrGlobalVariableOptionsDef1, OneOfIpv6AddrGlobalVariableOptionsDef2]
    remote_as: Union[OneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "remoteAs"}
    )
    # Set IPv6 BGP address family
    address_family: Optional[List[MulticloudConnectionAddressFamily]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            OneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            OneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            OneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            OneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    holdtime: Optional[Union[OneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2]] = _field(
        default=None
    )
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[Union[OneOfKeepaliveOptionsDef1, OneOfKeepaliveOptionsDef2]] = _field(
        default=None
    )
    local_as: Optional[
        Union[OneOfLocalAsOptionsDef1, OneOfLocalAsOptionsDef2, OneOfLocalAsOptionsDef3]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            OneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


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
class Ipv4AddressAndMaskDef:
    address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]
    mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]


@dataclass
class AggregateAddress:
    prefix: Ipv4AddressAndMaskDef
    as_set: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asSet"})
    summary_only: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "summaryOnly"})


@dataclass
class Network:
    prefix: Ipv4AddressAndMaskDef


@dataclass
class OneOfAddressFamilyPathsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAddressFamilyPathsOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAddressFamilyPathsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpv4AddressFamilyRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4AddressFamilyRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpv4AddressFamilyRedistributeProtocolOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Redistribute:
    protocol: Union[
        OneOfIpv4AddressFamilyRedistributeProtocolOptionsDef1,
        OneOfIpv4AddressFamilyRedistributeProtocolOptionsDef2,
    ]
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class ServiceMulticloudConnectionAddressFamily:
    """
    Set IPv4 unicast BGP address family
    """

    # Aggregate prefixes in specific range
    aggregate_address: Optional[List[AggregateAddress]] = _field(
        default=None, metadata={"alias": "aggregateAddress"}
    )
    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    name: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )
    # Configure the networks for BGP to advertise
    network: Optional[List[Network]] = _field(default=None)
    originate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    paths: Optional[
        Union[
            OneOfAddressFamilyPathsOptionsDef1,
            OneOfAddressFamilyPathsOptionsDef2,
            OneOfAddressFamilyPathsOptionsDef3,
        ]
    ] = _field(default=None)
    # Redistribute routes into BGP
    redistribute: Optional[List[Redistribute]] = _field(default=None)


@dataclass
class OneOfIpv6PrefixOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6PrefixOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Ipv6AggregateAddress:
    prefix: Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2]
    as_set: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asSet"})
    summary_only: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "summaryOnly"})


@dataclass
class Ipv6Network:
    prefix: Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2]


@dataclass
class OneOfIpv6AddressFamilyRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv6AddressFamilyRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpv6AddressFamilyRedistributeProtocolOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class MulticloudConnectionRedistribute:
    protocol: Union[
        OneOfIpv6AddressFamilyRedistributeProtocolOptionsDef1,
        OneOfIpv6AddressFamilyRedistributeProtocolOptionsDef2,
    ]
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class Ipv6AddressFamily:
    """
    Set BGP address family
    """

    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    # IPv6 Aggregate prefixes in specific range
    ipv6_aggregate_address: Optional[List[Ipv6AggregateAddress]] = _field(
        default=None, metadata={"alias": "ipv6AggregateAddress"}
    )
    # Configure the networks for BGP to advertise
    ipv6_network: Optional[List[Ipv6Network]] = _field(
        default=None, metadata={"alias": "ipv6Network"}
    )
    name: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )
    originate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    paths: Optional[
        Union[
            OneOfAddressFamilyPathsOptionsDef1,
            OneOfAddressFamilyPathsOptionsDef2,
            OneOfAddressFamilyPathsOptionsDef3,
        ]
    ] = _field(default=None)
    # Redistribute routes into BGP
    redistribute: Optional[List[MulticloudConnectionRedistribute]] = _field(default=None)


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
class OneOfIpv4NextHopTrackerOptionsDef1:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class OneOfIpv4NextHopTrackerOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class NextHopWithTracker:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        OneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]
    tracker: Union[OneOfIpv4NextHopTrackerOptionsDef1, OneOfIpv4NextHopTrackerOptionsDef2]


@dataclass
class NextHopContainer:
    # IPv4 Route Gateway Next Hop
    next_hop: Optional[List[NextHop]] = _field(default=None, metadata={"alias": "nextHop"})
    # IPv4 Route Gateway Next Hop with Tracker
    next_hop_with_tracker: Optional[List[NextHopWithTracker]] = _field(
        default=None, metadata={"alias": "nextHopWithTracker"}
    )


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


@dataclass
class OneOfIpv4RouteVpnOptionsWithoutVariable1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpv4RouteVpnOptionsWithoutVariable2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpRoute4:
    vpn: Union[OneOfIpv4RouteVpnOptionsWithoutVariable1, OneOfIpv4RouteVpnOptionsWithoutVariable2]


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
class MulticloudConnectionNextHop:
    address: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        OneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class MulticloudConnectionNextHopContainer:
    # IPv6 Route Gateway Next Hop
    next_hop: Optional[List[MulticloudConnectionNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )


@dataclass
class MulticloudConnectionOneOfIpRoute1:
    next_hop_container: MulticloudConnectionNextHopContainer = _field(
        metadata={"alias": "nextHopContainer"}
    )


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
class MulticloudConnectionOneOfIpRoute3:
    nat: Union[OneOfIpv6RouteNatOptionsWithoutDefault1, OneOfIpv6RouteNatOptionsWithoutDefault2]


@dataclass
class Ipv6Route:
    one_of_ip_route: Union[
        MulticloudConnectionOneOfIpRoute1, OneOfIpRoute2, MulticloudConnectionOneOfIpRoute3
    ] = _field(metadata={"alias": "oneOfIpRoute"})
    prefix: Union[OneOfIpv6RoutePrefixOptionsDef1, OneOfIpv6RoutePrefixOptionsDef2]


@dataclass
class ServiceMulticloudConnectionData:
    """
    Parameters for the new Connection
    """

    # Set IPv4 unicast BGP address family
    address_family: Optional[ServiceMulticloudConnectionAddressFamily] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    # IPv4 Static Route
    ipv4_route: Optional[List[Ipv4Route]] = _field(default=None, metadata={"alias": "ipv4Route"})
    # Set BGP address family
    ipv6_address_family: Optional[Ipv6AddressFamily] = _field(
        default=None, metadata={"alias": "ipv6AddressFamily"}
    )
    # Set BGP IPv6 neighbors
    ipv6_neighbor: Optional[List[Ipv6Neighbor]] = _field(
        default=None, metadata={"alias": "ipv6Neighbor"}
    )
    # IPv6 Static Route
    ipv6_route: Optional[List[Ipv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    # Set BGP IPv4 neighbors
    neighbor: Optional[List[Neighbor]] = _field(default=None)


@dataclass
class Extensions:
    parcel_type: Union[
        OneOfExtensionsParcelTypeOptionsDef1, OneOfExtensionsParcelTypeOptionsDef2
    ] = _field(metadata={"alias": "parcelType"})
    #  Parameters for the new Connection
    data: Optional[ServiceMulticloudConnectionData] = _field(default=None)
    parcel_id: Optional[
        Union[OneOfExtensionsParcelIdOptionsDef1, OneOfExtensionsParcelIdOptionsDef2]
    ] = _field(default=None, metadata={"alias": "parcelId"})


@dataclass
class MulticloudConnectionData:
    connection_name: VariableOptionTypeObjectDef = _field(metadata={"alias": "connectionName"})
    # Extending Bgp Neighbors, Ip Routes, Interface Parcel Id reference and Route Policy for Service Profile to build new Connections
    extensions: Optional[List[Extensions]] = _field(default=None)


@dataclass
class Payload:
    """
    SD-Routing multi-cloud-connection profile parcel schema for POST request
    """

    data: Optional[MulticloudConnectionData] = _field(default=None)
    description: Optional[str] = _field(default=None)
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
    # SD-Routing multi-cloud-connection profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingServiceVrfLanMulticloudConnectionPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateMultiCloudConnectionPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingServiceMulticloudConnectionData:
    connection_name: VariableOptionTypeObjectDef = _field(metadata={"alias": "connectionName"})
    # Extending Bgp Neighbors, Ip Routes, Interface Parcel Id reference and Route Policy for Service Profile to build new Connections
    extensions: Optional[List[Extensions]] = _field(default=None)


@dataclass
class CreateMultiCloudConnectionPostRequest:
    """
    SD-Routing multi-cloud-connection profile parcel schema for POST request
    """

    data: Optional[SdRoutingServiceMulticloudConnectionData] = _field(default=None)
    description: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class MulticloudConnectionOneOfExtensionsParcelTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: MulticloudConnectionExtensionsParcelTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class MulticloudConnectionOneOfExtensionsParcelIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class MulticloudConnectionOneOfNeighborDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class MulticloudConnectionOneOfAsNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class MulticloudConnectionOneOfLocalAsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class MulticloudConnectionOneOfKeepaliveOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionOneOfHoldtimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionOneOfNeighborPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class MulticloudConnectionOneOfNeighborAsNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionLanIpv4NeighborAfTypeDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SdRoutingServiceMulticloudConnectionPolicyType:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class MulticloudConnectionOneOfNeighborMaxPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionNeighborMaxPrefixConfigDef2:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    policy_type: SdRoutingServiceMulticloudConnectionPolicyType = _field(
        metadata={"alias": "policyType"}
    )
    prefix_num: Union[
        MulticloudConnectionOneOfNeighborMaxPrefixNumOptionsDef1,
        OneOfNeighborMaxPrefixNumOptionsDef2,
    ] = _field(metadata={"alias": "prefixNum"})
    restart_interval: Union[
        MulticloudConnectionOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1,
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2,
    ] = _field(metadata={"alias": "restartInterval"})
    threshold: Union[
        MulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        MulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionPolicyType:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class ServiceMulticloudConnectionOneOfNeighborMaxPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionNeighborMaxPrefixConfigDef3:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: FeatureProfileSdRoutingServiceMulticloudConnectionPolicyType = _field(
        metadata={"alias": "policyType"}
    )
    prefix_num: Union[
        ServiceMulticloudConnectionOneOfNeighborMaxPrefixNumOptionsDef1,
        OneOfNeighborMaxPrefixNumOptionsDef2,
    ] = _field(metadata={"alias": "prefixNum"})
    threshold: Union[
        ServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        ServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class SdRoutingServiceMulticloudConnectionAddressFamily:
    family_type: MulticloudConnectionLanIpv4NeighborAfTypeDef = _field(
        metadata={"alias": "familyType"}
    )
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[
            NeighborMaxPrefixConfigDef1,
            MulticloudConnectionNeighborMaxPrefixConfigDef2,
            MulticloudConnectionNeighborMaxPrefixConfigDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class MulticloudConnectionNeighbor:
    address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]
    remote_as: Union[MulticloudConnectionOneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "remoteAs"}
    )
    # Set BGP address family
    address_family: Optional[List[SdRoutingServiceMulticloudConnectionAddressFamily]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            MulticloudConnectionOneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            MulticloudConnectionOneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            MulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            MulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    holdtime: Optional[
        Union[MulticloudConnectionOneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[OneOfKeepaliveOptionsDef1, MulticloudConnectionOneOfKeepaliveOptionsDef2]
    ] = _field(default=None)
    local_as: Optional[
        Union[
            MulticloudConnectionOneOfLocalAsOptionsDef1,
            OneOfLocalAsOptionsDef2,
            OneOfLocalAsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            MulticloudConnectionOneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    send_label: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendLabel"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class ServiceMulticloudConnectionOneOfNeighborDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceMulticloudConnectionOneOfAsNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class ServiceMulticloudConnectionOneOfLocalAsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class ServiceMulticloudConnectionOneOfKeepaliveOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionOneOfHoldtimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionOneOfNeighborPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceMulticloudConnectionOneOfNeighborAsNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionLanIpv6NeighborAfTypeDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class V1FeatureProfileSdRoutingServiceMulticloudConnectionPolicyType:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfNeighborMaxPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionNeighborMaxPrefixConfigDef2:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    policy_type: V1FeatureProfileSdRoutingServiceMulticloudConnectionPolicyType = _field(
        metadata={"alias": "policyType"}
    )
    prefix_num: Union[
        SdRoutingServiceMulticloudConnectionOneOfNeighborMaxPrefixNumOptionsDef1,
        OneOfNeighborMaxPrefixNumOptionsDef2,
    ] = _field(metadata={"alias": "prefixNum"})
    restart_interval: Union[
        ServiceMulticloudConnectionOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1,
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2,
    ] = _field(metadata={"alias": "restartInterval"})
    threshold: Union[
        SdRoutingServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        SdRoutingServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class PolicyType1:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborMaxPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionNeighborMaxPrefixConfigDef3:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: PolicyType1 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborMaxPrefixNumOptionsDef1,
        OneOfNeighborMaxPrefixNumOptionsDef2,
    ] = _field(metadata={"alias": "prefixNum"})
    threshold: Union[
        FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionAddressFamily:
    family_type: MulticloudConnectionLanIpv6NeighborAfTypeDef = _field(
        metadata={"alias": "familyType"}
    )
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[
            NeighborMaxPrefixConfigDef1,
            ServiceMulticloudConnectionNeighborMaxPrefixConfigDef2,
            ServiceMulticloudConnectionNeighborMaxPrefixConfigDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class MulticloudConnectionIpv6Neighbor:
    address: Union[OneOfIpv6AddrGlobalVariableOptionsDef1, OneOfIpv6AddrGlobalVariableOptionsDef2]
    remote_as: Union[ServiceMulticloudConnectionOneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = (
        _field(metadata={"alias": "remoteAs"})
    )
    # Set IPv6 BGP address family
    address_family: Optional[
        List[FeatureProfileSdRoutingServiceMulticloudConnectionAddressFamily]
    ] = _field(default=None, metadata={"alias": "addressFamily"})
    as_number: Optional[
        Union[
            ServiceMulticloudConnectionOneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            ServiceMulticloudConnectionOneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            ServiceMulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            ServiceMulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    holdtime: Optional[
        Union[ServiceMulticloudConnectionOneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[OneOfKeepaliveOptionsDef1, ServiceMulticloudConnectionOneOfKeepaliveOptionsDef2]
    ] = _field(default=None)
    local_as: Optional[
        Union[
            ServiceMulticloudConnectionOneOfLocalAsOptionsDef1,
            OneOfLocalAsOptionsDef2,
            OneOfLocalAsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            ServiceMulticloudConnectionOneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class MulticloudConnectionOneOfAddressFamilyPathsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionOneOfIpv4AddressFamilyRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: MulticloudConnectionIpv4AddressFamilyRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class ServiceMulticloudConnectionRedistribute:
    protocol: Union[
        MulticloudConnectionOneOfIpv4AddressFamilyRedistributeProtocolOptionsDef1,
        OneOfIpv4AddressFamilyRedistributeProtocolOptionsDef2,
    ]
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class V1FeatureProfileSdRoutingServiceMulticloudConnectionAddressFamily:
    """
    Set IPv4 unicast BGP address family
    """

    # Aggregate prefixes in specific range
    aggregate_address: Optional[List[AggregateAddress]] = _field(
        default=None, metadata={"alias": "aggregateAddress"}
    )
    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    name: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )
    # Configure the networks for BGP to advertise
    network: Optional[List[Network]] = _field(default=None)
    originate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    paths: Optional[
        Union[
            MulticloudConnectionOneOfAddressFamilyPathsOptionsDef1,
            OneOfAddressFamilyPathsOptionsDef2,
            OneOfAddressFamilyPathsOptionsDef3,
        ]
    ] = _field(default=None)
    # Redistribute routes into BGP
    redistribute: Optional[List[ServiceMulticloudConnectionRedistribute]] = _field(default=None)


@dataclass
class ServiceMulticloudConnectionOneOfAddressFamilyPathsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionOneOfIpv6AddressFamilyRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: MulticloudConnectionIpv6AddressFamilyRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdRoutingServiceMulticloudConnectionRedistribute:
    protocol: Union[
        MulticloudConnectionOneOfIpv6AddressFamilyRedistributeProtocolOptionsDef1,
        OneOfIpv6AddressFamilyRedistributeProtocolOptionsDef2,
    ]
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class MulticloudConnectionIpv6AddressFamily:
    """
    Set BGP address family
    """

    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    # IPv6 Aggregate prefixes in specific range
    ipv6_aggregate_address: Optional[List[Ipv6AggregateAddress]] = _field(
        default=None, metadata={"alias": "ipv6AggregateAddress"}
    )
    # Configure the networks for BGP to advertise
    ipv6_network: Optional[List[Ipv6Network]] = _field(
        default=None, metadata={"alias": "ipv6Network"}
    )
    name: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )
    originate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    paths: Optional[
        Union[
            ServiceMulticloudConnectionOneOfAddressFamilyPathsOptionsDef1,
            OneOfAddressFamilyPathsOptionsDef2,
            OneOfAddressFamilyPathsOptionsDef3,
        ]
    ] = _field(default=None)
    # Redistribute routes into BGP
    redistribute: Optional[List[SdRoutingServiceMulticloudConnectionRedistribute]] = _field(
        default=None
    )


@dataclass
class MulticloudConnectionOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionNextHop:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        MulticloudConnectionOneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


@dataclass
class ServiceMulticloudConnectionOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionNextHopWithTracker:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        ServiceMulticloudConnectionOneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]
    tracker: Union[OneOfIpv4NextHopTrackerOptionsDef1, OneOfIpv4NextHopTrackerOptionsDef2]


@dataclass
class ServiceMulticloudConnectionNextHopContainer:
    # IPv4 Route Gateway Next Hop
    next_hop: Optional[List[ServiceMulticloudConnectionNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )
    # IPv4 Route Gateway Next Hop with Tracker
    next_hop_with_tracker: Optional[List[MulticloudConnectionNextHopWithTracker]] = _field(
        default=None, metadata={"alias": "nextHopWithTracker"}
    )


@dataclass
class ServiceMulticloudConnectionOneOfIpRoute1:
    next_hop_container: ServiceMulticloudConnectionNextHopContainer = _field(
        metadata={"alias": "nextHopContainer"}
    )


@dataclass
class MulticloudConnectionIpv4Route:
    one_of_ip_route: Union[
        ServiceMulticloudConnectionOneOfIpRoute1, OneOfIpRoute2, OneOfIpRoute3, OneOfIpRoute4
    ] = _field(metadata={"alias": "oneOfIpRoute"})
    # Prefix
    prefix: Prefix


@dataclass
class MulticloudConnectionOneOfIpv6NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingServiceMulticloudConnectionNextHop:
    address: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        MulticloudConnectionOneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class SdRoutingServiceMulticloudConnectionNextHopContainer:
    # IPv6 Route Gateway Next Hop
    next_hop: Optional[List[SdRoutingServiceMulticloudConnectionNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfIpRoute1:
    next_hop_container: SdRoutingServiceMulticloudConnectionNextHopContainer = _field(
        metadata={"alias": "nextHopContainer"}
    )


@dataclass
class ServiceMulticloudConnectionOneOfIpRoute3:
    nat: Union[OneOfIpv6RouteNatOptionsWithoutDefault1, OneOfIpv6RouteNatOptionsWithoutDefault2]


@dataclass
class MulticloudConnectionIpv6Route:
    one_of_ip_route: Union[
        SdRoutingServiceMulticloudConnectionOneOfIpRoute1,
        OneOfIpRoute2,
        ServiceMulticloudConnectionOneOfIpRoute3,
    ] = _field(metadata={"alias": "oneOfIpRoute"})
    prefix: Union[OneOfIpv6RoutePrefixOptionsDef1, OneOfIpv6RoutePrefixOptionsDef2]


@dataclass
class V1FeatureProfileSdRoutingServiceMulticloudConnectionData:
    """
    Parameters for the new Connection
    """

    # Set IPv4 unicast BGP address family
    address_family: Optional[V1FeatureProfileSdRoutingServiceMulticloudConnectionAddressFamily] = (
        _field(default=None, metadata={"alias": "addressFamily"})
    )
    # IPv4 Static Route
    ipv4_route: Optional[List[MulticloudConnectionIpv4Route]] = _field(
        default=None, metadata={"alias": "ipv4Route"}
    )
    # Set BGP address family
    ipv6_address_family: Optional[MulticloudConnectionIpv6AddressFamily] = _field(
        default=None, metadata={"alias": "ipv6AddressFamily"}
    )
    # Set BGP IPv6 neighbors
    ipv6_neighbor: Optional[List[MulticloudConnectionIpv6Neighbor]] = _field(
        default=None, metadata={"alias": "ipv6Neighbor"}
    )
    # IPv6 Static Route
    ipv6_route: Optional[List[MulticloudConnectionIpv6Route]] = _field(
        default=None, metadata={"alias": "ipv6Route"}
    )
    # Set BGP IPv4 neighbors
    neighbor: Optional[List[MulticloudConnectionNeighbor]] = _field(default=None)


@dataclass
class MulticloudConnectionExtensions:
    parcel_type: Union[
        MulticloudConnectionOneOfExtensionsParcelTypeOptionsDef1,
        OneOfExtensionsParcelTypeOptionsDef2,
    ] = _field(metadata={"alias": "parcelType"})
    #  Parameters for the new Connection
    data: Optional[V1FeatureProfileSdRoutingServiceMulticloudConnectionData] = _field(default=None)
    parcel_id: Optional[
        Union[
            MulticloudConnectionOneOfExtensionsParcelIdOptionsDef1,
            OneOfExtensionsParcelIdOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "parcelId"})


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionData:
    connection_name: VariableOptionTypeObjectDef = _field(metadata={"alias": "connectionName"})
    # Extending Bgp Neighbors, Ip Routes, Interface Parcel Id reference and Route Policy for Service Profile to build new Connections
    extensions: Optional[List[MulticloudConnectionExtensions]] = _field(default=None)


@dataclass
class MulticloudConnectionPayload:
    """
    SD-Routing multi-cloud-connection profile parcel schema for PUT request
    """

    data: Optional[FeatureProfileSdRoutingServiceMulticloudConnectionData] = _field(default=None)
    description: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdRoutingServiceVrfLanMulticloudConnectionPayload:
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
    # SD-Routing multi-cloud-connection profile parcel schema for PUT request
    payload: Optional[MulticloudConnectionPayload] = _field(default=None)


@dataclass
class EditMultiCloudConnectionPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ServiceMulticloudConnectionOneOfExtensionsParcelTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceMulticloudConnectionExtensionsParcelTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class ServiceMulticloudConnectionOneOfExtensionsParcelIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfNeighborDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfAsNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfLocalAsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfKeepaliveOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfHoldtimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfNeighborPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfNeighborAsNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionLanIpv4NeighborAfTypeDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class PolicyType2:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class V1FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborMaxPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingServiceMulticloudConnectionNeighborMaxPrefixConfigDef2:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    policy_type: PolicyType2 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        V1FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborMaxPrefixNumOptionsDef1,
        OneOfNeighborMaxPrefixNumOptionsDef2,
    ] = _field(metadata={"alias": "prefixNum"})
    restart_interval: Union[
        SdRoutingServiceMulticloudConnectionOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1,
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2,
    ] = _field(metadata={"alias": "restartInterval"})
    threshold: Union[
        V1FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        V1FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class PolicyType3:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef31:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingServiceMulticloudConnectionNeighborMaxPrefixConfigDef3:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: PolicyType3 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef11, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef11,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef31,
    ]


@dataclass
class AddressFamily1:
    family_type: ServiceMulticloudConnectionLanIpv4NeighborAfTypeDef = _field(
        metadata={"alias": "familyType"}
    )
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[
            NeighborMaxPrefixConfigDef1,
            SdRoutingServiceMulticloudConnectionNeighborMaxPrefixConfigDef2,
            SdRoutingServiceMulticloudConnectionNeighborMaxPrefixConfigDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class ServiceMulticloudConnectionNeighbor:
    address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]
    remote_as: Union[
        SdRoutingServiceMulticloudConnectionOneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2
    ] = _field(metadata={"alias": "remoteAs"})
    # Set BGP address family
    address_family: Optional[List[AddressFamily1]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            SdRoutingServiceMulticloudConnectionOneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            SdRoutingServiceMulticloudConnectionOneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            SdRoutingServiceMulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            SdRoutingServiceMulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    holdtime: Optional[
        Union[
            SdRoutingServiceMulticloudConnectionOneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2
        ]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[
            OneOfKeepaliveOptionsDef1, SdRoutingServiceMulticloudConnectionOneOfKeepaliveOptionsDef2
        ]
    ] = _field(default=None)
    local_as: Optional[
        Union[
            SdRoutingServiceMulticloudConnectionOneOfLocalAsOptionsDef1,
            OneOfLocalAsOptionsDef2,
            OneOfLocalAsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            SdRoutingServiceMulticloudConnectionOneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    send_label: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendLabel"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfAsNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfLocalAsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfKeepaliveOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfHoldtimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborAsNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionLanIpv6NeighborAfTypeDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class PolicyType4:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef12:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef12:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef32:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionNeighborMaxPrefixConfigDef2:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    policy_type: PolicyType4 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef12, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    restart_interval: Union[
        FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1,
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2,
    ] = _field(metadata={"alias": "restartInterval"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef12,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef32,
    ]


@dataclass
class PolicyType5:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef13:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef13:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef33:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionNeighborMaxPrefixConfigDef3:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: PolicyType5 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef13, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef13,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef33,
    ]


@dataclass
class AddressFamily2:
    family_type: ServiceMulticloudConnectionLanIpv6NeighborAfTypeDef = _field(
        metadata={"alias": "familyType"}
    )
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[
            NeighborMaxPrefixConfigDef1,
            FeatureProfileSdRoutingServiceMulticloudConnectionNeighborMaxPrefixConfigDef2,
            FeatureProfileSdRoutingServiceMulticloudConnectionNeighborMaxPrefixConfigDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class ServiceMulticloudConnectionIpv6Neighbor:
    address: Union[OneOfIpv6AddrGlobalVariableOptionsDef1, OneOfIpv6AddrGlobalVariableOptionsDef2]
    remote_as: Union[
        FeatureProfileSdRoutingServiceMulticloudConnectionOneOfAsNumOptionsDef1,
        OneOfAsNumOptionsDef2,
    ] = _field(metadata={"alias": "remoteAs"})
    # Set IPv6 BGP address family
    address_family: Optional[List[AddressFamily2]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    holdtime: Optional[
        Union[
            FeatureProfileSdRoutingServiceMulticloudConnectionOneOfHoldtimeOptionsDef1,
            OneOfHoldtimeOptionsDef2,
        ]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[
            OneOfKeepaliveOptionsDef1,
            FeatureProfileSdRoutingServiceMulticloudConnectionOneOfKeepaliveOptionsDef2,
        ]
    ] = _field(default=None)
    local_as: Optional[
        Union[
            FeatureProfileSdRoutingServiceMulticloudConnectionOneOfLocalAsOptionsDef1,
            OneOfLocalAsOptionsDef2,
            OneOfLocalAsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            FeatureProfileSdRoutingServiceMulticloudConnectionOneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfAddressFamilyPathsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionOneOfIpv4AddressFamilyRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceMulticloudConnectionIpv4AddressFamilyRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionRedistribute:
    protocol: Union[
        ServiceMulticloudConnectionOneOfIpv4AddressFamilyRedistributeProtocolOptionsDef1,
        OneOfIpv4AddressFamilyRedistributeProtocolOptionsDef2,
    ]
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class AddressFamily3:
    """
    Set IPv4 unicast BGP address family
    """

    # Aggregate prefixes in specific range
    aggregate_address: Optional[List[AggregateAddress]] = _field(
        default=None, metadata={"alias": "aggregateAddress"}
    )
    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    name: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )
    # Configure the networks for BGP to advertise
    network: Optional[List[Network]] = _field(default=None)
    originate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    paths: Optional[
        Union[
            SdRoutingServiceMulticloudConnectionOneOfAddressFamilyPathsOptionsDef1,
            OneOfAddressFamilyPathsOptionsDef2,
            OneOfAddressFamilyPathsOptionsDef3,
        ]
    ] = _field(default=None)
    # Redistribute routes into BGP
    redistribute: Optional[List[FeatureProfileSdRoutingServiceMulticloudConnectionRedistribute]] = (
        _field(default=None)
    )


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfAddressFamilyPathsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionOneOfIpv6AddressFamilyRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceMulticloudConnectionIpv6AddressFamilyRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class V1FeatureProfileSdRoutingServiceMulticloudConnectionRedistribute:
    protocol: Union[
        ServiceMulticloudConnectionOneOfIpv6AddressFamilyRedistributeProtocolOptionsDef1,
        OneOfIpv6AddressFamilyRedistributeProtocolOptionsDef2,
    ]
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class ServiceMulticloudConnectionIpv6AddressFamily:
    """
    Set BGP address family
    """

    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    # IPv6 Aggregate prefixes in specific range
    ipv6_aggregate_address: Optional[List[Ipv6AggregateAddress]] = _field(
        default=None, metadata={"alias": "ipv6AggregateAddress"}
    )
    # Configure the networks for BGP to advertise
    ipv6_network: Optional[List[Ipv6Network]] = _field(
        default=None, metadata={"alias": "ipv6Network"}
    )
    name: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )
    originate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    paths: Optional[
        Union[
            FeatureProfileSdRoutingServiceMulticloudConnectionOneOfAddressFamilyPathsOptionsDef1,
            OneOfAddressFamilyPathsOptionsDef2,
            OneOfAddressFamilyPathsOptionsDef3,
        ]
    ] = _field(default=None)
    # Redistribute routes into BGP
    redistribute: Optional[
        List[V1FeatureProfileSdRoutingServiceMulticloudConnectionRedistribute]
    ] = _field(default=None)


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionNextHop:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        SdRoutingServiceMulticloudConnectionOneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceMulticloudConnectionNextHopWithTracker:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        FeatureProfileSdRoutingServiceMulticloudConnectionOneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]
    tracker: Union[OneOfIpv4NextHopTrackerOptionsDef1, OneOfIpv4NextHopTrackerOptionsDef2]


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionNextHopContainer:
    # IPv4 Route Gateway Next Hop
    next_hop: Optional[List[FeatureProfileSdRoutingServiceMulticloudConnectionNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )
    # IPv4 Route Gateway Next Hop with Tracker
    next_hop_with_tracker: Optional[List[ServiceMulticloudConnectionNextHopWithTracker]] = _field(
        default=None, metadata={"alias": "nextHopWithTracker"}
    )


@dataclass
class FeatureProfileSdRoutingServiceMulticloudConnectionOneOfIpRoute1:
    next_hop_container: FeatureProfileSdRoutingServiceMulticloudConnectionNextHopContainer = _field(
        metadata={"alias": "nextHopContainer"}
    )


@dataclass
class ServiceMulticloudConnectionIpv4Route:
    one_of_ip_route: Union[
        FeatureProfileSdRoutingServiceMulticloudConnectionOneOfIpRoute1,
        OneOfIpRoute2,
        OneOfIpRoute3,
        OneOfIpRoute4,
    ] = _field(metadata={"alias": "oneOfIpRoute"})
    # Prefix
    prefix: Prefix


@dataclass
class ServiceMulticloudConnectionOneOfIpv6NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdRoutingServiceMulticloudConnectionNextHop:
    address: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        ServiceMulticloudConnectionOneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class V1FeatureProfileSdRoutingServiceMulticloudConnectionNextHopContainer:
    # IPv6 Route Gateway Next Hop
    next_hop: Optional[List[V1FeatureProfileSdRoutingServiceMulticloudConnectionNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )


@dataclass
class V1FeatureProfileSdRoutingServiceMulticloudConnectionOneOfIpRoute1:
    next_hop_container: V1FeatureProfileSdRoutingServiceMulticloudConnectionNextHopContainer = (
        _field(metadata={"alias": "nextHopContainer"})
    )


@dataclass
class SdRoutingServiceMulticloudConnectionOneOfIpRoute3:
    nat: Union[OneOfIpv6RouteNatOptionsWithoutDefault1, OneOfIpv6RouteNatOptionsWithoutDefault2]


@dataclass
class ServiceMulticloudConnectionIpv6Route:
    one_of_ip_route: Union[
        V1FeatureProfileSdRoutingServiceMulticloudConnectionOneOfIpRoute1,
        OneOfIpRoute2,
        SdRoutingServiceMulticloudConnectionOneOfIpRoute3,
    ] = _field(metadata={"alias": "oneOfIpRoute"})
    prefix: Union[OneOfIpv6RoutePrefixOptionsDef1, OneOfIpv6RoutePrefixOptionsDef2]


@dataclass
class Data2:
    """
    Parameters for the new Connection
    """

    # Set IPv4 unicast BGP address family
    address_family: Optional[AddressFamily3] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    # IPv4 Static Route
    ipv4_route: Optional[List[ServiceMulticloudConnectionIpv4Route]] = _field(
        default=None, metadata={"alias": "ipv4Route"}
    )
    # Set BGP address family
    ipv6_address_family: Optional[ServiceMulticloudConnectionIpv6AddressFamily] = _field(
        default=None, metadata={"alias": "ipv6AddressFamily"}
    )
    # Set BGP IPv6 neighbors
    ipv6_neighbor: Optional[List[ServiceMulticloudConnectionIpv6Neighbor]] = _field(
        default=None, metadata={"alias": "ipv6Neighbor"}
    )
    # IPv6 Static Route
    ipv6_route: Optional[List[ServiceMulticloudConnectionIpv6Route]] = _field(
        default=None, metadata={"alias": "ipv6Route"}
    )
    # Set BGP IPv4 neighbors
    neighbor: Optional[List[ServiceMulticloudConnectionNeighbor]] = _field(default=None)


@dataclass
class ServiceMulticloudConnectionExtensions:
    parcel_type: Union[
        ServiceMulticloudConnectionOneOfExtensionsParcelTypeOptionsDef1,
        OneOfExtensionsParcelTypeOptionsDef2,
    ] = _field(metadata={"alias": "parcelType"})
    #  Parameters for the new Connection
    data: Optional[Data2] = _field(default=None)
    parcel_id: Optional[
        Union[
            ServiceMulticloudConnectionOneOfExtensionsParcelIdOptionsDef1,
            OneOfExtensionsParcelIdOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "parcelId"})


@dataclass
class Data1:
    connection_name: VariableOptionTypeObjectDef = _field(metadata={"alias": "connectionName"})
    # Extending Bgp Neighbors, Ip Routes, Interface Parcel Id reference and Route Policy for Service Profile to build new Connections
    extensions: Optional[List[ServiceMulticloudConnectionExtensions]] = _field(default=None)


@dataclass
class EditMultiCloudConnectionPutRequest:
    """
    SD-Routing multi-cloud-connection profile parcel schema for PUT request
    """

    data: Optional[Data1] = _field(default=None)
    description: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
