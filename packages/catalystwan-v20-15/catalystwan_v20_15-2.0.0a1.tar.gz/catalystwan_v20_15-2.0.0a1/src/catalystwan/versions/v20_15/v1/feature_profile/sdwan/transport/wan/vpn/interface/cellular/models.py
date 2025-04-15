# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

ModeDef = Literal["spoke"]

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

ColorDef = Literal[
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

Value = Literal["mpls"]

EncapsulationEncapDef = Literal["gre", "ipsec"]

CoreRegionDef = Literal["core", "core-shared"]

DefaultCoreRegionDef = Literal["core-shared"]

SecondaryRegionDef = Literal["secondary-only", "secondary-shared"]

DefaultSecondaryRegionDef = Literal["secondary-shared"]

CellularModeDef = Literal["spoke"]

CellularCarrierDef = Literal[
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

CellularDefaultCarrierDef = Literal["default"]

CellularColorDef = Literal[
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

CellularEncapsulationEncapDef = Literal["gre", "ipsec"]

CellularCoreRegionDef = Literal["core", "core-shared"]

CellularDefaultCoreRegionDef = Literal["core-shared"]

CellularSecondaryRegionDef = Literal["secondary-only", "secondary-shared"]

CellularDefaultSecondaryRegionDef = Literal["secondary-shared"]

InterfaceCellularModeDef = Literal["spoke"]

InterfaceCellularCarrierDef = Literal[
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

InterfaceCellularDefaultCarrierDef = Literal["default"]

InterfaceCellularColorDef = Literal[
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

InterfaceCellularEncapsulationEncapDef = Literal["gre", "ipsec"]

InterfaceCellularCoreRegionDef = Literal["core", "core-shared"]

InterfaceCellularDefaultCoreRegionDef = Literal["core-shared"]

InterfaceCellularSecondaryRegionDef = Literal["secondary-only", "secondary-shared"]

InterfaceCellularDefaultSecondaryRegionDef = Literal["secondary-shared"]


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
class OneOfenableIpV6OptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfenableIpV6OptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfenableIpV6OptionsDef3:
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
    value: List[str]


@dataclass
class OneOfListOfIpV4OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfServiceProviderOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfServiceProviderOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfServiceProviderOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfBandwidthUpstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfBandwidthUpstreamOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBandwidthUpstreamOptionsDef3:
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
class OneOfTunnelInterfaceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTunnelInterfaceOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


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
class OneOfColorOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfColorOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfColorOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


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
class OneOfControllerGroupListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class OneOfControllerGroupListOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfControllerGroupListOptionsDef3:
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
            OneOfClearDontFragmentOptionsDef1,
            OneOfClearDontFragmentOptionsDef2,
            OneOfClearDontFragmentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "clearDontFragment"})
    color: Optional[Union[OneOfColorOptionsDef1, OneOfColorOptionsDef2, OneOfColorOptionsDef3]] = (
        _field(default=None)
    )
    exclude_controller_group_list: Optional[
        Union[
            OneOfControllerGroupListOptionsDef1,
            OneOfControllerGroupListOptionsDef2,
            OneOfControllerGroupListOptionsDef3,
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
    port_hop: Optional[
        Union[OneOfPortHopOptionsDef1, OneOfPortHopOptionsDef2, OneOfPortHopOptionsDef3]
    ] = _field(default=None, metadata={"alias": "portHop"})
    restrict: Optional[
        Union[OneOfRestrictOptionsDef1, OneOfRestrictOptionsDef2, OneOfRestrictOptionsDef3]
    ] = _field(default=None)
    tunnel_tcp_mss: Optional[
        Union[
            OneOfTunnelTcpMssAdjustOptionsDef1,
            OneOfTunnelTcpMssAdjustOptionsDef2,
            OneOfTunnelTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelTcpMss"})
    v_bond_as_stun_server: Optional[
        Union[
            OneOfVbondAsStunServerOptionsDef1,
            OneOfVbondAsStunServerOptionsDef2,
            OneOfVbondAsStunServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "vBondAsStunServer"})
    v_manage_connection_preference: Optional[
        Union[
            OneOfVmanageConnectionPreferenceOptionsDef1,
            OneOfVmanageConnectionPreferenceOptionsDef2,
            OneOfVmanageConnectionPreferenceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "vManageConnectionPreference"})


@dataclass
class OneOfAllowAllOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowAllOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowAllOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowBgpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowBgpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowBgpOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowDhcpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowDhcpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowDhcpOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowNtpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowNtpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowNtpOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowSshOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowSshOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowSshOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowServiceTrueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowServiceTrueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowServiceTrueOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowServiceFalseOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowServiceFalseOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowServiceFalseOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class AllowService:
    """
    Tunnel Interface Attributes
    """

    all: Optional[
        Union[OneOfAllowAllOptionsDef1, OneOfAllowAllOptionsDef2, OneOfAllowAllOptionsDef3]
    ] = _field(default=None)
    bfd: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    bgp: Optional[
        Union[OneOfAllowBgpOptionsDef1, OneOfAllowBgpOptionsDef2, OneOfAllowBgpOptionsDef3]
    ] = _field(default=None)
    dhcp: Optional[
        Union[OneOfAllowDhcpOptionsDef1, OneOfAllowDhcpOptionsDef2, OneOfAllowDhcpOptionsDef3]
    ] = _field(default=None)
    dns: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    https: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    icmp: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    netconf: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    ntp: Optional[
        Union[OneOfAllowNtpOptionsDef1, OneOfAllowNtpOptionsDef2, OneOfAllowNtpOptionsDef3]
    ] = _field(default=None)
    ospf: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    snmp: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    ssh: Optional[
        Union[OneOfAllowSshOptionsDef1, OneOfAllowSshOptionsDef2, OneOfAllowSshOptionsDef3]
    ] = _field(default=None)
    stun: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)


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
class OneOfNatOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNatOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfUdpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfUdpTimeoutOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUdpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTcpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTcpTimeoutOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTcpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NatAttributesIpv4:
    """
    NAT Attributes
    """

    tcp_timeout: Union[
        OneOfTcpTimeoutOptionsDef1, OneOfTcpTimeoutOptionsDef2, OneOfTcpTimeoutOptionsDef3
    ] = _field(metadata={"alias": "tcpTimeout"})
    udp_timeout: Union[
        OneOfUdpTimeoutOptionsDef1, OneOfUdpTimeoutOptionsDef2, OneOfUdpTimeoutOptionsDef3
    ] = _field(metadata={"alias": "udpTimeout"})


@dataclass
class OneOfQosAdaptiveOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfQosAdaptiveOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPeriodOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPeriodOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPeriodOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ShapingRateUpstream:
    value: Optional[Any] = _field(default=None)


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class ShapingRateUpstreamConfig:
    """
    adaptiveQoS Shaping Rate Upstream config
    """

    default_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef1, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateUpstream"})
    max_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef1, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "maxShapingRateUpstream"})
    min_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef1, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateUpstream"})


@dataclass
class OneOfShapingRateDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfShapingRateDownstreamOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class ShapingRateDownstreamConfig:
    """
    adaptiveQoS Shaping Rate Downstream config
    """

    default_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef1, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateDownstream"})
    max_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef1, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "maxShapingRateDownstream"})
    min_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef1, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateDownstream"})


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
class AclQos1:
    adaptive_qo_s: Union[OneOfQosAdaptiveOptionsDef1, OneOfQosAdaptiveOptionsDef2] = _field(
        metadata={"alias": "adaptiveQoS"}
    )
    shaping_rate_upstream: ShapingRateUpstream = _field(metadata={"alias": "shapingRateUpstream"})
    # adaptiveQoS Shaping Rate Upstream config
    shaping_rate_upstream_config: ShapingRateUpstreamConfig = _field(
        metadata={"alias": "shapingRateUpstreamConfig"}
    )
    adapt_period: Optional[
        Union[OneOfPeriodOptionsDef1, OneOfPeriodOptionsDef2, OneOfPeriodOptionsDef3]
    ] = _field(default=None, metadata={"alias": "adaptPeriod"})
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
    shaping_rate_downstream: Optional[
        Union[OneOfShapingRateDownstreamOptionsDef1, OneOfShapingRateDownstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateDownstream"})
    # adaptiveQoS Shaping Rate Downstream config
    shaping_rate_downstream_config: Optional[ShapingRateDownstreamConfig] = _field(
        default=None, metadata={"alias": "shapingRateDownstreamConfig"}
    )


@dataclass
class OneOfShapingRateUpstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfShapingRateUpstreamOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class AclQos2:
    adaptive_qo_s: Union[OneOfQosAdaptiveOptionsDef1, OneOfQosAdaptiveOptionsDef2] = _field(
        metadata={"alias": "adaptiveQoS"}
    )
    adapt_period: Optional[
        Union[OneOfPeriodOptionsDef1, OneOfPeriodOptionsDef2, OneOfPeriodOptionsDef3]
    ] = _field(default=None, metadata={"alias": "adaptPeriod"})
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
    shaping_rate_downstream: Optional[
        Union[OneOfShapingRateDownstreamOptionsDef1, OneOfShapingRateDownstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateDownstream"})
    # adaptiveQoS Shaping Rate Downstream config
    shaping_rate_downstream_config: Optional[ShapingRateDownstreamConfig] = _field(
        default=None, metadata={"alias": "shapingRateDownstreamConfig"}
    )
    shaping_rate_upstream: Optional[
        Union[OneOfShapingRateUpstreamOptionsDef1, OneOfShapingRateUpstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateUpstream"})
    # adaptiveQoS Shaping Rate Upstream config
    shaping_rate_upstream_config: Optional[ShapingRateUpstreamConfig] = _field(
        default=None, metadata={"alias": "shapingRateUpstreamConfig"}
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
class OneOfIpV4AddressOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfMacAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


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
class Arp:
    ip_address: Union[
        OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2, OneOfIpV4AddressOptionsDef3
    ] = _field(metadata={"alias": "ipAddress"})
    mac_address: Union[
        OneOfMacAddressOptionsDef1, OneOfMacAddressOptionsDef2, OneOfMacAddressOptionsDef3
    ] = _field(metadata={"alias": "macAddress"})


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
    tcp_mss: Optional[
        Union[
            OneOfTcpMssAdjustOptionsDef1, OneOfTcpMssAdjustOptionsDef2, OneOfTcpMssAdjustOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "tcpMss"})
    tloc_extension: Optional[
        Union[
            OneOfTlocExtensionOptionsDef1,
            OneOfTlocExtensionOptionsDef2,
            OneOfTlocExtensionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tlocExtension"})
    tracker: Optional[
        Union[OneOfTrackerOptionsDef1, OneOfTrackerOptionsDef2, OneOfTrackerOptionsDef3]
    ] = _field(default=None)


@dataclass
class CellularData:
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    # Encapsulation for TLOC
    encapsulation: List[Encapsulation]
    interface_name: Union[OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    nat: Union[OneOfNatOptionsDef1, OneOfNatOptionsDef2, OneOfNatOptionsDef3]
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tunnel_interface: Union[OneOfTunnelInterfaceOptionsDef1, OneOfTunnelInterfaceOptionsDef2] = (
        _field(metadata={"alias": "tunnelInterface"})
    )
    # ACL/QOS
    acl_qos: Optional[Union[AclQos1, AclQos2]] = _field(default=None, metadata={"alias": "aclQos"})
    # Advanced Attributes
    advanced: Optional[Advanced] = _field(default=None)
    # Tunnel Interface Attributes
    allow_service: Optional[AllowService] = _field(default=None, metadata={"alias": "allowService"})
    # Configure ARP entries
    arp: Optional[List[Arp]] = _field(default=None)
    bandwidth_downstream: Optional[
        Union[
            OneOfBandwidthDownstreamOptionsDef1,
            OneOfBandwidthDownstreamOptionsDef2,
            OneOfBandwidthDownstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthDownstream"})
    bandwidth_upstream: Optional[
        Union[
            OneOfBandwidthUpstreamOptionsDef1,
            OneOfBandwidthUpstreamOptionsDef2,
            OneOfBandwidthUpstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthUpstream"})
    dhcp_helper: Optional[
        Union[OneOfListOfIpV4OptionsDef1, OneOfListOfIpV4OptionsDef2, OneOfListOfIpV4OptionsDef3]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    enable_ipv6: Optional[
        Union[OneOfenableIpV6OptionsDef1, OneOfenableIpV6OptionsDef2, OneOfenableIpV6OptionsDef3]
    ] = _field(default=None, metadata={"alias": "enableIpv6"})
    # Multi-Region Fabric
    multi_region_fabric: Optional[MultiRegionFabric] = _field(
        default=None, metadata={"alias": "multiRegionFabric"}
    )
    # NAT Attributes
    nat_attributes_ipv4: Optional[NatAttributesIpv4] = _field(
        default=None, metadata={"alias": "natAttributesIpv4"}
    )
    service_provider: Optional[
        Union[
            OneOfServiceProviderOptionsDef1,
            OneOfServiceProviderOptionsDef2,
            OneOfServiceProviderOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "serviceProvider"})
    # Tunnel Interface Attributes
    tunnel: Optional[Tunnel] = _field(default=None)


@dataclass
class Payload:
    """
    WAN VPN Interface Cellular profile parcel schema for POST request
    """

    data: CellularData
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
    # WAN VPN Interface Cellular profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanTransportWanVpnInterfaceCellularPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateWanVpnInterfaceCellularParcelForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class InterfaceCellularData:
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    # Encapsulation for TLOC
    encapsulation: List[Encapsulation]
    interface_name: Union[OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    nat: Union[OneOfNatOptionsDef1, OneOfNatOptionsDef2, OneOfNatOptionsDef3]
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tunnel_interface: Union[OneOfTunnelInterfaceOptionsDef1, OneOfTunnelInterfaceOptionsDef2] = (
        _field(metadata={"alias": "tunnelInterface"})
    )
    # ACL/QOS
    acl_qos: Optional[Union[AclQos1, AclQos2]] = _field(default=None, metadata={"alias": "aclQos"})
    # Advanced Attributes
    advanced: Optional[Advanced] = _field(default=None)
    # Tunnel Interface Attributes
    allow_service: Optional[AllowService] = _field(default=None, metadata={"alias": "allowService"})
    # Configure ARP entries
    arp: Optional[List[Arp]] = _field(default=None)
    bandwidth_downstream: Optional[
        Union[
            OneOfBandwidthDownstreamOptionsDef1,
            OneOfBandwidthDownstreamOptionsDef2,
            OneOfBandwidthDownstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthDownstream"})
    bandwidth_upstream: Optional[
        Union[
            OneOfBandwidthUpstreamOptionsDef1,
            OneOfBandwidthUpstreamOptionsDef2,
            OneOfBandwidthUpstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthUpstream"})
    dhcp_helper: Optional[
        Union[OneOfListOfIpV4OptionsDef1, OneOfListOfIpV4OptionsDef2, OneOfListOfIpV4OptionsDef3]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    enable_ipv6: Optional[
        Union[OneOfenableIpV6OptionsDef1, OneOfenableIpV6OptionsDef2, OneOfenableIpV6OptionsDef3]
    ] = _field(default=None, metadata={"alias": "enableIpv6"})
    # Multi-Region Fabric
    multi_region_fabric: Optional[MultiRegionFabric] = _field(
        default=None, metadata={"alias": "multiRegionFabric"}
    )
    # NAT Attributes
    nat_attributes_ipv4: Optional[NatAttributesIpv4] = _field(
        default=None, metadata={"alias": "natAttributesIpv4"}
    )
    service_provider: Optional[
        Union[
            OneOfServiceProviderOptionsDef1,
            OneOfServiceProviderOptionsDef2,
            OneOfServiceProviderOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "serviceProvider"})
    # Tunnel Interface Attributes
    tunnel: Optional[Tunnel] = _field(default=None)


@dataclass
class CreateWanVpnInterfaceCellularParcelForTransportPostRequest:
    """
    WAN VPN Interface Cellular profile parcel schema for POST request
    """

    data: InterfaceCellularData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class CellularOneOfInterfaceNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CellularOneOfDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CellularOneOfListOfIpV4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class CellularOneOfBandwidthUpstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfBandwidthDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CellularModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class CellularOneOfBindOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CellularOneOfCarrierOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CellularCarrierDef


@dataclass
class CellularOneOfCarrierOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CellularDefaultCarrierDef  # pytype: disable=annotation-type-mismatch


@dataclass
class CellularOneOfColorOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CellularColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class CellularOneOfHelloIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfHelloIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfHelloToleranceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfHelloToleranceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfMaxControlConnectionsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfNatRefreshIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfNatRefreshIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfControllerGroupListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class CellularOneOfVmanageConnectionPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfVmanageConnectionPreferenceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfTunnelTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularTunnel:
    """
    Tunnel Interface Attributes
    """

    bind: Optional[
        Union[CellularOneOfBindOptionsDef1, OneOfBindOptionsDef2, OneOfBindOptionsDef3]
    ] = _field(default=None)
    border: Optional[
        Union[OneOfBorderOptionsDef1, OneOfBorderOptionsDef2, OneOfBorderOptionsDef3]
    ] = _field(default=None)
    carrier: Optional[
        Union[
            CellularOneOfCarrierOptionsDef1,
            OneOfCarrierOptionsDef2,
            CellularOneOfCarrierOptionsDef3,
        ]
    ] = _field(default=None)
    clear_dont_fragment: Optional[
        Union[
            OneOfClearDontFragmentOptionsDef1,
            OneOfClearDontFragmentOptionsDef2,
            OneOfClearDontFragmentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "clearDontFragment"})
    color: Optional[
        Union[CellularOneOfColorOptionsDef1, OneOfColorOptionsDef2, OneOfColorOptionsDef3]
    ] = _field(default=None)
    exclude_controller_group_list: Optional[
        Union[
            CellularOneOfControllerGroupListOptionsDef1,
            OneOfControllerGroupListOptionsDef2,
            OneOfControllerGroupListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "excludeControllerGroupList"})
    group: Optional[
        Union[CellularOneOfGroupOptionsDef1, OneOfGroupOptionsDef2, OneOfGroupOptionsDef3]
    ] = _field(default=None)
    hello_interval: Optional[
        Union[
            CellularOneOfHelloIntervalOptionsDef1,
            OneOfHelloIntervalOptionsDef2,
            CellularOneOfHelloIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "helloInterval"})
    hello_tolerance: Optional[
        Union[
            CellularOneOfHelloToleranceOptionsDef1,
            OneOfHelloToleranceOptionsDef2,
            CellularOneOfHelloToleranceOptionsDef3,
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
            CellularOneOfMaxControlConnectionsOptionsDef1,
            OneOfMaxControlConnectionsOptionsDef2,
            OneOfMaxControlConnectionsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxControlConnections"})
    mode: Optional[Union[CellularOneOfModeOptionsDef1, OneOfModeOptionsDef2]] = _field(default=None)
    nat_refresh_interval: Optional[
        Union[
            CellularOneOfNatRefreshIntervalOptionsDef1,
            OneOfNatRefreshIntervalOptionsDef2,
            CellularOneOfNatRefreshIntervalOptionsDef3,
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
    port_hop: Optional[
        Union[OneOfPortHopOptionsDef1, OneOfPortHopOptionsDef2, OneOfPortHopOptionsDef3]
    ] = _field(default=None, metadata={"alias": "portHop"})
    restrict: Optional[
        Union[OneOfRestrictOptionsDef1, OneOfRestrictOptionsDef2, OneOfRestrictOptionsDef3]
    ] = _field(default=None)
    tunnel_tcp_mss: Optional[
        Union[
            CellularOneOfTunnelTcpMssAdjustOptionsDef1,
            OneOfTunnelTcpMssAdjustOptionsDef2,
            OneOfTunnelTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelTcpMss"})
    v_bond_as_stun_server: Optional[
        Union[
            OneOfVbondAsStunServerOptionsDef1,
            OneOfVbondAsStunServerOptionsDef2,
            OneOfVbondAsStunServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "vBondAsStunServer"})
    v_manage_connection_preference: Optional[
        Union[
            CellularOneOfVmanageConnectionPreferenceOptionsDef1,
            OneOfVmanageConnectionPreferenceOptionsDef2,
            CellularOneOfVmanageConnectionPreferenceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "vManageConnectionPreference"})


@dataclass
class CellularAllowService:
    """
    Tunnel Interface Attributes
    """

    all: Optional[
        Union[OneOfAllowAllOptionsDef1, OneOfAllowAllOptionsDef2, OneOfAllowAllOptionsDef3]
    ] = _field(default=None)
    bfd: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    bgp: Optional[
        Union[OneOfAllowBgpOptionsDef1, OneOfAllowBgpOptionsDef2, OneOfAllowBgpOptionsDef3]
    ] = _field(default=None)
    dhcp: Optional[
        Union[OneOfAllowDhcpOptionsDef1, OneOfAllowDhcpOptionsDef2, OneOfAllowDhcpOptionsDef3]
    ] = _field(default=None)
    dns: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    https: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    icmp: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    netconf: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    ntp: Optional[
        Union[OneOfAllowNtpOptionsDef1, OneOfAllowNtpOptionsDef2, OneOfAllowNtpOptionsDef3]
    ] = _field(default=None)
    ospf: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    snmp: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    ssh: Optional[
        Union[OneOfAllowSshOptionsDef1, OneOfAllowSshOptionsDef2, OneOfAllowSshOptionsDef3]
    ] = _field(default=None)
    stun: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class CellularOneOfEncapsulationEncapOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CellularEncapsulationEncapDef  # pytype: disable=annotation-type-mismatch


@dataclass
class CellularOneOfEncapsulationPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfEncapsulationWeightOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfEncapsulationWeightOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularEncapsulation:
    encap: CellularOneOfEncapsulationEncapOptionsDef
    preference: Optional[
        Union[
            CellularOneOfEncapsulationPreferenceOptionsDef1,
            OneOfEncapsulationPreferenceOptionsDef2,
            OneOfEncapsulationPreferenceOptionsDef3,
        ]
    ] = _field(default=None)
    weight: Optional[
        Union[
            CellularOneOfEncapsulationWeightOptionsDef1,
            OneOfEncapsulationWeightOptionsDef2,
            CellularOneOfEncapsulationWeightOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class CellularOneOfCoreRegionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CellularCoreRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class CellularOneOfCoreRegionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CellularDefaultCoreRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class CellularOneOfSecondaryRegionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CellularSecondaryRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class CellularOneOfSecondaryRegionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CellularDefaultSecondaryRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class CellularMultiRegionFabric:
    """
    Multi-Region Fabric
    """

    core_region: Optional[Union[CellularOneOfCoreRegionDef1, CellularOneOfCoreRegionDef2]] = _field(
        default=None, metadata={"alias": "coreRegion"}
    )
    enable_core_region: Optional[Union[OneOfEnableRegionDef1, OneOfEnableRegionDef2]] = _field(
        default=None, metadata={"alias": "enableCoreRegion"}
    )
    enable_secondary_region: Optional[Union[OneOfEnableRegionDef1, OneOfEnableRegionDef2]] = _field(
        default=None, metadata={"alias": "enableSecondaryRegion"}
    )
    secondary_region: Optional[
        Union[CellularOneOfSecondaryRegionDef1, CellularOneOfSecondaryRegionDef2]
    ] = _field(default=None, metadata={"alias": "secondaryRegion"})


@dataclass
class CellularOneOfUdpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfUdpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfTcpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfTcpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularNatAttributesIpv4:
    """
    NAT Attributes
    """

    tcp_timeout: Union[
        CellularOneOfTcpTimeoutOptionsDef1,
        OneOfTcpTimeoutOptionsDef2,
        CellularOneOfTcpTimeoutOptionsDef3,
    ] = _field(metadata={"alias": "tcpTimeout"})
    udp_timeout: Union[
        CellularOneOfUdpTimeoutOptionsDef1,
        OneOfUdpTimeoutOptionsDef2,
        CellularOneOfUdpTimeoutOptionsDef3,
    ] = _field(metadata={"alias": "udpTimeout"})


@dataclass
class CellularOneOfPeriodOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfPeriodOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceCellularOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularShapingRateUpstreamConfig:
    """
    adaptiveQoS Shaping Rate Upstream config
    """

    default_shaping_rate_upstream: Union[
        VpnInterfaceCellularOneOfShapingRateUpOrDownstreamOptionsDef1,
        OneOfShapingRateUpOrDownstreamOptionsDef2,
    ] = _field(metadata={"alias": "defaultShapingRateUpstream"})
    max_shaping_rate_upstream: Union[
        InterfaceCellularOneOfShapingRateUpOrDownstreamOptionsDef1,
        OneOfShapingRateUpOrDownstreamOptionsDef2,
    ] = _field(metadata={"alias": "maxShapingRateUpstream"})
    min_shaping_rate_upstream: Union[
        CellularOneOfShapingRateUpOrDownstreamOptionsDef1, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateUpstream"})


@dataclass
class WanVpnInterfaceCellularOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportWanVpnInterfaceCellularOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanTransportWanVpnInterfaceCellularOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularShapingRateDownstreamConfig:
    """
    adaptiveQoS Shaping Rate Downstream config
    """

    default_shaping_rate_downstream: Union[
        SdwanTransportWanVpnInterfaceCellularOneOfShapingRateUpOrDownstreamOptionsDef1,
        OneOfShapingRateUpOrDownstreamOptionsDef2,
    ] = _field(metadata={"alias": "defaultShapingRateDownstream"})
    max_shaping_rate_downstream: Union[
        TransportWanVpnInterfaceCellularOneOfShapingRateUpOrDownstreamOptionsDef1,
        OneOfShapingRateUpOrDownstreamOptionsDef2,
    ] = _field(metadata={"alias": "maxShapingRateDownstream"})
    min_shaping_rate_downstream: Union[
        WanVpnInterfaceCellularOneOfShapingRateUpOrDownstreamOptionsDef1,
        OneOfShapingRateUpOrDownstreamOptionsDef2,
    ] = _field(metadata={"alias": "minShapingRateDownstream"})


@dataclass
class CellularAclQos1:
    adaptive_qo_s: Union[OneOfQosAdaptiveOptionsDef1, OneOfQosAdaptiveOptionsDef2] = _field(
        metadata={"alias": "adaptiveQoS"}
    )
    shaping_rate_upstream: ShapingRateUpstream = _field(metadata={"alias": "shapingRateUpstream"})
    # adaptiveQoS Shaping Rate Upstream config
    shaping_rate_upstream_config: CellularShapingRateUpstreamConfig = _field(
        metadata={"alias": "shapingRateUpstreamConfig"}
    )
    adapt_period: Optional[
        Union[
            CellularOneOfPeriodOptionsDef1, OneOfPeriodOptionsDef2, CellularOneOfPeriodOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "adaptPeriod"})
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
    shaping_rate_downstream: Optional[
        Union[OneOfShapingRateDownstreamOptionsDef1, OneOfShapingRateDownstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateDownstream"})
    # adaptiveQoS Shaping Rate Downstream config
    shaping_rate_downstream_config: Optional[CellularShapingRateDownstreamConfig] = _field(
        default=None, metadata={"alias": "shapingRateDownstreamConfig"}
    )


@dataclass
class InterfaceCellularOneOfPeriodOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfPeriodOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdwanTransportWanVpnInterfaceCellularOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdwanTransportWanVpnInterfaceCellularOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularShapingRateUpstreamConfig:
    """
    adaptiveQoS Shaping Rate Upstream config
    """

    default_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef11, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateUpstream"})
    max_shaping_rate_upstream: Union[
        V1FeatureProfileSdwanTransportWanVpnInterfaceCellularOneOfShapingRateUpOrDownstreamOptionsDef1,
        OneOfShapingRateUpOrDownstreamOptionsDef2,
    ] = _field(metadata={"alias": "maxShapingRateUpstream"})
    min_shaping_rate_upstream: Union[
        FeatureProfileSdwanTransportWanVpnInterfaceCellularOneOfShapingRateUpOrDownstreamOptionsDef1,
        OneOfShapingRateUpOrDownstreamOptionsDef2,
    ] = _field(metadata={"alias": "minShapingRateUpstream"})


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef12:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef13:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef14:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularShapingRateDownstreamConfig:
    """
    adaptiveQoS Shaping Rate Downstream config
    """

    default_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef14, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateDownstream"})
    max_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef13, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "maxShapingRateDownstream"})
    min_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef12, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateDownstream"})


@dataclass
class CellularAclQos2:
    adaptive_qo_s: Union[OneOfQosAdaptiveOptionsDef1, OneOfQosAdaptiveOptionsDef2] = _field(
        metadata={"alias": "adaptiveQoS"}
    )
    adapt_period: Optional[
        Union[
            InterfaceCellularOneOfPeriodOptionsDef1,
            OneOfPeriodOptionsDef2,
            InterfaceCellularOneOfPeriodOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "adaptPeriod"})
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
    shaping_rate_downstream: Optional[
        Union[OneOfShapingRateDownstreamOptionsDef1, OneOfShapingRateDownstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateDownstream"})
    # adaptiveQoS Shaping Rate Downstream config
    shaping_rate_downstream_config: Optional[InterfaceCellularShapingRateDownstreamConfig] = _field(
        default=None, metadata={"alias": "shapingRateDownstreamConfig"}
    )
    shaping_rate_upstream: Optional[
        Union[OneOfShapingRateUpstreamOptionsDef1, OneOfShapingRateUpstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateUpstream"})
    # adaptiveQoS Shaping Rate Upstream config
    shaping_rate_upstream_config: Optional[InterfaceCellularShapingRateUpstreamConfig] = _field(
        default=None, metadata={"alias": "shapingRateUpstreamConfig"}
    )


@dataclass
class CellularOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CellularOneOfMacAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CellularArp:
    ip_address: Union[
        OneOfIpV4AddressOptionsDef1,
        CellularOneOfIpV4AddressOptionsDef2,
        OneOfIpV4AddressOptionsDef3,
    ] = _field(metadata={"alias": "ipAddress"})
    mac_address: Union[
        CellularOneOfMacAddressOptionsDef1, OneOfMacAddressOptionsDef2, OneOfMacAddressOptionsDef3
    ] = _field(metadata={"alias": "macAddress"})


@dataclass
class CellularOneOfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfIntrfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfIntrfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CellularOneOfTlocExtensionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CellularOneOfTrackerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CellularAdvanced:
    """
    Advanced Attributes
    """

    intrf_mtu: Optional[
        Union[
            CellularOneOfIntrfMtuOptionsDef1,
            OneOfIntrfMtuOptionsDef2,
            CellularOneOfIntrfMtuOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "intrfMtu"})
    ip_directed_broadcast: Optional[
        Union[
            OneOfIpDirectedBroadcastOptionsDef1,
            OneOfIpDirectedBroadcastOptionsDef2,
            OneOfIpDirectedBroadcastOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipDirectedBroadcast"})
    ip_mtu: Optional[
        Union[CellularOneOfMtuOptionsDef1, OneOfMtuOptionsDef2, CellularOneOfMtuOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ipMtu"})
    tcp_mss: Optional[
        Union[
            CellularOneOfTcpMssAdjustOptionsDef1,
            OneOfTcpMssAdjustOptionsDef2,
            OneOfTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMss"})
    tloc_extension: Optional[
        Union[
            CellularOneOfTlocExtensionOptionsDef1,
            OneOfTlocExtensionOptionsDef2,
            OneOfTlocExtensionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tlocExtension"})
    tracker: Optional[
        Union[CellularOneOfTrackerOptionsDef1, OneOfTrackerOptionsDef2, OneOfTrackerOptionsDef3]
    ] = _field(default=None)


@dataclass
class VpnInterfaceCellularData:
    description: Union[
        CellularOneOfDescriptionOptionsDef1,
        OneOfDescriptionOptionsDef2,
        OneOfDescriptionOptionsDef3,
    ]
    # Encapsulation for TLOC
    encapsulation: List[CellularEncapsulation]
    interface_name: Union[CellularOneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2] = (
        _field(metadata={"alias": "interfaceName"})
    )
    nat: Union[OneOfNatOptionsDef1, OneOfNatOptionsDef2, OneOfNatOptionsDef3]
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tunnel_interface: Union[OneOfTunnelInterfaceOptionsDef1, OneOfTunnelInterfaceOptionsDef2] = (
        _field(metadata={"alias": "tunnelInterface"})
    )
    # ACL/QOS
    acl_qos: Optional[Union[CellularAclQos1, CellularAclQos2]] = _field(
        default=None, metadata={"alias": "aclQos"}
    )
    # Advanced Attributes
    advanced: Optional[CellularAdvanced] = _field(default=None)
    # Tunnel Interface Attributes
    allow_service: Optional[CellularAllowService] = _field(
        default=None, metadata={"alias": "allowService"}
    )
    # Configure ARP entries
    arp: Optional[List[CellularArp]] = _field(default=None)
    bandwidth_downstream: Optional[
        Union[
            CellularOneOfBandwidthDownstreamOptionsDef1,
            OneOfBandwidthDownstreamOptionsDef2,
            OneOfBandwidthDownstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthDownstream"})
    bandwidth_upstream: Optional[
        Union[
            CellularOneOfBandwidthUpstreamOptionsDef1,
            OneOfBandwidthUpstreamOptionsDef2,
            OneOfBandwidthUpstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthUpstream"})
    dhcp_helper: Optional[
        Union[
            OneOfListOfIpV4OptionsDef1,
            CellularOneOfListOfIpV4OptionsDef2,
            OneOfListOfIpV4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    enable_ipv6: Optional[
        Union[OneOfenableIpV6OptionsDef1, OneOfenableIpV6OptionsDef2, OneOfenableIpV6OptionsDef3]
    ] = _field(default=None, metadata={"alias": "enableIpv6"})
    # Multi-Region Fabric
    multi_region_fabric: Optional[CellularMultiRegionFabric] = _field(
        default=None, metadata={"alias": "multiRegionFabric"}
    )
    # NAT Attributes
    nat_attributes_ipv4: Optional[CellularNatAttributesIpv4] = _field(
        default=None, metadata={"alias": "natAttributesIpv4"}
    )
    service_provider: Optional[
        Union[
            OneOfServiceProviderOptionsDef1,
            OneOfServiceProviderOptionsDef2,
            OneOfServiceProviderOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "serviceProvider"})
    # Tunnel Interface Attributes
    tunnel: Optional[CellularTunnel] = _field(default=None)


@dataclass
class CellularPayload:
    """
    WAN VPN Interface Cellular profile parcel schema for PUT request
    """

    data: VpnInterfaceCellularData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanTransportWanVpnInterfaceCellularPayload:
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
    # WAN VPN Interface Cellular profile parcel schema for PUT request
    payload: Optional[CellularPayload] = _field(default=None)


@dataclass
class EditWanVpnInterfaceCellularParcelForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class InterfaceCellularOneOfInterfaceNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceCellularOneOfDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceCellularOneOfListOfIpV4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class InterfaceCellularOneOfBandwidthUpstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfBandwidthDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceCellularModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceCellularOneOfBindOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceCellularOneOfCarrierOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceCellularCarrierDef


@dataclass
class InterfaceCellularOneOfCarrierOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceCellularDefaultCarrierDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceCellularOneOfColorOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceCellularColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceCellularOneOfHelloIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfHelloIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfHelloToleranceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfHelloToleranceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfMaxControlConnectionsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfNatRefreshIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfNatRefreshIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfControllerGroupListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class InterfaceCellularOneOfVmanageConnectionPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfVmanageConnectionPreferenceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfTunnelTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularTunnel:
    """
    Tunnel Interface Attributes
    """

    bind: Optional[
        Union[InterfaceCellularOneOfBindOptionsDef1, OneOfBindOptionsDef2, OneOfBindOptionsDef3]
    ] = _field(default=None)
    border: Optional[
        Union[OneOfBorderOptionsDef1, OneOfBorderOptionsDef2, OneOfBorderOptionsDef3]
    ] = _field(default=None)
    carrier: Optional[
        Union[
            InterfaceCellularOneOfCarrierOptionsDef1,
            OneOfCarrierOptionsDef2,
            InterfaceCellularOneOfCarrierOptionsDef3,
        ]
    ] = _field(default=None)
    clear_dont_fragment: Optional[
        Union[
            OneOfClearDontFragmentOptionsDef1,
            OneOfClearDontFragmentOptionsDef2,
            OneOfClearDontFragmentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "clearDontFragment"})
    color: Optional[
        Union[InterfaceCellularOneOfColorOptionsDef1, OneOfColorOptionsDef2, OneOfColorOptionsDef3]
    ] = _field(default=None)
    exclude_controller_group_list: Optional[
        Union[
            InterfaceCellularOneOfControllerGroupListOptionsDef1,
            OneOfControllerGroupListOptionsDef2,
            OneOfControllerGroupListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "excludeControllerGroupList"})
    group: Optional[
        Union[InterfaceCellularOneOfGroupOptionsDef1, OneOfGroupOptionsDef2, OneOfGroupOptionsDef3]
    ] = _field(default=None)
    hello_interval: Optional[
        Union[
            InterfaceCellularOneOfHelloIntervalOptionsDef1,
            OneOfHelloIntervalOptionsDef2,
            InterfaceCellularOneOfHelloIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "helloInterval"})
    hello_tolerance: Optional[
        Union[
            InterfaceCellularOneOfHelloToleranceOptionsDef1,
            OneOfHelloToleranceOptionsDef2,
            InterfaceCellularOneOfHelloToleranceOptionsDef3,
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
            InterfaceCellularOneOfMaxControlConnectionsOptionsDef1,
            OneOfMaxControlConnectionsOptionsDef2,
            OneOfMaxControlConnectionsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxControlConnections"})
    mode: Optional[Union[InterfaceCellularOneOfModeOptionsDef1, OneOfModeOptionsDef2]] = _field(
        default=None
    )
    nat_refresh_interval: Optional[
        Union[
            InterfaceCellularOneOfNatRefreshIntervalOptionsDef1,
            OneOfNatRefreshIntervalOptionsDef2,
            InterfaceCellularOneOfNatRefreshIntervalOptionsDef3,
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
    port_hop: Optional[
        Union[OneOfPortHopOptionsDef1, OneOfPortHopOptionsDef2, OneOfPortHopOptionsDef3]
    ] = _field(default=None, metadata={"alias": "portHop"})
    restrict: Optional[
        Union[OneOfRestrictOptionsDef1, OneOfRestrictOptionsDef2, OneOfRestrictOptionsDef3]
    ] = _field(default=None)
    tunnel_tcp_mss: Optional[
        Union[
            InterfaceCellularOneOfTunnelTcpMssAdjustOptionsDef1,
            OneOfTunnelTcpMssAdjustOptionsDef2,
            OneOfTunnelTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelTcpMss"})
    v_bond_as_stun_server: Optional[
        Union[
            OneOfVbondAsStunServerOptionsDef1,
            OneOfVbondAsStunServerOptionsDef2,
            OneOfVbondAsStunServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "vBondAsStunServer"})
    v_manage_connection_preference: Optional[
        Union[
            InterfaceCellularOneOfVmanageConnectionPreferenceOptionsDef1,
            OneOfVmanageConnectionPreferenceOptionsDef2,
            InterfaceCellularOneOfVmanageConnectionPreferenceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "vManageConnectionPreference"})


@dataclass
class InterfaceCellularAllowService:
    """
    Tunnel Interface Attributes
    """

    all: Optional[
        Union[OneOfAllowAllOptionsDef1, OneOfAllowAllOptionsDef2, OneOfAllowAllOptionsDef3]
    ] = _field(default=None)
    bfd: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    bgp: Optional[
        Union[OneOfAllowBgpOptionsDef1, OneOfAllowBgpOptionsDef2, OneOfAllowBgpOptionsDef3]
    ] = _field(default=None)
    dhcp: Optional[
        Union[OneOfAllowDhcpOptionsDef1, OneOfAllowDhcpOptionsDef2, OneOfAllowDhcpOptionsDef3]
    ] = _field(default=None)
    dns: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    https: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    icmp: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    netconf: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    ntp: Optional[
        Union[OneOfAllowNtpOptionsDef1, OneOfAllowNtpOptionsDef2, OneOfAllowNtpOptionsDef3]
    ] = _field(default=None)
    ospf: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    snmp: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    ssh: Optional[
        Union[OneOfAllowSshOptionsDef1, OneOfAllowSshOptionsDef2, OneOfAllowSshOptionsDef3]
    ] = _field(default=None)
    stun: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class InterfaceCellularOneOfEncapsulationEncapOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceCellularEncapsulationEncapDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceCellularOneOfEncapsulationPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfEncapsulationWeightOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfEncapsulationWeightOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularEncapsulation:
    encap: InterfaceCellularOneOfEncapsulationEncapOptionsDef
    preference: Optional[
        Union[
            InterfaceCellularOneOfEncapsulationPreferenceOptionsDef1,
            OneOfEncapsulationPreferenceOptionsDef2,
            OneOfEncapsulationPreferenceOptionsDef3,
        ]
    ] = _field(default=None)
    weight: Optional[
        Union[
            InterfaceCellularOneOfEncapsulationWeightOptionsDef1,
            OneOfEncapsulationWeightOptionsDef2,
            InterfaceCellularOneOfEncapsulationWeightOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class InterfaceCellularOneOfCoreRegionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceCellularCoreRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceCellularOneOfCoreRegionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceCellularDefaultCoreRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceCellularOneOfSecondaryRegionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceCellularSecondaryRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceCellularOneOfSecondaryRegionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceCellularDefaultSecondaryRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceCellularMultiRegionFabric:
    """
    Multi-Region Fabric
    """

    core_region: Optional[
        Union[InterfaceCellularOneOfCoreRegionDef1, InterfaceCellularOneOfCoreRegionDef2]
    ] = _field(default=None, metadata={"alias": "coreRegion"})
    enable_core_region: Optional[Union[OneOfEnableRegionDef1, OneOfEnableRegionDef2]] = _field(
        default=None, metadata={"alias": "enableCoreRegion"}
    )
    enable_secondary_region: Optional[Union[OneOfEnableRegionDef1, OneOfEnableRegionDef2]] = _field(
        default=None, metadata={"alias": "enableSecondaryRegion"}
    )
    secondary_region: Optional[
        Union[InterfaceCellularOneOfSecondaryRegionDef1, InterfaceCellularOneOfSecondaryRegionDef2]
    ] = _field(default=None, metadata={"alias": "secondaryRegion"})


@dataclass
class InterfaceCellularOneOfUdpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfUdpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfTcpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfTcpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularNatAttributesIpv4:
    """
    NAT Attributes
    """

    tcp_timeout: Union[
        InterfaceCellularOneOfTcpTimeoutOptionsDef1,
        OneOfTcpTimeoutOptionsDef2,
        InterfaceCellularOneOfTcpTimeoutOptionsDef3,
    ] = _field(metadata={"alias": "tcpTimeout"})
    udp_timeout: Union[
        InterfaceCellularOneOfUdpTimeoutOptionsDef1,
        OneOfUdpTimeoutOptionsDef2,
        InterfaceCellularOneOfUdpTimeoutOptionsDef3,
    ] = _field(metadata={"alias": "udpTimeout"})


@dataclass
class VpnInterfaceCellularOneOfPeriodOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceCellularOneOfPeriodOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef15:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef16:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef17:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceCellularShapingRateUpstreamConfig:
    """
    adaptiveQoS Shaping Rate Upstream config
    """

    default_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef17, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateUpstream"})
    max_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef16, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "maxShapingRateUpstream"})
    min_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef15, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateUpstream"})


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef18:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef19:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef110:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceCellularShapingRateDownstreamConfig:
    """
    adaptiveQoS Shaping Rate Downstream config
    """

    default_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef110, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateDownstream"})
    max_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef19, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "maxShapingRateDownstream"})
    min_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef18, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateDownstream"})


@dataclass
class InterfaceCellularAclQos1:
    adaptive_qo_s: Union[OneOfQosAdaptiveOptionsDef1, OneOfQosAdaptiveOptionsDef2] = _field(
        metadata={"alias": "adaptiveQoS"}
    )
    shaping_rate_upstream: ShapingRateUpstream = _field(metadata={"alias": "shapingRateUpstream"})
    # adaptiveQoS Shaping Rate Upstream config
    shaping_rate_upstream_config: VpnInterfaceCellularShapingRateUpstreamConfig = _field(
        metadata={"alias": "shapingRateUpstreamConfig"}
    )
    adapt_period: Optional[
        Union[
            VpnInterfaceCellularOneOfPeriodOptionsDef1,
            OneOfPeriodOptionsDef2,
            VpnInterfaceCellularOneOfPeriodOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "adaptPeriod"})
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
    shaping_rate_downstream: Optional[
        Union[OneOfShapingRateDownstreamOptionsDef1, OneOfShapingRateDownstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateDownstream"})
    # adaptiveQoS Shaping Rate Downstream config
    shaping_rate_downstream_config: Optional[VpnInterfaceCellularShapingRateDownstreamConfig] = (
        _field(default=None, metadata={"alias": "shapingRateDownstreamConfig"})
    )


@dataclass
class WanVpnInterfaceCellularOneOfPeriodOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnInterfaceCellularOneOfPeriodOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef111:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef112:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef113:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnInterfaceCellularShapingRateUpstreamConfig:
    """
    adaptiveQoS Shaping Rate Upstream config
    """

    default_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef113, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateUpstream"})
    max_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef112, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "maxShapingRateUpstream"})
    min_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef111, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateUpstream"})


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef114:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef115:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef116:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnInterfaceCellularShapingRateDownstreamConfig:
    """
    adaptiveQoS Shaping Rate Downstream config
    """

    default_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef116, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateDownstream"})
    max_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef115, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "maxShapingRateDownstream"})
    min_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef114, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateDownstream"})


@dataclass
class InterfaceCellularAclQos2:
    adaptive_qo_s: Union[OneOfQosAdaptiveOptionsDef1, OneOfQosAdaptiveOptionsDef2] = _field(
        metadata={"alias": "adaptiveQoS"}
    )
    adapt_period: Optional[
        Union[
            WanVpnInterfaceCellularOneOfPeriodOptionsDef1,
            OneOfPeriodOptionsDef2,
            WanVpnInterfaceCellularOneOfPeriodOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "adaptPeriod"})
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
    shaping_rate_downstream: Optional[
        Union[OneOfShapingRateDownstreamOptionsDef1, OneOfShapingRateDownstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateDownstream"})
    # adaptiveQoS Shaping Rate Downstream config
    shaping_rate_downstream_config: Optional[WanVpnInterfaceCellularShapingRateDownstreamConfig] = (
        _field(default=None, metadata={"alias": "shapingRateDownstreamConfig"})
    )
    shaping_rate_upstream: Optional[
        Union[OneOfShapingRateUpstreamOptionsDef1, OneOfShapingRateUpstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateUpstream"})
    # adaptiveQoS Shaping Rate Upstream config
    shaping_rate_upstream_config: Optional[WanVpnInterfaceCellularShapingRateUpstreamConfig] = (
        _field(default=None, metadata={"alias": "shapingRateUpstreamConfig"})
    )


@dataclass
class InterfaceCellularOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceCellularOneOfMacAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceCellularArp:
    ip_address: Union[
        OneOfIpV4AddressOptionsDef1,
        InterfaceCellularOneOfIpV4AddressOptionsDef2,
        OneOfIpV4AddressOptionsDef3,
    ] = _field(metadata={"alias": "ipAddress"})
    mac_address: Union[
        InterfaceCellularOneOfMacAddressOptionsDef1,
        OneOfMacAddressOptionsDef2,
        OneOfMacAddressOptionsDef3,
    ] = _field(metadata={"alias": "macAddress"})


@dataclass
class InterfaceCellularOneOfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfIntrfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfIntrfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceCellularOneOfTlocExtensionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceCellularOneOfTrackerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceCellularAdvanced:
    """
    Advanced Attributes
    """

    intrf_mtu: Optional[
        Union[
            InterfaceCellularOneOfIntrfMtuOptionsDef1,
            OneOfIntrfMtuOptionsDef2,
            InterfaceCellularOneOfIntrfMtuOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "intrfMtu"})
    ip_directed_broadcast: Optional[
        Union[
            OneOfIpDirectedBroadcastOptionsDef1,
            OneOfIpDirectedBroadcastOptionsDef2,
            OneOfIpDirectedBroadcastOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipDirectedBroadcast"})
    ip_mtu: Optional[
        Union[
            InterfaceCellularOneOfMtuOptionsDef1,
            OneOfMtuOptionsDef2,
            InterfaceCellularOneOfMtuOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipMtu"})
    tcp_mss: Optional[
        Union[
            InterfaceCellularOneOfTcpMssAdjustOptionsDef1,
            OneOfTcpMssAdjustOptionsDef2,
            OneOfTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMss"})
    tloc_extension: Optional[
        Union[
            InterfaceCellularOneOfTlocExtensionOptionsDef1,
            OneOfTlocExtensionOptionsDef2,
            OneOfTlocExtensionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tlocExtension"})
    tracker: Optional[
        Union[
            InterfaceCellularOneOfTrackerOptionsDef1,
            OneOfTrackerOptionsDef2,
            OneOfTrackerOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class WanVpnInterfaceCellularData:
    description: Union[
        InterfaceCellularOneOfDescriptionOptionsDef1,
        OneOfDescriptionOptionsDef2,
        OneOfDescriptionOptionsDef3,
    ]
    # Encapsulation for TLOC
    encapsulation: List[InterfaceCellularEncapsulation]
    interface_name: Union[
        InterfaceCellularOneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2
    ] = _field(metadata={"alias": "interfaceName"})
    nat: Union[OneOfNatOptionsDef1, OneOfNatOptionsDef2, OneOfNatOptionsDef3]
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tunnel_interface: Union[OneOfTunnelInterfaceOptionsDef1, OneOfTunnelInterfaceOptionsDef2] = (
        _field(metadata={"alias": "tunnelInterface"})
    )
    # ACL/QOS
    acl_qos: Optional[Union[InterfaceCellularAclQos1, InterfaceCellularAclQos2]] = _field(
        default=None, metadata={"alias": "aclQos"}
    )
    # Advanced Attributes
    advanced: Optional[InterfaceCellularAdvanced] = _field(default=None)
    # Tunnel Interface Attributes
    allow_service: Optional[InterfaceCellularAllowService] = _field(
        default=None, metadata={"alias": "allowService"}
    )
    # Configure ARP entries
    arp: Optional[List[InterfaceCellularArp]] = _field(default=None)
    bandwidth_downstream: Optional[
        Union[
            InterfaceCellularOneOfBandwidthDownstreamOptionsDef1,
            OneOfBandwidthDownstreamOptionsDef2,
            OneOfBandwidthDownstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthDownstream"})
    bandwidth_upstream: Optional[
        Union[
            InterfaceCellularOneOfBandwidthUpstreamOptionsDef1,
            OneOfBandwidthUpstreamOptionsDef2,
            OneOfBandwidthUpstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthUpstream"})
    dhcp_helper: Optional[
        Union[
            OneOfListOfIpV4OptionsDef1,
            InterfaceCellularOneOfListOfIpV4OptionsDef2,
            OneOfListOfIpV4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    enable_ipv6: Optional[
        Union[OneOfenableIpV6OptionsDef1, OneOfenableIpV6OptionsDef2, OneOfenableIpV6OptionsDef3]
    ] = _field(default=None, metadata={"alias": "enableIpv6"})
    # Multi-Region Fabric
    multi_region_fabric: Optional[InterfaceCellularMultiRegionFabric] = _field(
        default=None, metadata={"alias": "multiRegionFabric"}
    )
    # NAT Attributes
    nat_attributes_ipv4: Optional[InterfaceCellularNatAttributesIpv4] = _field(
        default=None, metadata={"alias": "natAttributesIpv4"}
    )
    service_provider: Optional[
        Union[
            OneOfServiceProviderOptionsDef1,
            OneOfServiceProviderOptionsDef2,
            OneOfServiceProviderOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "serviceProvider"})
    # Tunnel Interface Attributes
    tunnel: Optional[InterfaceCellularTunnel] = _field(default=None)


@dataclass
class EditWanVpnInterfaceCellularParcelForTransportPutRequest:
    """
    WAN VPN Interface Cellular profile parcel schema for PUT request
    """

    data: WanVpnInterfaceCellularData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
