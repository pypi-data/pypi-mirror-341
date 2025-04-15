# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

TunnelModeDef = Literal["ipv4", "ipv4-v6overlay", "ipv6"]

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

IkeV1ModeDef = Literal["aggressive", "main"]

DefaultIkeV1ModeDef = Literal["main"]

IkeV1CipherSuiteDef = Literal[
    "aes128-cbc-sha1", "aes128-cbc-sha2", "aes256-cbc-sha1", "aes256-cbc-sha2"
]

DefaultIkeV1CipherSuiteDef = Literal["aes256-cbc-sha1"]

IkeGroupDef = Literal["14", "15", "16", "19", "20", "21"]

DefaultIkeGroupDef = Literal["16"]

IpsecCipherSuiteDef = Literal[
    "aes256-cbc-sha1", "aes256-cbc-sha256", "aes256-cbc-sha384", "aes256-cbc-sha512", "aes256-gcm"
]

DefaultIpsecCipherSuiteDef = Literal["aes256-gcm"]

PerfectForwardSecrecyDef = Literal[
    "group-14", "group-15", "group-16", "group-19", "group-20", "group-21", "none"
]

DefaultPerfectForwardSecrecyDef = Literal["group-16"]


@dataclass
class OneOfIpsecIfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpsecIfNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


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
class OneOfTunnelModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TunnelModeDef


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
class Ipv4AddressAndMaskDef:
    address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]
    mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]


@dataclass
class TunnelSource1:
    source_ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "sourceIpAddress"}
    )


@dataclass
class OneOfTunnelSourceInterfaceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTunnelSourceInterfaceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class TunnelSource2:
    source_interface: Union[
        OneOfTunnelSourceInterfaceOptionsDef1, OneOfTunnelSourceInterfaceOptionsDef2
    ] = _field(metadata={"alias": "sourceInterface"})


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
class OneOfClearDontFragmentOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfClearDontFragmentOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfClearDontFragmentOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class TunnelConfig4O4:
    """
    Tunnel Config for Mode ipv4
    """

    clear_dont_fragment: Union[
        OneOfClearDontFragmentOptionsDef1,
        OneOfClearDontFragmentOptionsDef2,
        OneOfClearDontFragmentOptionsDef3,
    ] = _field(metadata={"alias": "clearDontFragment"})
    ip_address: Ipv4AddressAndMaskDef = _field(metadata={"alias": "ipAddress"})
    mtu: Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3]
    tunnel_dest_ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = (
        _field(metadata={"alias": "tunnelDestIpAddress"})
    )
    # Tunnel Source
    tunnel_source: Union[TunnelSource1, TunnelSource2] = _field(metadata={"alias": "tunnelSource"})
    tcp_mss_adjust: Optional[
        Union[
            OneOfTcpMssAdjustOptionsDef1, OneOfTcpMssAdjustOptionsDef2, OneOfTcpMssAdjustOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})


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
class OneOfIpv6AddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6AddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class IpsecTunnelSource1:
    source_ipv6_address: Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2] = _field(
        metadata={"alias": "sourceIpv6Address"}
    )


