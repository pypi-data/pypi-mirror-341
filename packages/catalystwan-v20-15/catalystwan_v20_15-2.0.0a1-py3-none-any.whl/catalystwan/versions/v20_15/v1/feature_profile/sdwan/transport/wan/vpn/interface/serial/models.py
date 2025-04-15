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

ClockRateDef = Literal[
    "1000000",
    "115200",
    "1200",
    "125000",
    "14400",
    "148000",
    "19200",
    "192000",
    "2000000",
    "2400",
    "250000",
    "256000",
    "28800",
    "32000",
    "38400",
    "384000",
    "4000000",
    "4800",
    "48000",
    "500000",
    "512000",
    "5300000",
    "56000",
    "57600",
    "64000",
    "72000",
    "768000",
    "800000",
    "8000000",
    "9600",
]

EncapsulationSerialDef = Literal["frame-relay", "hdlc", "ppp"]

ModeDef = Literal["spoke"]

ValueDef = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

DefaultValueDef = Literal["default"]

CarrierDef = Literal[
    "carrier1",
    "carrier2",
    "carrier3",
    "carrier4",
    "carrier5",
    "carrier6",
    "carrier7",
    "carrier8",
    "default",
]

DefaultCarrierDef = Literal["default"]

CoreRegionDef = Literal["core", "core-shared"]

DefaultCoreRegionDef = Literal["core-shared"]

SecondaryRegionDef = Literal["secondary-only", "secondary-shared"]

DefaultSecondaryRegionDef = Literal["secondary-shared"]

EncapsulationEncapDef = Literal["gre", "ipsec"]


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
class OneOfBandwidthOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfBandwidthOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBandwidthOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfClockRateOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ClockRateDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfClockRateOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfClockRateOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEncapsulationSerialOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EncapsulationSerialDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEncapsulationSerialOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEncapsulationSerialOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfBandwidthDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfBandwidthDownstreamOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBandwidthDownstreamOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class TunnelInterface:
    option_type: Optional[Any] = _field(default=None, metadata={"alias": "optionType"})
    value: Optional[Any] = _field(default=None)


@dataclass
class OneOfPerTunnelQosOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPerTunnelQosOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPerTunnelQosOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnOffDefaultFalseWithVariable1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnOffDefaultFalseWithVariable2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOnOffDefaultFalseWithVariable3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfModeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ValueDef


@dataclass
class OneOfValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfValueOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultValueDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRestrictOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfRestrictOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRestrictOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfGroupOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfGroupOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfBorderOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfBorderOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBorderOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfMaxControlConnectionsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMaxControlConnectionsOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMaxControlConnectionsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVbondAsStunServerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfVbondAsStunServerOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVbondAsStunServerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfExcludeControllerGroupListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class OneOfExcludeControllerGroupListOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfExcludeControllerGroupListOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVmanageConnectionPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVmanageConnectionPreferenceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVmanageConnectionPreferenceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPortHopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPortHopOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPortHopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfLowBandwidthLinkOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfLowBandwidthLinkOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLowBandwidthLinkOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTunnelTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTunnelTcpMssAdjustOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTunnelTcpMssAdjustOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTunnelClearDontFragmentOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTunnelClearDontFragmentOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTunnelClearDontFragmentOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNetworkBroadcastOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNetworkBroadcastOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNetworkBroadcastOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfCarrierOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CarrierDef


