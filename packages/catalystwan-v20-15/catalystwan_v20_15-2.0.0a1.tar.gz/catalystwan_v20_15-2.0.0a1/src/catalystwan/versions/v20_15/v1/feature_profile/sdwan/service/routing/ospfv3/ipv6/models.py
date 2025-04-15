# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

OptionType = Literal["default", "global"]

MetricTypeDef = Literal["type1", "type2"]

Ipv6RedistributeProtocolDef = Literal["bgp", "connected", "eigrp", "omp", "static"]

Value = Literal["stub"]

Ipv6Value = Literal["nssa"]

Ospfv3Ipv6Value = Literal["normal"]

AreaInterfaceNetworkDef = Literal[
    "broadcast", "non-broadcast", "point-to-multipoint", "point-to-point"
]

RoutingOspfv3Ipv6Value = Literal["no-auth"]

ServiceRoutingOspfv3Ipv6Value = Literal["ipsec-sha1"]


@dataclass
class OneOfIpV4AddressDefaultOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4AddressDefaultOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfIpV4AddressDefaultOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDistanceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDistanceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDistanceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfExternalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfExternalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfExternalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterAreaOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterAreaOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterAreaOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIntraAreaOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIntraAreaOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIntraAreaOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BasicConfigDef:
    distance: Optional[
        Union[OneOfDistanceOptionsDef1, OneOfDistanceOptionsDef2, OneOfDistanceOptionsDef3]
    ] = _field(default=None)
    external_distance: Optional[
        Union[OneOfExternalOptionsDef1, OneOfExternalOptionsDef2, OneOfExternalOptionsDef3]
    ] = _field(default=None, metadata={"alias": "externalDistance"})
    inter_area_distance: Optional[
        Union[OneOfInterAreaOptionsDef1, OneOfInterAreaOptionsDef2, OneOfInterAreaOptionsDef3]
    ] = _field(default=None, metadata={"alias": "interAreaDistance"})
    intra_area_distance: Optional[
        Union[OneOfIntraAreaOptionsDef1, OneOfIntraAreaOptionsDef2, OneOfIntraAreaOptionsDef3]
    ] = _field(default=None, metadata={"alias": "intraAreaDistance"})
    router_id: Optional[
        Union[
            OneOfIpV4AddressDefaultOptionsDef1,
            OneOfIpV4AddressDefaultOptionsDef2,
            OneOfIpV4AddressDefaultOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "routerId"})


@dataclass
class OneOfReferenceBandwidthOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfReferenceBandwidthOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfReferenceBandwidthOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


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
class Originate:
    """
    Distribute default external route into OSPF disabled
    """

    option_type: OptionType = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDefaultOriginateOptionsDef1:
    # Distribute default external route into OSPF disabled
    originate: Optional[Originate] = _field(default=None)


