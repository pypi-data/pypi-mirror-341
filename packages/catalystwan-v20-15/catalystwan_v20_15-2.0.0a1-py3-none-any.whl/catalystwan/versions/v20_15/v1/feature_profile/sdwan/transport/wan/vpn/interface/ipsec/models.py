# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

TunnelModeDef = Literal["ipv4", "ipv4-v6overlay", "ipv6"]

DefaultTunnelModeDef = Literal["ipv4"]

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

ApplicationDef = Literal["none", "sig"]

IkeModeDef = Literal["aggressive", "main"]

DefaultIkeModeDef = Literal["main"]

IkeCiphersuiteDef = Literal[
    "aes128-cbc-sha1", "aes128-cbc-sha2", "aes256-cbc-sha1", "aes256-cbc-sha2"
]

DefaultIkeCiphersuiteDef = Literal["aes256-cbc-sha1"]

IkeGroupDef = Literal["14", "15", "16", "19", "2", "20", "21", "24"]

DefaultIkeGroupDef = Literal["16"]

IpsecCiphersuiteDef = Literal[
    "aes256-cbc-sha1",
    "aes256-cbc-sha256",
    "aes256-cbc-sha384",
    "aes256-cbc-sha512",
    "aes256-gcm",
    "null-sha1",
    "null-sha256",
    "null-sha384",
    "null-sha512",
]

DefaultIpsecCiphersuiteDef = Literal["aes256-gcm"]

PerfectForwardSecrecyDef = Literal[
    "group-1",
    "group-14",
    "group-15",
    "group-16",
    "group-19",
    "group-2",
    "group-20",
    "group-21",
    "group-24",
    "group-5",
    "none",
]

DefaultPerfectForwardSecrecyDef = Literal["group-16"]


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
class OneOfMultiplexingOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfMultiplexingOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMultiplexingOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTunnelModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TunnelModeDef


@dataclass
class OneOfTunnelModeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultTunnelModeDef  # pytype: disable=annotation-type-mismatch


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
class OneOfIpV4AddressOptionsWithDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4AddressOptionsWithDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfIpV4AddressOptionsWithDefault3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpV4SubnetMaskOptionsWithDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4SubnetMaskOptionsWithDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4SubnetMaskDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpV4SubnetMaskOptionsWithDefault3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Ipv4AddressAndMaskWithDefault:
    address: Optional[
        Union[
            OneOfIpV4AddressOptionsWithDefault1,
            OneOfIpV4AddressOptionsWithDefault2,
            OneOfIpV4AddressOptionsWithDefault3,
        ]
    ] = _field(default=None)
    mask: Optional[
        Union[
            OneOfIpV4SubnetMaskOptionsWithDefault1,
            OneOfIpV4SubnetMaskOptionsWithDefault2,
            OneOfIpV4SubnetMaskOptionsWithDefault3,
        ]
    ] = _field(default=None)


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
class OneOfApplicationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ApplicationDef


@dataclass
class OneOfApplicationOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


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
class OneOfIkeVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIkeVersionOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIkeModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IkeModeDef


@dataclass
class OneOfIkeModeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeModeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultIkeModeDef  # pytype: disable=annotation-type-mismatch


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
class OneOfIkeCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IkeCiphersuiteDef


@dataclass
class OneOfIkeCiphersuiteOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeCiphersuiteOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultIkeCiphersuiteDef  # pytype: disable=annotation-type-mismatch


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
class OneOfIkeLocalIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIkeLocalIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeLocalIdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIkeRemoteIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIkeRemoteIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeRemoteIdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


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
class OneOfIpsecCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IpsecCiphersuiteDef