@dataclass
class OneOfCarrierOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfCarrierOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultCarrierDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfBindOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfBindOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBindOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLastResortCircuitOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfLastResortCircuitOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLastResortCircuitOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNatRefreshIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNatRefreshIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatRefreshIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHelloIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHelloIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHelloIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHelloToleranceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHelloToleranceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHelloToleranceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Tunnel:
    """
    Tunnel Interface Attributes
    """

    bind: Optional[Union[OneOfBindOptionsDef1, OneOfBindOptionsDef2, OneOfBindOptionsDef3]] = (
        _field(default=None)
    )
    border: Optional[
        Union[OneOfBorderOptionsDef1, OneOfBorderOptionsDef2, OneOfBorderOptionsDef3]
    ] = _field(default=None)
    carrier: Optional[
        Union[OneOfCarrierOptionsDef1, OneOfCarrierOptionsDef2, OneOfCarrierOptionsDef3]
    ] = _field(default=None)
    clear_dont_fragment: Optional[
        Union[
            OneOfTunnelClearDontFragmentOptionsDef1,
            OneOfTunnelClearDontFragmentOptionsDef2,
            OneOfTunnelClearDontFragmentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "clearDontFragment"})
    color: Optional[Union[OneOfValueOptionsDef1, OneOfValueOptionsDef2, OneOfValueOptionsDef3]] = (
        _field(default=None)
    )
    exclude_controller_group_list: Optional[
        Union[
            OneOfExcludeControllerGroupListOptionsDef1,
            OneOfExcludeControllerGroupListOptionsDef2,
            OneOfExcludeControllerGroupListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "excludeControllerGroupList"})
    group: Optional[Union[OneOfGroupOptionsDef1, OneOfGroupOptionsDef2, OneOfGroupOptionsDef3]] = (
        _field(default=None)
    )
    hello_interval: Optional[
        Union[
            OneOfHelloIntervalOptionsDef1,
            OneOfHelloIntervalOptionsDef2,
            OneOfHelloIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "helloInterval"})
    hello_tolerance: Optional[
        Union[
            OneOfHelloToleranceOptionsDef1,
            OneOfHelloToleranceOptionsDef2,
            OneOfHelloToleranceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "helloTolerance"})
    last_resort_circuit: Optional[
        Union[
            OneOfLastResortCircuitOptionsDef1,
            OneOfLastResortCircuitOptionsDef2,
            OneOfLastResortCircuitOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lastResortCircuit"})
    low_bandwidth_link: Optional[
        Union[
            OneOfLowBandwidthLinkOptionsDef1,
            OneOfLowBandwidthLinkOptionsDef2,
            OneOfLowBandwidthLinkOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lowBandwidthLink"})
    max_control_connections: Optional[
        Union[
            OneOfMaxControlConnectionsOptionsDef1,
            OneOfMaxControlConnectionsOptionsDef2,
            OneOfMaxControlConnectionsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxControlConnections"})
    mode: Optional[Union[OneOfModeOptionsDef1, OneOfModeOptionsDef2]] = _field(default=None)
    nat_refresh_interval: Optional[
        Union[
            OneOfNatRefreshIntervalOptionsDef1,
            OneOfNatRefreshIntervalOptionsDef2,
            OneOfNatRefreshIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "natRefreshInterval"})
    network_broadcast: Optional[
        Union[
            OneOfNetworkBroadcastOptionsDef1,
            OneOfNetworkBroadcastOptionsDef2,
            OneOfNetworkBroadcastOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "networkBroadcast"})
    per_tunnel_qos: Optional[
        Union[
            OneOfPerTunnelQosOptionsDef1, OneOfPerTunnelQosOptionsDef2, OneOfPerTunnelQosOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "perTunnelQos"})
    per_tunnel_qos_aggregator: Optional[
        Union[
            OneOfOnOffDefaultFalseWithVariable1,
            OneOfOnOffDefaultFalseWithVariable2,
            OneOfOnOffDefaultFalseWithVariable3,
        ]
    ] = _field(default=None, metadata={"alias": "perTunnelQosAggregator"})
    port_hop: Optional[
        Union[OneOfPortHopOptionsDef1, OneOfPortHopOptionsDef2, OneOfPortHopOptionsDef3]
    ] = _field(default=None, metadata={"alias": "portHop"})
    restrict: Optional[
        Union[OneOfRestrictOptionsDef1, OneOfRestrictOptionsDef2, OneOfRestrictOptionsDef3]
    ] = _field(default=None)
    tunnel_tcp_mss_adjust: Optional[
        Union[
            OneOfTunnelTcpMssAdjustOptionsDef1,
            OneOfTunnelTcpMssAdjustOptionsDef2,
            OneOfTunnelTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelTcpMssAdjust"})
    vbond_as_stun_server: Optional[
        Union[
            OneOfVbondAsStunServerOptionsDef1,
            OneOfVbondAsStunServerOptionsDef2,
            OneOfVbondAsStunServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "vbondAsStunServer"})
    vmanage_connection_preference: Optional[
        Union[
            OneOfVmanageConnectionPreferenceOptionsDef1,
            OneOfVmanageConnectionPreferenceOptionsDef2,
            OneOfVmanageConnectionPreferenceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "vmanageConnectionPreference"})


@dataclass
class OneOfAllOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfBgpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfBgpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBgpOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDhcpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDhcpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDhcpOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDnsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDnsOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDnsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIcmpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIcmpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIcmpOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNetconfOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNetconfOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNetconfOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNtpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNtpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNtpOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOspfOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOspfOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOspfOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfSshdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfSshdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSshdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfStunOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfStunOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStunOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfHttpsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfHttpsOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHttpsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfSnmpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfSnmpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSnmpOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfBfdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfBfdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBfdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class AllowService:
    """
    Tunnel Interface Attributes
    """

    all: Optional[Union[OneOfAllOptionsDef1, OneOfAllOptionsDef2, OneOfAllOptionsDef3]] = _field(
        default=None
    )
    bfd: Optional[Union[OneOfBfdOptionsDef1, OneOfBfdOptionsDef2, OneOfBfdOptionsDef3]] = _field(
        default=None
    )
    bgp: Optional[Union[OneOfBgpOptionsDef1, OneOfBgpOptionsDef2, OneOfBgpOptionsDef3]] = _field(
        default=None
    )
    dhcp: Optional[Union[OneOfDhcpOptionsDef1, OneOfDhcpOptionsDef2, OneOfDhcpOptionsDef3]] = (
        _field(default=None)
    )
    dns: Optional[Union[OneOfDnsOptionsDef1, OneOfDnsOptionsDef2, OneOfDnsOptionsDef3]] = _field(
        default=None
    )
    https: Optional[Union[OneOfHttpsOptionsDef1, OneOfHttpsOptionsDef2, OneOfHttpsOptionsDef3]] = (
        _field(default=None)
    )
    icmp: Optional[Union[OneOfIcmpOptionsDef1, OneOfIcmpOptionsDef2, OneOfIcmpOptionsDef3]] = (
        _field(default=None)
    )
    netconf: Optional[
        Union[OneOfNetconfOptionsDef1, OneOfNetconfOptionsDef2, OneOfNetconfOptionsDef3]
    ] = _field(default=None)
    ntp: Optional[Union[OneOfNtpOptionsDef1, OneOfNtpOptionsDef2, OneOfNtpOptionsDef3]] = _field(
        default=None
    )
    ospf: Optional[Union[OneOfOspfOptionsDef1, OneOfOspfOptionsDef2, OneOfOspfOptionsDef3]] = (
        _field(default=None)
    )
    snmp: Optional[Union[OneOfSnmpOptionsDef1, OneOfSnmpOptionsDef2, OneOfSnmpOptionsDef3]] = (
        _field(default=None)
    )
    sshd: Optional[Union[OneOfSshdOptionsDef1, OneOfSshdOptionsDef2, OneOfSshdOptionsDef3]] = (
        _field(default=None)
    )
    stun: Optional[Union[OneOfStunOptionsDef1, OneOfStunOptionsDef2, OneOfStunOptionsDef3]] = (
        _field(default=None)
    )


@dataclass
class OneOfEnableRegionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfEnableRegionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfCoreRegionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CoreRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfCoreRegionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultCoreRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSecondaryRegionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SecondaryRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSecondaryRegionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultSecondaryRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class MultiRegionFabric:
    """
    Multi-Region Fabric
    """

    core_region: Optional[Union[OneOfCoreRegionDef1, OneOfCoreRegionDef2]] = _field(
        default=None, metadata={"alias": "coreRegion"}
    )
    enable_core_region: Optional[Union[OneOfEnableRegionDef1, OneOfEnableRegionDef2]] = _field(
        default=None, metadata={"alias": "enableCoreRegion"}
    )
    enable_secondary_region: Optional[Union[OneOfEnableRegionDef1, OneOfEnableRegionDef2]] = _field(
        default=None, metadata={"alias": "enableSecondaryRegion"}
    )
    secondary_region: Optional[Union[OneOfSecondaryRegionDef1, OneOfSecondaryRegionDef2]] = _field(
        default=None, metadata={"alias": "secondaryRegion"}
    )


@dataclass
class OneOfShapingRateOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfShapingRateOptionsDef3:
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
class ParcelReferenceDef:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class AclQos:
    """
    ACL part
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
    shaping_rate: Optional[
        Union[OneOfShapingRateOptionsDef1, OneOfShapingRateOptionsDef2, OneOfShapingRateOptionsDef3]
    ] = _field(default=None, metadata={"alias": "shapingRate"})


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
class OneOfIpMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpMtuOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTlocExtensionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTlocExtensionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTlocExtensionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Advanced:
    """
    advanced part
    """

    ip_mtu: Optional[Union[OneOfIpMtuOptionsDef1, OneOfIpMtuOptionsDef2, OneOfIpMtuOptionsDef3]] = (
        _field(default=None, metadata={"alias": "ipMtu"})
    )
    mtu: Optional[Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3]] = _field(
        default=None
    )
    tcp_mss_adjust: Optional[
        Union[
            OneOfTcpMssAdjustOptionsDef1, OneOfTcpMssAdjustOptionsDef2, OneOfTcpMssAdjustOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})
    tloc_extension: Optional[
        Union[
            OneOfTlocExtensionOptionsDef1,
            OneOfTlocExtensionOptionsDef2,
            OneOfTlocExtensionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tlocExtension"})


@dataclass
class Data1:
    interface_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    # ACL part
    acl_qos: Optional[AclQos] = _field(default=None, metadata={"alias": "aclQos"})
    address_v4: Optional[Ipv4AddressAndMaskWithDefault] = _field(
        default=None, metadata={"alias": "addressV4"}
    )
    address_v6: Optional[
        Union[
            OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef1,
            OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef2,
            OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "addressV6"})
    # advanced part
    advanced: Optional[Advanced] = _field(default=None)
    # Tunnel Interface Attributes
    allow_service: Optional[AllowService] = _field(default=None, metadata={"alias": "allowService"})
    bandwidth: Optional[
        Union[OneOfBandwidthOptionsDef1, OneOfBandwidthOptionsDef2, OneOfBandwidthOptionsDef3]
    ] = _field(default=None)
    bandwidth_downstream: Optional[
        Union[
            OneOfBandwidthDownstreamOptionsDef1,
            OneOfBandwidthDownstreamOptionsDef2,
            OneOfBandwidthDownstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthDownstream"})
    clock_rate: Optional[
        Union[OneOfClockRateOptionsDef1, OneOfClockRateOptionsDef2, OneOfClockRateOptionsDef3]
    ] = _field(default=None, metadata={"alias": "clockRate"})
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)
    encapsulation: Optional[Any] = _field(default=None)
    encapsulation_serial: Optional[
        Union[
            OneOfEncapsulationSerialOptionsDef1,
            OneOfEncapsulationSerialOptionsDef2,
            OneOfEncapsulationSerialOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "encapsulationSerial"})
    # Multi-Region Fabric
    multi_region_fabric: Optional[MultiRegionFabric] = _field(
        default=None, metadata={"alias": "multiRegionFabric"}
    )
    shutdown: Optional[
        Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    ] = _field(default=None)
    # Tunnel Interface Attributes
    tunnel: Optional[Tunnel] = _field(default=None)
    tunnel_interface: Optional[TunnelInterface] = _field(
        default=None, metadata={"alias": "tunnelInterface"}
    )


@dataclass
class OneOfTunnelInterfaceDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTunnelInterfaceDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfEncapsulationEncapOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EncapsulationEncapDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEncapsulationPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEncapsulationPreferenceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEncapsulationPreferenceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEncapsulationWeightOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEncapsulationWeightOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEncapsulationWeightOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Encapsulation:
    encap: OneOfEncapsulationEncapOptionsDef
    preference: Optional[
        Union[
            OneOfEncapsulationPreferenceOptionsDef1,
            OneOfEncapsulationPreferenceOptionsDef2,
            OneOfEncapsulationPreferenceOptionsDef3,
        ]
    ] = _field(default=None)
    weight: Optional[
        Union[
            OneOfEncapsulationWeightOptionsDef1,
            OneOfEncapsulationWeightOptionsDef2,
            OneOfEncapsulationWeightOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class Data2:
    interface_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    # ACL part
    acl_qos: Optional[AclQos] = _field(default=None, metadata={"alias": "aclQos"})
    address_v4: Optional[Ipv4AddressAndMaskWithDefault] = _field(
        default=None, metadata={"alias": "addressV4"}
    )
    address_v6: Optional[
        Union[
            OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef1,
            OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef2,
            OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "addressV6"})
    # advanced part
    advanced: Optional[Advanced] = _field(default=None)
    # Tunnel Interface Attributes
    allow_service: Optional[AllowService] = _field(default=None, metadata={"alias": "allowService"})
    bandwidth: Optional[
        Union[OneOfBandwidthOptionsDef1, OneOfBandwidthOptionsDef2, OneOfBandwidthOptionsDef3]
    ] = _field(default=None)
    bandwidth_downstream: Optional[
        Union[
            OneOfBandwidthDownstreamOptionsDef1,
            OneOfBandwidthDownstreamOptionsDef2,
            OneOfBandwidthDownstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthDownstream"})
    clock_rate: Optional[
        Union[OneOfClockRateOptionsDef1, OneOfClockRateOptionsDef2, OneOfClockRateOptionsDef3]
    ] = _field(default=None, metadata={"alias": "clockRate"})
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)
    # Encapsulation for TLOC
    encapsulation: Optional[List[Encapsulation]] = _field(default=None)
    encapsulation_serial: Optional[
        Union[
            OneOfEncapsulationSerialOptionsDef1,
            OneOfEncapsulationSerialOptionsDef2,
            OneOfEncapsulationSerialOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "encapsulationSerial"})
    # Multi-Region Fabric
    multi_region_fabric: Optional[MultiRegionFabric] = _field(
        default=None, metadata={"alias": "multiRegionFabric"}
    )
    shutdown: Optional[
        Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    ] = _field(default=None)
    # Tunnel Interface Attributes
    tunnel: Optional[Tunnel] = _field(default=None)
    tunnel_interface: Optional[Union[OneOfTunnelInterfaceDef1, OneOfTunnelInterfaceDef2]] = _field(
        default=None, metadata={"alias": "tunnelInterface"}
    )


@dataclass
class Payload:
    """
    Serial profile parcel schema for POST request
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
    # Serial profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanTransportWanVpnInterfaceSerialPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateWanVpnInterfaceSerialParcelForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateWanVpnInterfaceSerialParcelForTransportPostRequest:
    """
    Serial profile parcel schema for POST request
    """

    data: Union[Data1, Data2]
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanTransportWanVpnInterfaceSerialPayload:
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
    # Serial profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditWanVpnInterfaceSerialParcelForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EditWanVpnInterfaceSerialParcelForTransportPutRequest:
    """
    Serial profile parcel schema for POST request
    """

    data: Union[Data1, Data2]
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