@dataclass
class Ipv6Originate:
    """
    Distribute default external route into OSPF enabled
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


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
class OneOfMetricOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMetricOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMetricOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfMetricTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: MetricTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfMetricTypeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMetricTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDefaultOriginateOptionsDef2:
    # Distribute default external route into OSPF enabled
    originate: Ipv6Originate
    always: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    metric: Optional[
        Union[OneOfMetricOptionsDef1, OneOfMetricOptionsDef2, OneOfMetricOptionsDef3]
    ] = _field(default=None)
    metric_type: Optional[
        Union[OneOfMetricTypeOptionsDef1, OneOfMetricTypeOptionsDef2, OneOfMetricTypeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "metricType"})


@dataclass
class OneOfDelayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDelayOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDelayOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInitialHoldOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInitialHoldOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInitialHoldOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMaxHoldOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMaxHoldOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMaxHoldOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SpfTimersDef:
    delay: Optional[Union[OneOfDelayOptionsDef1, OneOfDelayOptionsDef2, OneOfDelayOptionsDef3]] = (
        _field(default=None)
    )
    initial_hold: Optional[
        Union[OneOfInitialHoldOptionsDef1, OneOfInitialHoldOptionsDef2, OneOfInitialHoldOptionsDef3]
    ] = _field(default=None, metadata={"alias": "initialHold"})
    max_hold: Optional[
        Union[OneOfMaxHoldOptionsDef1, OneOfMaxHoldOptionsDef2, OneOfMaxHoldOptionsDef3]
    ] = _field(default=None, metadata={"alias": "maxHold"})


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
class AdvancedConfigDef:
    compatible_rfc1583: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "compatibleRfc1583"})
    default_originate: Optional[
        Union[OneOfDefaultOriginateOptionsDef1, OneOfDefaultOriginateOptionsDef2]
    ] = _field(default=None, metadata={"alias": "defaultOriginate"})
    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    policy_name: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "policyName"})
    reference_bandwidth: Optional[
        Union[
            OneOfReferenceBandwidthOptionsDef1,
            OneOfReferenceBandwidthOptionsDef2,
            OneOfReferenceBandwidthOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "referenceBandwidth"})
    spf_timers: Optional[SpfTimersDef] = _field(default=None, metadata={"alias": "spfTimers"})


@dataclass
class OneOfIpv6RedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv6RedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpv6RedistributeProtocolOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Ipv6RedistributeProtocolsObjDef:
    protocol: Union[
        OneOfIpv6RedistributeProtocolOptionsDef1, OneOfIpv6RedistributeProtocolOptionsDef2
    ]
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})
    translate_rib_metric: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "translateRibMetric"})


@dataclass
class Action:
    """
    Not advertise maximum metric Router LSA policy by default
    """

    option_type: OptionType = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfMaxMetricRouterLsaOptionsDef1:
    # Not advertise maximum metric Router LSA policy by default
    action: Action


@dataclass
class Ipv6Action:
    """
    Advertise maximum metric Router LSA immediately
    """

    option_type: Any = _field(metadata={"alias": "optionType"})
    value: Any


@dataclass
class OneOfMaxMetricRouterLsaOptionsDef2:
    # Advertise maximum metric Router LSA immediately
    action: Ipv6Action


@dataclass
class Ospfv3Ipv6Action:
    """
    Advertise maximum metric router LSA after router start up with configured duration time(seconds)
    """

    option_type: Any = _field(metadata={"alias": "optionType"})
    value: Any


@dataclass
class OneOfOnStartUpTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfOnStartUpTimeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMaxMetricRouterLsaOptionsDef3:
    # Advertise maximum metric router LSA after router start up with configured duration time(seconds)
    action: Ospfv3Ipv6Action
    on_start_up_time: Union[OneOfOnStartUpTimeOptionsDef1, OneOfOnStartUpTimeOptionsDef2] = _field(
        metadata={"alias": "onStartUpTime"}
    )


@dataclass
class OneOfAreaNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAreaNumOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class AreaType:
    """
    stub area type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAreaTypeConfigOptionsDef1:
    # stub area type
    area_type: Optional[AreaType] = _field(default=None, metadata={"alias": "areaType"})
    no_summary: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "noSummary"})


@dataclass
class Ipv6AreaType:
    """
    NSSA area type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv6Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAreaTypeConfigOptionsDef2:
    always_translate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "alwaysTranslate"})
    # NSSA area type
    area_type: Optional[Ipv6AreaType] = _field(default=None, metadata={"alias": "areaType"})
    no_summary: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "noSummary"})


@dataclass
class Ospfv3Ipv6AreaType:
    """
    Normal area type, area number 0 only support normal area type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ospfv3Ipv6Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAreaTypeConfigOptionsDef3:
    # Normal area type, area number 0 only support normal area type
    area_type: Optional[Ospfv3Ipv6AreaType] = _field(default=None, metadata={"alias": "areaType"})


@dataclass
class DefaultOptionNoDefaultDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAreaTypeConfigOptionsDef4:
    area_type: Optional[DefaultOptionNoDefaultDef] = _field(
        default=None, metadata={"alias": "areaType"}
    )