@dataclass
class OneOfIpsecCiphersuiteOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpsecCiphersuiteOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultIpsecCiphersuiteDef  # pytype: disable=annotation-type-mismatch


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
class OneOfTrackerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTrackerOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


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
class Data1:
    address: Ipv4AddressAndMaskWithDefault
    application: Union[OneOfApplicationOptionsDef1, OneOfApplicationOptionsDef2]
    clear_dont_fragment: Union[
        OneOfClearDontFragmentOptionsDef1,
        OneOfClearDontFragmentOptionsDef2,
        OneOfClearDontFragmentOptionsDef3,
    ] = _field(metadata={"alias": "clearDontFragment"})
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    dpd_interval: Union[
        OneOfDpdIntervalOptionsDef1, OneOfDpdIntervalOptionsDef2, OneOfDpdIntervalOptionsDef3
    ] = _field(metadata={"alias": "dpdInterval"})
    dpd_retries: Union[
        OneOfDpdRetriesOptionsDef1, OneOfDpdRetriesOptionsDef2, OneOfDpdRetriesOptionsDef3
    ] = _field(metadata={"alias": "dpdRetries"})
    if_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "ifName"}
    )
    ike_ciphersuite: Union[
        OneOfIkeCiphersuiteOptionsDef1,
        OneOfIkeCiphersuiteOptionsDef2,
        OneOfIkeCiphersuiteOptionsDef3,
    ] = _field(metadata={"alias": "ikeCiphersuite"})
    ike_group: Union[
        OneOfIkeGroupOptionsDef1, OneOfIkeGroupOptionsDef2, OneOfIkeGroupOptionsDef3
    ] = _field(metadata={"alias": "ikeGroup"})
    ike_local_id: Union[
        OneOfIkeLocalIdOptionsDef1, OneOfIkeLocalIdOptionsDef2, OneOfIkeLocalIdOptionsDef3
    ] = _field(metadata={"alias": "ikeLocalId"})
    ike_rekey_interval: Union[
        OneOfIkeRekeyIntervalOptionsDef1,
        OneOfIkeRekeyIntervalOptionsDef2,
        OneOfIkeRekeyIntervalOptionsDef3,
    ] = _field(metadata={"alias": "ikeRekeyInterval"})
    ike_remote_id: Union[
        OneOfIkeRemoteIdOptionsDef1, OneOfIkeRemoteIdOptionsDef2, OneOfIkeRemoteIdOptionsDef3
    ] = _field(metadata={"alias": "ikeRemoteId"})
    ike_version: Union[OneOfIkeVersionOptionsDef1, OneOfIkeVersionOptionsDef2] = _field(
        metadata={"alias": "ikeVersion"}
    )
    ipsec_ciphersuite: Union[
        OneOfIpsecCiphersuiteOptionsDef1,
        OneOfIpsecCiphersuiteOptionsDef2,
        OneOfIpsecCiphersuiteOptionsDef3,
    ] = _field(metadata={"alias": "ipsecCiphersuite"})
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
    mtu: Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3]
    perfect_forward_secrecy: Union[
        OneOfPerfectForwardSecrecyOptionsDef1,
        OneOfPerfectForwardSecrecyOptionsDef2,
        OneOfPerfectForwardSecrecyOptionsDef3,
    ] = _field(metadata={"alias": "perfectForwardSecrecy"})
    pre_shared_secret: Union[OneOfPreSharedSecretOptionsDef1, OneOfPreSharedSecretOptionsDef2] = (
        _field(metadata={"alias": "preSharedSecret"})
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tcp_mss_adjust: Union[
        OneOfTcpMssAdjustOptionsDef1, OneOfTcpMssAdjustOptionsDef2, OneOfTcpMssAdjustOptionsDef3
    ] = _field(metadata={"alias": "tcpMssAdjust"})
    tunnel_destination: Ipv4AddressAndMaskDef = _field(metadata={"alias": "tunnelDestination"})
    tunnel_source: Ipv4AddressAndMaskDef = _field(metadata={"alias": "tunnelSource"})
    ike_mode: Optional[
        Union[OneOfIkeModeOptionsDef1, OneOfIkeModeOptionsDef2, OneOfIkeModeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ikeMode"})
    ipv6_address: Optional[Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2]] = _field(
        default=None, metadata={"alias": "ipv6Address"}
    )
    mtu_v6: Optional[Union[OneOfMtuV6OptionsDef1, OneOfMtuV6OptionsDef2, OneOfMtuV6OptionsDef3]] = (
        _field(default=None, metadata={"alias": "mtuV6"})
    )
    multiplexing: Optional[
        Union[
            OneOfMultiplexingOptionsDef1, OneOfMultiplexingOptionsDef2, OneOfMultiplexingOptionsDef3
        ]
    ] = _field(default=None)
    tcp_mss_adjust_v6: Optional[
        Union[
            OneOfTcpMssAdjustV6OptionsDef1,
            OneOfTcpMssAdjustV6OptionsDef2,
            OneOfTcpMssAdjustV6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjustV6"})
    tracker: Optional[
        Union[OneOfTrackerOptionsDef1, OneOfTrackerOptionsDef2, OneOfTrackerOptionsDef3]
    ] = _field(default=None)
    tunnel_destination_v6: Optional[
        Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelDestinationV6"})
    tunnel_mode: Optional[Union[OneOfTunnelModeOptionsDef1, OneOfTunnelModeOptionsDef2]] = _field(
        default=None, metadata={"alias": "tunnelMode"}
    )
    tunnel_route_via: Optional[
        Union[
            OneOfTunnelRouteViaOptionsDef1,
            OneOfTunnelRouteViaOptionsDef2,
            OneOfTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    tunnel_source_interface: Optional[
        Union[OneOfTunnelSourceInterfaceOptionsDef1, OneOfTunnelSourceInterfaceOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelSourceInterface"})
    tunnel_source_v6: Optional[Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2]] = (
        _field(default=None, metadata={"alias": "tunnelSourceV6"})
    )


@dataclass
class Data2:
    address: Ipv4AddressAndMaskWithDefault
    application: Union[OneOfApplicationOptionsDef1, OneOfApplicationOptionsDef2]
    clear_dont_fragment: Union[
        OneOfClearDontFragmentOptionsDef1,
        OneOfClearDontFragmentOptionsDef2,
        OneOfClearDontFragmentOptionsDef3,
    ] = _field(metadata={"alias": "clearDontFragment"})
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    dpd_interval: Union[
        OneOfDpdIntervalOptionsDef1, OneOfDpdIntervalOptionsDef2, OneOfDpdIntervalOptionsDef3
    ] = _field(metadata={"alias": "dpdInterval"})
    dpd_retries: Union[
        OneOfDpdRetriesOptionsDef1, OneOfDpdRetriesOptionsDef2, OneOfDpdRetriesOptionsDef3
    ] = _field(metadata={"alias": "dpdRetries"})
    if_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "ifName"}
    )
    ike_ciphersuite: Union[
        OneOfIkeCiphersuiteOptionsDef1,
        OneOfIkeCiphersuiteOptionsDef2,
        OneOfIkeCiphersuiteOptionsDef3,
    ] = _field(metadata={"alias": "ikeCiphersuite"})
    ike_group: Union[
        OneOfIkeGroupOptionsDef1, OneOfIkeGroupOptionsDef2, OneOfIkeGroupOptionsDef3
    ] = _field(metadata={"alias": "ikeGroup"})
    ike_local_id: Union[
        OneOfIkeLocalIdOptionsDef1, OneOfIkeLocalIdOptionsDef2, OneOfIkeLocalIdOptionsDef3
    ] = _field(metadata={"alias": "ikeLocalId"})
    ike_rekey_interval: Union[
        OneOfIkeRekeyIntervalOptionsDef1,
        OneOfIkeRekeyIntervalOptionsDef2,
        OneOfIkeRekeyIntervalOptionsDef3,
    ] = _field(metadata={"alias": "ikeRekeyInterval"})
    ike_remote_id: Union[
        OneOfIkeRemoteIdOptionsDef1, OneOfIkeRemoteIdOptionsDef2, OneOfIkeRemoteIdOptionsDef3
    ] = _field(metadata={"alias": "ikeRemoteId"})
    ike_version: Union[OneOfIkeVersionOptionsDef1, OneOfIkeVersionOptionsDef2] = _field(
        metadata={"alias": "ikeVersion"}
    )
    ipsec_ciphersuite: Union[
        OneOfIpsecCiphersuiteOptionsDef1,
        OneOfIpsecCiphersuiteOptionsDef2,
        OneOfIpsecCiphersuiteOptionsDef3,
    ] = _field(metadata={"alias": "ipsecCiphersuite"})
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
    mtu: Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3]
    perfect_forward_secrecy: Union[
        OneOfPerfectForwardSecrecyOptionsDef1,
        OneOfPerfectForwardSecrecyOptionsDef2,
        OneOfPerfectForwardSecrecyOptionsDef3,
    ] = _field(metadata={"alias": "perfectForwardSecrecy"})
    pre_shared_secret: Union[OneOfPreSharedSecretOptionsDef1, OneOfPreSharedSecretOptionsDef2] = (
        _field(metadata={"alias": "preSharedSecret"})
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tcp_mss_adjust: Union[
        OneOfTcpMssAdjustOptionsDef1, OneOfTcpMssAdjustOptionsDef2, OneOfTcpMssAdjustOptionsDef3
    ] = _field(metadata={"alias": "tcpMssAdjust"})
    tunnel_destination: Ipv4AddressAndMaskDef = _field(metadata={"alias": "tunnelDestination"})
    tunnel_source_interface: Union[
        OneOfTunnelSourceInterfaceOptionsDef1, OneOfTunnelSourceInterfaceOptionsDef2
    ] = _field(metadata={"alias": "tunnelSourceInterface"})
    ike_mode: Optional[
        Union[OneOfIkeModeOptionsDef1, OneOfIkeModeOptionsDef2, OneOfIkeModeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ikeMode"})
    ipv6_address: Optional[Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2]] = _field(
        default=None, metadata={"alias": "ipv6Address"}
    )
    mtu_v6: Optional[Union[OneOfMtuV6OptionsDef1, OneOfMtuV6OptionsDef2, OneOfMtuV6OptionsDef3]] = (
        _field(default=None, metadata={"alias": "mtuV6"})
    )
    multiplexing: Optional[
        Union[
            OneOfMultiplexingOptionsDef1, OneOfMultiplexingOptionsDef2, OneOfMultiplexingOptionsDef3
        ]
    ] = _field(default=None)
    tcp_mss_adjust_v6: Optional[
        Union[
            OneOfTcpMssAdjustV6OptionsDef1,
            OneOfTcpMssAdjustV6OptionsDef2,
            OneOfTcpMssAdjustV6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjustV6"})
    tracker: Optional[
        Union[OneOfTrackerOptionsDef1, OneOfTrackerOptionsDef2, OneOfTrackerOptionsDef3]
    ] = _field(default=None)
    tunnel_destination_v6: Optional[
        Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelDestinationV6"})
    tunnel_mode: Optional[Union[OneOfTunnelModeOptionsDef1, OneOfTunnelModeOptionsDef2]] = _field(
        default=None, metadata={"alias": "tunnelMode"}
    )
    tunnel_route_via: Optional[
        Union[
            OneOfTunnelRouteViaOptionsDef1,
            OneOfTunnelRouteViaOptionsDef2,
            OneOfTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    tunnel_source: Optional[Ipv4AddressAndMaskDef] = _field(
        default=None, metadata={"alias": "tunnelSource"}
    )
    tunnel_source_v6: Optional[Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2]] = (
        _field(default=None, metadata={"alias": "tunnelSourceV6"})
    )


@dataclass
class Data3:
    application: Union[OneOfApplicationOptionsDef1, OneOfApplicationOptionsDef2]
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    dpd_interval: Union[
        OneOfDpdIntervalOptionsDef1, OneOfDpdIntervalOptionsDef2, OneOfDpdIntervalOptionsDef3
    ] = _field(metadata={"alias": "dpdInterval"})
    dpd_retries: Union[
        OneOfDpdRetriesOptionsDef1, OneOfDpdRetriesOptionsDef2, OneOfDpdRetriesOptionsDef3
    ] = _field(metadata={"alias": "dpdRetries"})
    if_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "ifName"}
    )
    ike_ciphersuite: Union[
        OneOfIkeCiphersuiteOptionsDef1,
        OneOfIkeCiphersuiteOptionsDef2,
        OneOfIkeCiphersuiteOptionsDef3,
    ] = _field(metadata={"alias": "ikeCiphersuite"})
    ike_group: Union[
        OneOfIkeGroupOptionsDef1, OneOfIkeGroupOptionsDef2, OneOfIkeGroupOptionsDef3
    ] = _field(metadata={"alias": "ikeGroup"})
    ike_local_id: Union[
        OneOfIkeLocalIdOptionsDef1, OneOfIkeLocalIdOptionsDef2, OneOfIkeLocalIdOptionsDef3
    ] = _field(metadata={"alias": "ikeLocalId"})
    ike_rekey_interval: Union[
        OneOfIkeRekeyIntervalOptionsDef1,
        OneOfIkeRekeyIntervalOptionsDef2,
        OneOfIkeRekeyIntervalOptionsDef3,
    ] = _field(metadata={"alias": "ikeRekeyInterval"})
    ike_remote_id: Union[
        OneOfIkeRemoteIdOptionsDef1, OneOfIkeRemoteIdOptionsDef2, OneOfIkeRemoteIdOptionsDef3
    ] = _field(metadata={"alias": "ikeRemoteId"})
    ike_version: Union[OneOfIkeVersionOptionsDef1, OneOfIkeVersionOptionsDef2] = _field(
        metadata={"alias": "ikeVersion"}
    )
    ipsec_ciphersuite: Union[
        OneOfIpsecCiphersuiteOptionsDef1,
        OneOfIpsecCiphersuiteOptionsDef2,
        OneOfIpsecCiphersuiteOptionsDef3,
    ] = _field(metadata={"alias": "ipsecCiphersuite"})
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
    ipv6_address: Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2] = _field(
        metadata={"alias": "ipv6Address"}
    )
    mtu_v6: Union[OneOfMtuV6OptionsDef1, OneOfMtuV6OptionsDef2, OneOfMtuV6OptionsDef3] = _field(
        metadata={"alias": "mtuV6"}
    )
    perfect_forward_secrecy: Union[
        OneOfPerfectForwardSecrecyOptionsDef1,
        OneOfPerfectForwardSecrecyOptionsDef2,
        OneOfPerfectForwardSecrecyOptionsDef3,
    ] = _field(metadata={"alias": "perfectForwardSecrecy"})
    pre_shared_secret: Union[OneOfPreSharedSecretOptionsDef1, OneOfPreSharedSecretOptionsDef2] = (
        _field(metadata={"alias": "preSharedSecret"})
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tcp_mss_adjust_v6: Union[
        OneOfTcpMssAdjustV6OptionsDef1,
        OneOfTcpMssAdjustV6OptionsDef2,
        OneOfTcpMssAdjustV6OptionsDef3,
    ] = _field(metadata={"alias": "tcpMssAdjustV6"})
    tunnel_destination_v6: Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2] = _field(
        metadata={"alias": "tunnelDestinationV6"}
    )
    tunnel_source_v6: Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2] = _field(
        metadata={"alias": "tunnelSourceV6"}
    )
    address: Optional[Ipv4AddressAndMaskWithDefault] = _field(default=None)
    clear_dont_fragment: Optional[
        Union[
            OneOfClearDontFragmentOptionsDef1,
            OneOfClearDontFragmentOptionsDef2,
            OneOfClearDontFragmentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "clearDontFragment"})
    ike_mode: Optional[
        Union[OneOfIkeModeOptionsDef1, OneOfIkeModeOptionsDef2, OneOfIkeModeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ikeMode"})
    mtu: Optional[Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3]] = _field(
        default=None
    )
    multiplexing: Optional[
        Union[
            OneOfMultiplexingOptionsDef1, OneOfMultiplexingOptionsDef2, OneOfMultiplexingOptionsDef3
        ]
    ] = _field(default=None)
    tcp_mss_adjust: Optional[
        Union[
            OneOfTcpMssAdjustOptionsDef1, OneOfTcpMssAdjustOptionsDef2, OneOfTcpMssAdjustOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})
    tracker: Optional[
        Union[OneOfTrackerOptionsDef1, OneOfTrackerOptionsDef2, OneOfTrackerOptionsDef3]
    ] = _field(default=None)
    tunnel_destination: Optional[Ipv4AddressAndMaskDef] = _field(
        default=None, metadata={"alias": "tunnelDestination"}
    )
    tunnel_mode: Optional[Union[OneOfTunnelModeOptionsDef1, OneOfTunnelModeOptionsDef2]] = _field(
        default=None, metadata={"alias": "tunnelMode"}
    )
    tunnel_route_via: Optional[
        Union[
            OneOfTunnelRouteViaOptionsDef1,
            OneOfTunnelRouteViaOptionsDef2,
            OneOfTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    tunnel_source: Optional[Ipv4AddressAndMaskDef] = _field(
        default=None, metadata={"alias": "tunnelSource"}
    )
    tunnel_source_interface: Optional[
        Union[OneOfTunnelSourceInterfaceOptionsDef1, OneOfTunnelSourceInterfaceOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelSourceInterface"})


@dataclass
class Data4:
    application: Union[OneOfApplicationOptionsDef1, OneOfApplicationOptionsDef2]
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    dpd_interval: Union[
        OneOfDpdIntervalOptionsDef1, OneOfDpdIntervalOptionsDef2, OneOfDpdIntervalOptionsDef3
    ] = _field(metadata={"alias": "dpdInterval"})
    dpd_retries: Union[
        OneOfDpdRetriesOptionsDef1, OneOfDpdRetriesOptionsDef2, OneOfDpdRetriesOptionsDef3
    ] = _field(metadata={"alias": "dpdRetries"})
    if_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "ifName"}
    )
    ike_ciphersuite: Union[
        OneOfIkeCiphersuiteOptionsDef1,
        OneOfIkeCiphersuiteOptionsDef2,
        OneOfIkeCiphersuiteOptionsDef3,
    ] = _field(metadata={"alias": "ikeCiphersuite"})
    ike_group: Union[
        OneOfIkeGroupOptionsDef1, OneOfIkeGroupOptionsDef2, OneOfIkeGroupOptionsDef3
    ] = _field(metadata={"alias": "ikeGroup"})
    ike_local_id: Union[
        OneOfIkeLocalIdOptionsDef1, OneOfIkeLocalIdOptionsDef2, OneOfIkeLocalIdOptionsDef3
    ] = _field(metadata={"alias": "ikeLocalId"})
    ike_rekey_interval: Union[
        OneOfIkeRekeyIntervalOptionsDef1,
        OneOfIkeRekeyIntervalOptionsDef2,
        OneOfIkeRekeyIntervalOptionsDef3,
    ] = _field(metadata={"alias": "ikeRekeyInterval"})
    ike_remote_id: Union[
        OneOfIkeRemoteIdOptionsDef1, OneOfIkeRemoteIdOptionsDef2, OneOfIkeRemoteIdOptionsDef3
    ] = _field(metadata={"alias": "ikeRemoteId"})
    ike_version: Union[OneOfIkeVersionOptionsDef1, OneOfIkeVersionOptionsDef2] = _field(
        metadata={"alias": "ikeVersion"}
    )
    ipsec_ciphersuite: Union[
        OneOfIpsecCiphersuiteOptionsDef1,
        OneOfIpsecCiphersuiteOptionsDef2,
        OneOfIpsecCiphersuiteOptionsDef3,
    ] = _field(metadata={"alias": "ipsecCiphersuite"})
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
    ipv6_address: Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2] = _field(
        metadata={"alias": "ipv6Address"}
    )
    mtu_v6: Union[OneOfMtuV6OptionsDef1, OneOfMtuV6OptionsDef2, OneOfMtuV6OptionsDef3] = _field(
        metadata={"alias": "mtuV6"}
    )
    perfect_forward_secrecy: Union[
        OneOfPerfectForwardSecrecyOptionsDef1,
        OneOfPerfectForwardSecrecyOptionsDef2,
        OneOfPerfectForwardSecrecyOptionsDef3,
    ] = _field(metadata={"alias": "perfectForwardSecrecy"})
    pre_shared_secret: Union[OneOfPreSharedSecretOptionsDef1, OneOfPreSharedSecretOptionsDef2] = (
        _field(metadata={"alias": "preSharedSecret"})
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tcp_mss_adjust_v6: Union[
        OneOfTcpMssAdjustV6OptionsDef1,
        OneOfTcpMssAdjustV6OptionsDef2,
        OneOfTcpMssAdjustV6OptionsDef3,
    ] = _field(metadata={"alias": "tcpMssAdjustV6"})
    tunnel_destination_v6: Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2] = _field(
        metadata={"alias": "tunnelDestinationV6"}
    )
    tunnel_source_interface: Union[
        OneOfTunnelSourceInterfaceOptionsDef1, OneOfTunnelSourceInterfaceOptionsDef2
    ] = _field(metadata={"alias": "tunnelSourceInterface"})
    address: Optional[Ipv4AddressAndMaskWithDefault] = _field(default=None)
    clear_dont_fragment: Optional[
        Union[
            OneOfClearDontFragmentOptionsDef1,
            OneOfClearDontFragmentOptionsDef2,
            OneOfClearDontFragmentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "clearDontFragment"})
    ike_mode: Optional[
        Union[OneOfIkeModeOptionsDef1, OneOfIkeModeOptionsDef2, OneOfIkeModeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ikeMode"})
    mtu: Optional[Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3]] = _field(
        default=None
    )
    multiplexing: Optional[
        Union[
            OneOfMultiplexingOptionsDef1, OneOfMultiplexingOptionsDef2, OneOfMultiplexingOptionsDef3
        ]
    ] = _field(default=None)
    tcp_mss_adjust: Optional[
        Union[
            OneOfTcpMssAdjustOptionsDef1, OneOfTcpMssAdjustOptionsDef2, OneOfTcpMssAdjustOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})
    tracker: Optional[
        Union[OneOfTrackerOptionsDef1, OneOfTrackerOptionsDef2, OneOfTrackerOptionsDef3]
    ] = _field(default=None)
    tunnel_destination: Optional[Ipv4AddressAndMaskDef] = _field(
        default=None, metadata={"alias": "tunnelDestination"}
    )
    tunnel_mode: Optional[Union[OneOfTunnelModeOptionsDef1, OneOfTunnelModeOptionsDef2]] = _field(
        default=None, metadata={"alias": "tunnelMode"}
    )
    tunnel_route_via: Optional[
        Union[
            OneOfTunnelRouteViaOptionsDef1,
            OneOfTunnelRouteViaOptionsDef2,
            OneOfTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    tunnel_source: Optional[Ipv4AddressAndMaskDef] = _field(
        default=None, metadata={"alias": "tunnelSource"}
    )
    tunnel_source_v6: Optional[Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2]] = (
        _field(default=None, metadata={"alias": "tunnelSourceV6"})
    )


@dataclass
class Data5:
    application: Union[OneOfApplicationOptionsDef1, OneOfApplicationOptionsDef2]
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    dpd_interval: Union[
        OneOfDpdIntervalOptionsDef1, OneOfDpdIntervalOptionsDef2, OneOfDpdIntervalOptionsDef3
    ] = _field(metadata={"alias": "dpdInterval"})
    dpd_retries: Union[
        OneOfDpdRetriesOptionsDef1, OneOfDpdRetriesOptionsDef2, OneOfDpdRetriesOptionsDef3
    ] = _field(metadata={"alias": "dpdRetries"})
    if_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "ifName"}
    )
    ike_ciphersuite: Union[
        OneOfIkeCiphersuiteOptionsDef1,
        OneOfIkeCiphersuiteOptionsDef2,
        OneOfIkeCiphersuiteOptionsDef3,
    ] = _field(metadata={"alias": "ikeCiphersuite"})
    ike_group: Union[
        OneOfIkeGroupOptionsDef1, OneOfIkeGroupOptionsDef2, OneOfIkeGroupOptionsDef3
    ] = _field(metadata={"alias": "ikeGroup"})
    ike_local_id: Union[
        OneOfIkeLocalIdOptionsDef1, OneOfIkeLocalIdOptionsDef2, OneOfIkeLocalIdOptionsDef3
    ] = _field(metadata={"alias": "ikeLocalId"})
    ike_rekey_interval: Union[
        OneOfIkeRekeyIntervalOptionsDef1,
        OneOfIkeRekeyIntervalOptionsDef2,
        OneOfIkeRekeyIntervalOptionsDef3,
    ] = _field(metadata={"alias": "ikeRekeyInterval"})
    ike_remote_id: Union[
        OneOfIkeRemoteIdOptionsDef1, OneOfIkeRemoteIdOptionsDef2, OneOfIkeRemoteIdOptionsDef3
    ] = _field(metadata={"alias": "ikeRemoteId"})
    ike_version: Union[OneOfIkeVersionOptionsDef1, OneOfIkeVersionOptionsDef2] = _field(
        metadata={"alias": "ikeVersion"}
    )
    ipsec_ciphersuite: Union[
        OneOfIpsecCiphersuiteOptionsDef1,
        OneOfIpsecCiphersuiteOptionsDef2,
        OneOfIpsecCiphersuiteOptionsDef3,
    ] = _field(metadata={"alias": "ipsecCiphersuite"})
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
    ipv6_address: Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2] = _field(
        metadata={"alias": "ipv6Address"}
    )
    mtu_v6: Union[OneOfMtuV6OptionsDef1, OneOfMtuV6OptionsDef2, OneOfMtuV6OptionsDef3] = _field(
        metadata={"alias": "mtuV6"}
    )
    perfect_forward_secrecy: Union[
        OneOfPerfectForwardSecrecyOptionsDef1,
        OneOfPerfectForwardSecrecyOptionsDef2,
        OneOfPerfectForwardSecrecyOptionsDef3,
    ] = _field(metadata={"alias": "perfectForwardSecrecy"})
    pre_shared_secret: Union[OneOfPreSharedSecretOptionsDef1, OneOfPreSharedSecretOptionsDef2] = (
        _field(metadata={"alias": "preSharedSecret"})
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tcp_mss_adjust_v6: Union[
        OneOfTcpMssAdjustV6OptionsDef1,
        OneOfTcpMssAdjustV6OptionsDef2,
        OneOfTcpMssAdjustV6OptionsDef3,
    ] = _field(metadata={"alias": "tcpMssAdjustV6"})
    tunnel_destination: Ipv4AddressAndMaskDef = _field(metadata={"alias": "tunnelDestination"})
    tunnel_source: Ipv4AddressAndMaskDef = _field(metadata={"alias": "tunnelSource"})
    address: Optional[Ipv4AddressAndMaskWithDefault] = _field(default=None)
    clear_dont_fragment: Optional[
        Union[
            OneOfClearDontFragmentOptionsDef1,
            OneOfClearDontFragmentOptionsDef2,
            OneOfClearDontFragmentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "clearDontFragment"})
    ike_mode: Optional[
        Union[OneOfIkeModeOptionsDef1, OneOfIkeModeOptionsDef2, OneOfIkeModeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ikeMode"})
    mtu: Optional[Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3]] = _field(
        default=None
    )
    multiplexing: Optional[
        Union[
            OneOfMultiplexingOptionsDef1, OneOfMultiplexingOptionsDef2, OneOfMultiplexingOptionsDef3
        ]
    ] = _field(default=None)
    tcp_mss_adjust: Optional[
        Union[
            OneOfTcpMssAdjustOptionsDef1, OneOfTcpMssAdjustOptionsDef2, OneOfTcpMssAdjustOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})
    tracker: Optional[
        Union[OneOfTrackerOptionsDef1, OneOfTrackerOptionsDef2, OneOfTrackerOptionsDef3]
    ] = _field(default=None)
    tunnel_destination_v6: Optional[
        Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelDestinationV6"})
    tunnel_mode: Optional[Union[OneOfTunnelModeOptionsDef1, OneOfTunnelModeOptionsDef2]] = _field(
        default=None, metadata={"alias": "tunnelMode"}
    )
    tunnel_route_via: Optional[
        Union[
            OneOfTunnelRouteViaOptionsDef1,
            OneOfTunnelRouteViaOptionsDef2,
            OneOfTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    tunnel_source_interface: Optional[
        Union[OneOfTunnelSourceInterfaceOptionsDef1, OneOfTunnelSourceInterfaceOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelSourceInterface"})
    tunnel_source_v6: Optional[Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2]] = (
        _field(default=None, metadata={"alias": "tunnelSourceV6"})
    )


@dataclass
class Data6:
    application: Union[OneOfApplicationOptionsDef1, OneOfApplicationOptionsDef2]
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    dpd_interval: Union[
        OneOfDpdIntervalOptionsDef1, OneOfDpdIntervalOptionsDef2, OneOfDpdIntervalOptionsDef3
    ] = _field(metadata={"alias": "dpdInterval"})
    dpd_retries: Union[
        OneOfDpdRetriesOptionsDef1, OneOfDpdRetriesOptionsDef2, OneOfDpdRetriesOptionsDef3
    ] = _field(metadata={"alias": "dpdRetries"})
    if_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "ifName"}
    )
    ike_ciphersuite: Union[
        OneOfIkeCiphersuiteOptionsDef1,
        OneOfIkeCiphersuiteOptionsDef2,
        OneOfIkeCiphersuiteOptionsDef3,
    ] = _field(metadata={"alias": "ikeCiphersuite"})
    ike_group: Union[
        OneOfIkeGroupOptionsDef1, OneOfIkeGroupOptionsDef2, OneOfIkeGroupOptionsDef3
    ] = _field(metadata={"alias": "ikeGroup"})
    ike_local_id: Union[
        OneOfIkeLocalIdOptionsDef1, OneOfIkeLocalIdOptionsDef2, OneOfIkeLocalIdOptionsDef3
    ] = _field(metadata={"alias": "ikeLocalId"})
    ike_rekey_interval: Union[
        OneOfIkeRekeyIntervalOptionsDef1,
        OneOfIkeRekeyIntervalOptionsDef2,
        OneOfIkeRekeyIntervalOptionsDef3,
    ] = _field(metadata={"alias": "ikeRekeyInterval"})
    ike_remote_id: Union[
        OneOfIkeRemoteIdOptionsDef1, OneOfIkeRemoteIdOptionsDef2, OneOfIkeRemoteIdOptionsDef3
    ] = _field(metadata={"alias": "ikeRemoteId"})
    ike_version: Union[OneOfIkeVersionOptionsDef1, OneOfIkeVersionOptionsDef2] = _field(
        metadata={"alias": "ikeVersion"}
    )
    ipsec_ciphersuite: Union[
        OneOfIpsecCiphersuiteOptionsDef1,
        OneOfIpsecCiphersuiteOptionsDef2,
        OneOfIpsecCiphersuiteOptionsDef3,
    ] = _field(metadata={"alias": "ipsecCiphersuite"})
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
    ipv6_address: Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2] = _field(
        metadata={"alias": "ipv6Address"}
    )
    mtu_v6: Union[OneOfMtuV6OptionsDef1, OneOfMtuV6OptionsDef2, OneOfMtuV6OptionsDef3] = _field(
        metadata={"alias": "mtuV6"}
    )
    perfect_forward_secrecy: Union[
        OneOfPerfectForwardSecrecyOptionsDef1,
        OneOfPerfectForwardSecrecyOptionsDef2,
        OneOfPerfectForwardSecrecyOptionsDef3,
    ] = _field(metadata={"alias": "perfectForwardSecrecy"})
    pre_shared_secret: Union[OneOfPreSharedSecretOptionsDef1, OneOfPreSharedSecretOptionsDef2] = (
        _field(metadata={"alias": "preSharedSecret"})
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tcp_mss_adjust_v6: Union[
        OneOfTcpMssAdjustV6OptionsDef1,
        OneOfTcpMssAdjustV6OptionsDef2,
        OneOfTcpMssAdjustV6OptionsDef3,
    ] = _field(metadata={"alias": "tcpMssAdjustV6"})
    tunnel_destination: Ipv4AddressAndMaskDef = _field(metadata={"alias": "tunnelDestination"})
    tunnel_source_interface: Union[
        OneOfTunnelSourceInterfaceOptionsDef1, OneOfTunnelSourceInterfaceOptionsDef2
    ] = _field(metadata={"alias": "tunnelSourceInterface"})
    address: Optional[Ipv4AddressAndMaskWithDefault] = _field(default=None)
    clear_dont_fragment: Optional[
        Union[
            OneOfClearDontFragmentOptionsDef1,
            OneOfClearDontFragmentOptionsDef2,
            OneOfClearDontFragmentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "clearDontFragment"})
    ike_mode: Optional[
        Union[OneOfIkeModeOptionsDef1, OneOfIkeModeOptionsDef2, OneOfIkeModeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ikeMode"})
    mtu: Optional[Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3]] = _field(
        default=None
    )
    multiplexing: Optional[
        Union[
            OneOfMultiplexingOptionsDef1, OneOfMultiplexingOptionsDef2, OneOfMultiplexingOptionsDef3
        ]
    ] = _field(default=None)
    tcp_mss_adjust: Optional[
        Union[
            OneOfTcpMssAdjustOptionsDef1, OneOfTcpMssAdjustOptionsDef2, OneOfTcpMssAdjustOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})
    tracker: Optional[
        Union[OneOfTrackerOptionsDef1, OneOfTrackerOptionsDef2, OneOfTrackerOptionsDef3]
    ] = _field(default=None)
    tunnel_destination_v6: Optional[
        Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelDestinationV6"})
    tunnel_mode: Optional[Union[OneOfTunnelModeOptionsDef1, OneOfTunnelModeOptionsDef2]] = _field(
        default=None, metadata={"alias": "tunnelMode"}
    )
    tunnel_route_via: Optional[
        Union[
            OneOfTunnelRouteViaOptionsDef1,
            OneOfTunnelRouteViaOptionsDef2,
            OneOfTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    tunnel_source: Optional[Ipv4AddressAndMaskDef] = _field(
        default=None, metadata={"alias": "tunnelSource"}
    )
    tunnel_source_v6: Optional[Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2]] = (
        _field(default=None, metadata={"alias": "tunnelSourceV6"})
    )


@dataclass
class Payload:
    """
    WAN VPN Interface Ipsec profile parcel schema for POST request
    """

    data: Union[Data1, Data2, Data3, Data4, Data5, Data6]
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
    # WAN VPN Interface Ipsec profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanTransportWanVpnInterfaceIpsecPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateIpSecProfileParcel1PostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateIpSecProfileParcel1PostRequest:
    """
    WAN VPN Interface Ipsec profile parcel schema for POST request
    """

    data: Union[Data1, Data2, Data3, Data4, Data5, Data6]
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanTransportWanVpnInterfaceIpsecPayload:
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
    # WAN VPN Interface Ipsec profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditProfileParcel1PutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EditProfileParcel1PutRequest:
    """
    WAN VPN Interface Ipsec profile parcel schema for POST request
    """

    data: Union[Data1, Data2, Data3, Data4, Data5, Data6]
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