@dataclass
class OneOfMtuV6OptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMtuV6OptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMtuV6OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTcpMssAdjustV6OptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTcpMssAdjustV6OptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTcpMssAdjustV6OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class TunnelConfig6O6:
    """
    Tunnel Config for Mode ipv6
    """

    ipv6_address: Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2] = _field(
        metadata={"alias": "ipv6Address"}
    )
    tunnel_dest_ipv6_address: Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2] = (
        _field(metadata={"alias": "tunnelDestIpv6Address"})
    )
    # Tunnel Source
    tunnel_source: Union[IpsecTunnelSource1, TunnelSource2] = _field(
        metadata={"alias": "tunnelSource"}
    )
    ipv6_mtu: Optional[
        Union[OneOfMtuV6OptionsDef1, OneOfMtuV6OptionsDef2, OneOfMtuV6OptionsDef3]
    ] = _field(default=None, metadata={"alias": "ipv6Mtu"})
    ipv6_tcp_mss_adjust: Optional[
        Union[
            OneOfTcpMssAdjustV6OptionsDef1,
            OneOfTcpMssAdjustV6OptionsDef2,
            OneOfTcpMssAdjustV6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipv6TcpMssAdjust"})


@dataclass
class TunnelConfig6O4:
    """
    Tunnel Config for Mode ipv6 over ipv4
    """

    ipv6_address: Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2] = _field(
        metadata={"alias": "ipv6Address"}
    )
    tunnel_dest_ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = (
        _field(metadata={"alias": "tunnelDestIpAddress"})
    )
    # Tunnel Source
    tunnel_source: Union[TunnelSource1, TunnelSource2] = _field(metadata={"alias": "tunnelSource"})
    ipv6_mtu: Optional[
        Union[OneOfMtuV6OptionsDef1, OneOfMtuV6OptionsDef2, OneOfMtuV6OptionsDef3]
    ] = _field(default=None, metadata={"alias": "ipv6Mtu"})
    ipv6_tcp_mss_adjust: Optional[
        Union[
            OneOfTcpMssAdjustV6OptionsDef1,
            OneOfTcpMssAdjustV6OptionsDef2,
            OneOfTcpMssAdjustV6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipv6TcpMssAdjust"})


@dataclass
class OneOfTunnelRouteViaOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTunnelRouteViaOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTunnelRouteViaOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTunnelVrfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTunnelVrfNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class TunnelVrf1:
    vrf: Union[OneOfTunnelVrfNameOptionsDef1, OneOfTunnelVrfNameOptionsDef2]


@dataclass
class OneOfTunnelVrfGlobalVrfOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class TunnelVrf2:
    global_vrf: OneOfTunnelVrfGlobalVrfOptionsDef = _field(metadata={"alias": "globalVrf"})


@dataclass
class OneOfDpdIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDpdIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDpdIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDpdRetriesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDpdRetriesOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDpdRetriesOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Dpd:
    """
    dead-peer detection
    """

    dpd_interval: Union[
        OneOfDpdIntervalOptionsDef1, OneOfDpdIntervalOptionsDef2, OneOfDpdIntervalOptionsDef3
    ] = _field(metadata={"alias": "dpdInterval"})
    dpd_retries: Union[
        OneOfDpdRetriesOptionsDef1, OneOfDpdRetriesOptionsDef2, OneOfDpdRetriesOptionsDef3
    ] = _field(metadata={"alias": "dpdRetries"})


@dataclass
class IkeVersion:
    value: Optional[Any] = _field(default=None)


@dataclass
class OneOfIkeV1ModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IkeV1ModeDef


@dataclass
class OneOfIkeV1ModeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeV1ModeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultIkeV1ModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIkeRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIkeRekeyIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeRekeyIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIkeV1CipherSuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IkeV1CipherSuiteDef


@dataclass
class OneOfIkeV1CipherSuiteOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeV1CipherSuiteOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultIkeV1CipherSuiteDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIkeGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IkeGroupDef


@dataclass
class OneOfIkeGroupOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeGroupOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultIkeGroupDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPreSharedSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPreSharedSecretOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


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
class OneOfIkeV1LocalIdentityOptionsDef1:
    ipv4_addr: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipv4Addr"})


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
class OneOfIkeV1LocalIdentityOptionsDef2:
    ipv6_addr: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ] = _field(metadata={"alias": "ipv6Addr"})


@dataclass
class OneOfIdentityValueFqdnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIdentityValueFqdnOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeV1LocalIdentityOptionsDef3:
    fqdn: Union[OneOfIdentityValueFqdnOptionsDef1, OneOfIdentityValueFqdnOptionsDef2]


@dataclass
class OneOfIdentityValueEmailOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIdentityValueEmailOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeV1LocalIdentityOptionsDef4:
    email: Union[OneOfIdentityValueEmailOptionsDef1, OneOfIdentityValueEmailOptionsDef2]


@dataclass
class OneOfIkeV1LocalIdentityOptionsDef5:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIkeV1RemoteIdentityOptionsDef1:
    ipv4_addr: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipv4Addr"})


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
class OneOfIkeV1RemoteIdentityOptionsDef2:
    ipv6_prefix: Union[
        OneOfIpv6PrefixGlobalVariableWithoutDefault1, OneOfIpv6PrefixGlobalVariableWithoutDefault2
    ] = _field(metadata={"alias": "ipv6Prefix"})


@dataclass
class OneOfIkeV1RemoteIdentityOptionsDef3:
    fqdn: Union[OneOfIdentityValueFqdnOptionsDef1, OneOfIdentityValueFqdnOptionsDef2]


@dataclass
class OneOfIkeV1RemoteIdentityOptionsDef4:
    email: Union[OneOfIdentityValueEmailOptionsDef1, OneOfIdentityValueEmailOptionsDef2]


@dataclass
class OneOfIkeV1RemoteIdentityOptionsDef5:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class IkeV1:
    """
    IKEv1 config
    """

    ike_dh_group: Union[
        OneOfIkeGroupOptionsDef1, OneOfIkeGroupOptionsDef2, OneOfIkeGroupOptionsDef3
    ] = _field(metadata={"alias": "ikeDhGroup"})
    ike_rekey_interval: Union[
        OneOfIkeRekeyIntervalOptionsDef1,
        OneOfIkeRekeyIntervalOptionsDef2,
        OneOfIkeRekeyIntervalOptionsDef3,
    ] = _field(metadata={"alias": "ikeRekeyInterval"})
    ike_v1_cipher_suite: Union[
        OneOfIkeV1CipherSuiteOptionsDef1,
        OneOfIkeV1CipherSuiteOptionsDef2,
        OneOfIkeV1CipherSuiteOptionsDef3,
    ] = _field(metadata={"alias": "ikeV1CipherSuite"})
    ike_v1_mode: Union[
        OneOfIkeV1ModeOptionsDef1, OneOfIkeV1ModeOptionsDef2, OneOfIkeV1ModeOptionsDef3
    ] = _field(metadata={"alias": "ikeV1Mode"})
    pre_shared_secret: Union[OneOfPreSharedSecretOptionsDef1, OneOfPreSharedSecretOptionsDef2] = (
        _field(metadata={"alias": "preSharedSecret"})
    )
    ike_local_id: Optional[
        Union[
            OneOfIkeV1LocalIdentityOptionsDef1,
            OneOfIkeV1LocalIdentityOptionsDef2,
            OneOfIkeV1LocalIdentityOptionsDef3,
            OneOfIkeV1LocalIdentityOptionsDef4,
            OneOfIkeV1LocalIdentityOptionsDef5,
        ]
    ] = _field(default=None, metadata={"alias": "ikeLocalId"})
    ike_remote_id: Optional[
        Union[
            OneOfIkeV1RemoteIdentityOptionsDef1,
            OneOfIkeV1RemoteIdentityOptionsDef2,
            OneOfIkeV1RemoteIdentityOptionsDef3,
            OneOfIkeV1RemoteIdentityOptionsDef4,
            OneOfIkeV1RemoteIdentityOptionsDef5,
        ]
    ] = _field(default=None, metadata={"alias": "ikeRemoteId"})


@dataclass
class OneOfIkeV2LocalIdentityOptionsDef1:
    ipv4_addr: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipv4Addr"})


@dataclass
class OneOfIkeV2LocalIdentityOptionsDef2:
    ipv6_addr: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ] = _field(metadata={"alias": "ipv6Addr"})


@dataclass
class OneOfIkeV2LocalIdentityOptionsDef3:
    fqdn: Union[OneOfIdentityValueFqdnOptionsDef1, OneOfIdentityValueFqdnOptionsDef2]


@dataclass
class OneOfIkeV2LocalIdentityOptionsDef4:
    email: Union[OneOfIdentityValueEmailOptionsDef1, OneOfIdentityValueEmailOptionsDef2]


@dataclass
class OneOfIdentityValueKeyIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIdentityValueKeyIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeV2LocalIdentityOptionsDef5:
    key_id: Union[OneOfIdentityValueKeyIdOptionsDef1, OneOfIdentityValueKeyIdOptionsDef2] = _field(
        metadata={"alias": "keyId"}
    )


@dataclass
class OneOfIkeV2LocalIdentityOptionsDef6:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIkeV2RemoteIdentityOptionsDef1:
    ipv4_addr: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipv4Addr"})


@dataclass
class OneOfIkeV2RemoteIdentityOptionsDef2:
    ipv6_prefix: Union[
        OneOfIpv6PrefixGlobalVariableWithoutDefault1, OneOfIpv6PrefixGlobalVariableWithoutDefault2
    ] = _field(metadata={"alias": "ipv6Prefix"})


@dataclass
class OneOfIkeV2RemoteIdentityOptionsDef3:
    fqdn: Union[OneOfIdentityValueFqdnOptionsDef1, OneOfIdentityValueFqdnOptionsDef2]


@dataclass
class OneOfIkeV2RemoteIdentityOptionsDef4:
    email: Union[OneOfIdentityValueEmailOptionsDef1, OneOfIdentityValueEmailOptionsDef2]


@dataclass
class OneOfIkeV2RemoteIdentityOptionsDef5:
    key_id: Union[OneOfIdentityValueKeyIdOptionsDef1, OneOfIdentityValueKeyIdOptionsDef2] = _field(
        metadata={"alias": "keyId"}
    )


@dataclass
class OneOfIkeV2RemoteIdentityOptionsDef6:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class IkeV2:
    """
    IKE V2 config
    """

    ike_rekey_interval: Union[
        OneOfIkeRekeyIntervalOptionsDef1,
        OneOfIkeRekeyIntervalOptionsDef2,
        OneOfIkeRekeyIntervalOptionsDef3,
    ] = _field(metadata={"alias": "ikeRekeyInterval"})
    pre_shared_secret: Union[OneOfPreSharedSecretOptionsDef1, OneOfPreSharedSecretOptionsDef2] = (
        _field(metadata={"alias": "preSharedSecret"})
    )
    ike_local_id: Optional[
        Union[
            OneOfIkeV2LocalIdentityOptionsDef1,
            OneOfIkeV2LocalIdentityOptionsDef2,
            OneOfIkeV2LocalIdentityOptionsDef3,
            OneOfIkeV2LocalIdentityOptionsDef4,
            OneOfIkeV2LocalIdentityOptionsDef5,
            OneOfIkeV2LocalIdentityOptionsDef6,
        ]
    ] = _field(default=None, metadata={"alias": "ikeLocalId"})
    ike_remote_id: Optional[
        Union[
            OneOfIkeV2RemoteIdentityOptionsDef1,
            OneOfIkeV2RemoteIdentityOptionsDef2,
            OneOfIkeV2RemoteIdentityOptionsDef3,
            OneOfIkeV2RemoteIdentityOptionsDef4,
            OneOfIkeV2RemoteIdentityOptionsDef5,
            OneOfIkeV2RemoteIdentityOptionsDef6,
        ]
    ] = _field(default=None, metadata={"alias": "ikeRemoteId"})


@dataclass
class OneOfIpsecRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpsecRekeyIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpsecRekeyIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpsecReplayWindowOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpsecReplayWindowOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpsecReplayWindowOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpsecCipherSuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IpsecCipherSuiteDef


@dataclass
class OneOfIpsecCipherSuiteOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpsecCipherSuiteOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultIpsecCipherSuiteDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPerfectForwardSecrecyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PerfectForwardSecrecyDef


@dataclass
class OneOfPerfectForwardSecrecyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPerfectForwardSecrecyOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultPerfectForwardSecrecyDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Ipsec:
    """
    ipsec config
    """

    ipsec_cipher_suite: Union[
        OneOfIpsecCipherSuiteOptionsDef1,
        OneOfIpsecCipherSuiteOptionsDef2,
        OneOfIpsecCipherSuiteOptionsDef3,
    ] = _field(metadata={"alias": "ipsecCipherSuite"})
    ipsec_rekey_interval: Union[
        OneOfIpsecRekeyIntervalOptionsDef1,
        OneOfIpsecRekeyIntervalOptionsDef2,
        OneOfIpsecRekeyIntervalOptionsDef3,
    ] = _field(metadata={"alias": "ipsecRekeyInterval"})
    ipsec_replay_window: Union[
        OneOfIpsecReplayWindowOptionsDef1,
        OneOfIpsecReplayWindowOptionsDef2,
        OneOfIpsecReplayWindowOptionsDef3,
    ] = _field(metadata={"alias": "ipsecReplayWindow"})
    perfect_forward_secrecy: Union[
        OneOfPerfectForwardSecrecyOptionsDef1,
        OneOfPerfectForwardSecrecyOptionsDef2,
        OneOfPerfectForwardSecrecyOptionsDef3,
    ] = _field(metadata={"alias": "perfectForwardSecrecy"})


@dataclass
class Data1:
    # dead-peer detection
    dpd: Dpd
    if_name: Union[OneOfIpsecIfNameOptionsDef1, OneOfIpsecIfNameOptionsDef2] = _field(
        metadata={"alias": "ifName"}
    )
    # IKE V2 config
    ike_v2: IkeV2 = _field(metadata={"alias": "ikeV2"})
    ike_version: IkeVersion = _field(metadata={"alias": "ikeVersion"})
    # ipsec config
    ipsec: Ipsec
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tunnel_mode: OneOfTunnelModeOptionsDef = _field(metadata={"alias": "tunnelMode"})
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)
    # IKEv1 config
    ike_v1: Optional[IkeV1] = _field(default=None, metadata={"alias": "ikeV1"})
    # Tunnel Config for Mode ipv4
    tunnel_config4o4: Optional[TunnelConfig4O4] = _field(
        default=None, metadata={"alias": "tunnelConfig4o4"}
    )
    # Tunnel Config for Mode ipv6 over ipv4
    tunnel_config6o4: Optional[TunnelConfig6O4] = _field(
        default=None, metadata={"alias": "tunnelConfig6o4"}
    )
    # Tunnel Config for Mode ipv6
    tunnel_config6o6: Optional[TunnelConfig6O6] = _field(
        default=None, metadata={"alias": "tunnelConfig6o6"}
    )
    tunnel_route_via: Optional[
        Union[
            OneOfTunnelRouteViaOptionsDef1,
            OneOfTunnelRouteViaOptionsDef2,
            OneOfTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    # Tunnel Vrf
    tunnel_vrf: Optional[Union[TunnelVrf1, TunnelVrf2]] = _field(
        default=None, metadata={"alias": "tunnelVrf"}
    )


@dataclass
class OneOfIkeVersionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Data2:
    # dead-peer detection
    dpd: Dpd
    if_name: Union[OneOfIpsecIfNameOptionsDef1, OneOfIpsecIfNameOptionsDef2] = _field(
        metadata={"alias": "ifName"}
    )
    ike_version: OneOfIkeVersionOptionsDef = _field(metadata={"alias": "ikeVersion"})
    # ipsec config
    ipsec: Ipsec
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tunnel_mode: OneOfTunnelModeOptionsDef = _field(metadata={"alias": "tunnelMode"})
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)
    # IKEv1 config
    ike_v1: Optional[IkeV1] = _field(default=None, metadata={"alias": "ikeV1"})
    # IKE V2 config
    ike_v2: Optional[IkeV2] = _field(default=None, metadata={"alias": "ikeV2"})
    # Tunnel Config for Mode ipv4
    tunnel_config4o4: Optional[TunnelConfig4O4] = _field(
        default=None, metadata={"alias": "tunnelConfig4o4"}
    )
    # Tunnel Config for Mode ipv6 over ipv4
    tunnel_config6o4: Optional[TunnelConfig6O4] = _field(
        default=None, metadata={"alias": "tunnelConfig6o4"}
    )
    # Tunnel Config for Mode ipv6
    tunnel_config6o6: Optional[TunnelConfig6O6] = _field(
        default=None, metadata={"alias": "tunnelConfig6o6"}
    )
    tunnel_route_via: Optional[
        Union[
            OneOfTunnelRouteViaOptionsDef1,
            OneOfTunnelRouteViaOptionsDef2,
            OneOfTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    # Tunnel Vrf
    tunnel_vrf: Optional[Union[TunnelVrf1, TunnelVrf2]] = _field(
        default=None, metadata={"alias": "tunnelVrf"}
    )


@dataclass
class Payload:
    """
    IPSec interface feature schema in WAN VRF
    """

    data: Union[Data1, Data2]
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
    # IPSec interface feature schema in WAN VRF
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingTransportVrfWanInterfaceIpsecPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingTransportVrfInterfaceIpsecFeatureForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdroutingTransportVrfInterfaceIpsecFeatureForTransportPostRequest:
    """
    IPSec interface feature schema in WAN VRF
    """

    data: Union[Data1, Data2]
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdRoutingTransportVrfWanInterfaceIpsecPayload:
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
    # IPSec interface feature schema in WAN VRF
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingTransportVrfInterfaceIpsecFeatureForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EditSdroutingTransportVrfInterfaceIpsecFeatureForTransportPutRequest:
    """
    IPSec interface feature schema in WAN VRF
    """

    data: Union[Data1, Data2]
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