@dataclass
class OneOfAreaInterfaceNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAreaInterfaceNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAreaInterfaceHelloIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAreaInterfaceHelloIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAreaInterfaceHelloIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAreaInterfaceDeadIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAreaInterfaceDeadIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAreaInterfaceDeadIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAreaInterfaceRetransmitIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAreaInterfaceRetransmitIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAreaInterfaceRetransmitIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAreaInterfaceCostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAreaInterfaceCostOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAreaInterfaceCostOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAreaInterfaceNetworkOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AreaInterfaceNetworkDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAreaInterfaceNetworkOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAreaInterfaceNetworkOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class AreaInterfaceNoAuthTypeDef:
    option_type: OptionType = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RoutingOspfv3Ipv6Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAreaInterfaceAuthConfigOptionsDef1:
    auth_type: AreaInterfaceNoAuthTypeDef = _field(metadata={"alias": "authType"})


@dataclass
class AreaInterfaceIpsecSha1AuthTypeDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceRoutingOspfv3Ipv6Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAreaInterfaceSpiOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAreaInterfaceSpiOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAreaInterfaceSha1AuthKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAreaInterfaceSha1AuthKeyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAreaInterfaceAuthConfigOptionsDef2:
    auth_key: Union[
        OneOfAreaInterfaceSha1AuthKeyOptionsDef1, OneOfAreaInterfaceSha1AuthKeyOptionsDef2
    ] = _field(metadata={"alias": "authKey"})
    auth_type: AreaInterfaceIpsecSha1AuthTypeDef = _field(metadata={"alias": "authType"})
    spi: Union[OneOfAreaInterfaceSpiOptionsDef1, OneOfAreaInterfaceSpiOptionsDef2]


@dataclass
class AreaInterfaceDef:
    if_name: Union[OneOfAreaInterfaceNameOptionsDef1, OneOfAreaInterfaceNameOptionsDef2] = _field(
        metadata={"alias": "ifName"}
    )
    authentication_config: Optional[
        Union[OneOfAreaInterfaceAuthConfigOptionsDef1, OneOfAreaInterfaceAuthConfigOptionsDef2]
    ] = _field(default=None, metadata={"alias": "authenticationConfig"})
    cost: Optional[
        Union[
            OneOfAreaInterfaceCostOptionsDef1,
            OneOfAreaInterfaceCostOptionsDef2,
            OneOfAreaInterfaceCostOptionsDef3,
        ]
    ] = _field(default=None)
    dead_interval: Optional[
        Union[
            OneOfAreaInterfaceDeadIntervalOptionsDef1,
            OneOfAreaInterfaceDeadIntervalOptionsDef2,
            OneOfAreaInterfaceDeadIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "deadInterval"})
    hello_interval: Optional[
        Union[
            OneOfAreaInterfaceHelloIntervalOptionsDef1,
            OneOfAreaInterfaceHelloIntervalOptionsDef2,
            OneOfAreaInterfaceHelloIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "helloInterval"})
    network_type: Optional[
        Union[
            OneOfAreaInterfaceNetworkOptionsDef1,
            OneOfAreaInterfaceNetworkOptionsDef2,
            OneOfAreaInterfaceNetworkOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "networkType"})
    passive_interface: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "passiveInterface"})
    retransmit_interval: Optional[
        Union[
            OneOfAreaInterfaceRetransmitIntervalOptionsDef1,
            OneOfAreaInterfaceRetransmitIntervalOptionsDef2,
            OneOfAreaInterfaceRetransmitIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "retransmitInterval"})


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
class OneOfAreaRangeCostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAreaRangeCostOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAreaRangeCostOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Ipv6AreaRangeDef:
    network: Union[
        OneOfIpv6PrefixGlobalVariableWithoutDefault1, OneOfIpv6PrefixGlobalVariableWithoutDefault2
    ]
    no_advertise: Union[
        OneOfOnBooleanDefaultFalseOptionsDef1,
        OneOfOnBooleanDefaultFalseOptionsDef2,
        OneOfOnBooleanDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "noAdvertise"})
    cost: Optional[
        Union[
            OneOfAreaRangeCostOptionsDef1,
            OneOfAreaRangeCostOptionsDef2,
            OneOfAreaRangeCostOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class Area:
    area_num: Union[OneOfAreaNumOptionsDef1, OneOfAreaNumOptionsDef2] = _field(
        metadata={"alias": "areaNum"}
    )
    # Set OSPF interface parameters
    interfaces: List[AreaInterfaceDef]
    area_type_config: Optional[
        Union[
            OneOfAreaTypeConfigOptionsDef1,
            OneOfAreaTypeConfigOptionsDef2,
            OneOfAreaTypeConfigOptionsDef3,
            OneOfAreaTypeConfigOptionsDef4,
        ]
    ] = _field(default=None, metadata={"alias": "areaTypeConfig"})
    # Summarize OSPF routes at an area boundary
    ranges: Optional[List[Ipv6AreaRangeDef]] = _field(default=None)


@dataclass
class Ipv6Data:
    """
    IPv6 address family configuration
    """

    # Configure OSPFv3 IPv6 area
    area: List[Area]
    advanced: Optional[AdvancedConfigDef] = _field(default=None)
    basic: Optional[BasicConfigDef] = _field(default=None)
    max_metric_router_lsa: Optional[
        Union[
            OneOfMaxMetricRouterLsaOptionsDef1,
            OneOfMaxMetricRouterLsaOptionsDef2,
            OneOfMaxMetricRouterLsaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxMetricRouterLsa"})
    redistribute: Optional[List[Ipv6RedistributeProtocolsObjDef]] = _field(default=None)


@dataclass
class Payload:
    """
    Routing protocol OSPFv3 for IPv6 Address family feature schema
    """

    # IPv6 address family configuration
    data: Ipv6Data
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
    # Routing protocol OSPFv3 for IPv6 Address family feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanServiceRoutingOspfv3Ipv6Payload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateRoutingOspfv3Ipv6AfProfileParcelForServicePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Ospfv3Ipv6Data:
    """
    IPv6 address family configuration
    """

    # Configure OSPFv3 IPv6 area
    area: List[Area]
    advanced: Optional[AdvancedConfigDef] = _field(default=None)
    basic: Optional[BasicConfigDef] = _field(default=None)
    max_metric_router_lsa: Optional[
        Union[
            OneOfMaxMetricRouterLsaOptionsDef1,
            OneOfMaxMetricRouterLsaOptionsDef2,
            OneOfMaxMetricRouterLsaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxMetricRouterLsa"})
    redistribute: Optional[List[Ipv6RedistributeProtocolsObjDef]] = _field(default=None)


@dataclass
class CreateRoutingOspfv3Ipv6AfProfileParcelForServicePostRequest:
    """
    Routing protocol OSPFv3 for IPv6 Address family feature schema
    """

    # IPv6 address family configuration
    data: Ospfv3Ipv6Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanServiceRoutingOspfv3Ipv6Payload:
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
    # Routing protocol OSPFv3 for IPv6 Address family feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditRoutingOspfv3IPv6AfProfileParcelForServicePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class RoutingOspfv3Ipv6Data:
    """
    IPv6 address family configuration
    """

    # Configure OSPFv3 IPv6 area
    area: List[Area]
    advanced: Optional[AdvancedConfigDef] = _field(default=None)
    basic: Optional[BasicConfigDef] = _field(default=None)
    max_metric_router_lsa: Optional[
        Union[
            OneOfMaxMetricRouterLsaOptionsDef1,
            OneOfMaxMetricRouterLsaOptionsDef2,
            OneOfMaxMetricRouterLsaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxMetricRouterLsa"})
    redistribute: Optional[List[Ipv6RedistributeProtocolsObjDef]] = _field(default=None)


@dataclass
class EditRoutingOspfv3IPv6AfProfileParcelForServicePutRequest:
    """
    Routing protocol OSPFv3 for IPv6 Address family feature schema
    """

    # IPv6 address family configuration
    data: RoutingOspfv3Ipv6Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
