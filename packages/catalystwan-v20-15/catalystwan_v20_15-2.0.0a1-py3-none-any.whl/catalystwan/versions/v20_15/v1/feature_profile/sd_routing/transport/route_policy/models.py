# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

DefaultActionDef = Literal["accept", "reject"]

DefaultOptionTypeDef = Literal["default"]

Value = Literal["reject"]

SequencesBaseActionDef = Literal["accept", "reject"]

ProtocolDef = Literal["BOTH", "IPV4", "IPV6"]

RoutePolicyValue = Literal["IPV4"]

VariableOptionTypeDef = Literal["variable"]

MetricTypeDef = Literal["type1", "type2"]

OriginDef = Literal["EGP", "IGP", "Incomplete"]


@dataclass
class OneOfDefaultActionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultActionDef


@dataclass
class OneOfDefaultActionOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSequencesSequenceIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSequencesSequenceNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSequencesBaseActionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SequencesBaseActionDef


@dataclass
class OneOfSequencesBaseActionOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSequencesProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ProtocolDef


@dataclass
class OneOfSequencesProtocolOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RoutePolicyValue  # pytype: disable=annotation-type-mismatch


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
class OneOfOnBooleanDefaultFalseNoVariableOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultFalseNoVariableOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfSequencesMatchEntriesCommunityListDef1:
    exact: Union[
        OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
        OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
    ]
    standard_community_list: List[ParcelReferenceDef] = _field(
        metadata={"alias": "standardCommunityList"}
    )


@dataclass
class OneOfSequencesMatchEntriesCommunityListDef2:
    expanded_community_list: List[ParcelReferenceDef] = _field(
        metadata={"alias": "expandedCommunityList"}
    )


@dataclass
class OneOfSequencesMatchEntriesBgpLocalPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class OneOfSequencesMatchEntriesMetricOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class OneOfSequencesMatchEntriesOspfTagOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class OneOfSequencesMatchEntriesIpv4AddressDef1:
    prefix_list: List[ParcelReferenceDef] = _field(metadata={"alias": "prefixList"})


@dataclass
class OneOfSequencesMatchEntriesIpv4AddressDef2:
    acl_name_list: List[ParcelReferenceDef] = _field(metadata={"alias": "aclNameList"})


@dataclass
class OneOfSequencesMatchEntriesIpv4NextHopDef1:
    prefix_list: List[ParcelReferenceDef] = _field(metadata={"alias": "prefixList"})


@dataclass
class OneOfSequencesMatchEntriesIpv4NextHopDef2:
    acl_name_list: List[ParcelReferenceDef] = _field(metadata={"alias": "aclNameList"})


@dataclass
class OneOfSequencesInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class MatchEntries:
    as_path_list: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "asPathList"}
    )
    bgp_local_preference: Optional[OneOfSequencesMatchEntriesBgpLocalPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "bgpLocalPreference"}
    )
    community_list: Optional[
        Union[
            OneOfSequencesMatchEntriesCommunityListDef1, OneOfSequencesMatchEntriesCommunityListDef2
        ]
    ] = _field(default=None, metadata={"alias": "communityList"})
    ext_community_list: Optional[List[ParcelReferenceDef]] = _field(
        default=None, metadata={"alias": "extCommunityList"}
    )
    interface: Optional[OneOfSequencesInterfaceOptionsDef] = _field(default=None)
    ipv4_address: Optional[
        Union[OneOfSequencesMatchEntriesIpv4AddressDef1, OneOfSequencesMatchEntriesIpv4AddressDef2]
    ] = _field(default=None, metadata={"alias": "ipv4Address"})
    ipv4_next_hop: Optional[
        Union[OneOfSequencesMatchEntriesIpv4NextHopDef1, OneOfSequencesMatchEntriesIpv4NextHopDef2]
    ] = _field(default=None, metadata={"alias": "ipv4NextHop"})
    ipv6_address: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6Address"}
    )
    ipv6_next_hop: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6NextHop"}
    )
    metric: Optional[OneOfSequencesMatchEntriesMetricOptionsDef] = _field(default=None)
    ospf_tag: Optional[OneOfSequencesMatchEntriesOspfTagOptionsDef] = _field(
        default=None, metadata={"alias": "ospfTag"}
    )


@dataclass
class SequencesActionsEnableAcceptOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class PrependOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[int, str]]


@dataclass
class SequencesActionsSetAsPathOptionsDef:
    prepend: Optional[PrependOptionsDef] = _field(default=None)


@dataclass
class OneOfSequencesActionsSetCommunityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[str, str]]


@dataclass
class OneOfSequencesActionsSetCommunityOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class SequencesActionsSetCommunityDef:
    additive: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None)
    community: Optional[
        Union[
            OneOfSequencesActionsSetCommunityOptionsDef1,
            OneOfSequencesActionsSetCommunityOptionsDef2,
        ]
    ] = _field(default=None)


@dataclass
class OneOfSequencesActionsSetLocalPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSequencesActionsSetMetricOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSequencesActionsSetMetricTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: MetricTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SetOriginOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: OriginDef  # pytype: disable=annotation-type-mismatch


@dataclass
class RemoteAsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSequencesActionsSetOriginOptionsDef:
    origin_option: SetOriginOptionsDef = _field(metadata={"alias": "originOption"})
    remote_as: Optional[RemoteAsDef] = _field(default=None, metadata={"alias": "remoteAs"})


@dataclass
class OneOfSequencesActionsSetOspfTagOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSequencesActionsSetWeightOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSequencesActionsSetIpv4NextHopDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfSequencesActionsSetIpv6NextHopDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class Accept:
    """
    Accept Action
    """

    enable_accept_action: SequencesActionsEnableAcceptOptionsDef = _field(
        metadata={"alias": "enableAcceptAction"}
    )
    set_as_path: Optional[SequencesActionsSetAsPathOptionsDef] = _field(
        default=None, metadata={"alias": "setAsPath"}
    )
    set_community: Optional[SequencesActionsSetCommunityDef] = _field(
        default=None, metadata={"alias": "setCommunity"}
    )
    set_interface: Optional[OneOfSequencesInterfaceOptionsDef] = _field(
        default=None, metadata={"alias": "setInterface"}
    )
    set_ipv4_next_hop: Optional[OneOfSequencesActionsSetIpv4NextHopDef] = _field(
        default=None, metadata={"alias": "setIpv4NextHop"}
    )
    set_ipv6_next_hop: Optional[OneOfSequencesActionsSetIpv6NextHopDef] = _field(
        default=None, metadata={"alias": "setIpv6NextHop"}
    )
    set_local_preference: Optional[OneOfSequencesActionsSetLocalPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "setLocalPreference"}
    )
    set_metric: Optional[OneOfSequencesActionsSetMetricOptionsDef] = _field(
        default=None, metadata={"alias": "setMetric"}
    )
    set_metric_type: Optional[OneOfSequencesActionsSetMetricTypeOptionsDef] = _field(
        default=None, metadata={"alias": "setMetricType"}
    )
    set_origin: Optional[OneOfSequencesActionsSetOriginOptionsDef] = _field(
        default=None, metadata={"alias": "setOrigin"}
    )
    set_ospf_tag: Optional[OneOfSequencesActionsSetOspfTagOptionsDef] = _field(
        default=None, metadata={"alias": "setOspfTag"}
    )
    set_weight: Optional[OneOfSequencesActionsSetWeightOptionsDef] = _field(
        default=None, metadata={"alias": "setWeight"}
    )


@dataclass
class Actions1:
    # Accept Action
    accept: Accept


@dataclass
class SequencesActionsRejectOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Actions2:
    reject: SequencesActionsRejectOptionsDef


@dataclass
class Sequences:
    base_action: Union[OneOfSequencesBaseActionOptionsDef1, OneOfSequencesBaseActionOptionsDef2] = (
        _field(metadata={"alias": "baseAction"})
    )
    protocol: Union[OneOfSequencesProtocolOptionsDef1, OneOfSequencesProtocolOptionsDef2]
    sequence_id: OneOfSequencesSequenceIdOptionsDef = _field(metadata={"alias": "sequenceId"})
    sequence_name: OneOfSequencesSequenceNameOptionsDef = _field(metadata={"alias": "sequenceName"})
    # Define list of actions
    actions: Optional[List[Union[Actions1, Actions2]]] = _field(default=None)
    # Define match conditions
    match_entries: Optional[List[MatchEntries]] = _field(
        default=None, metadata={"alias": "matchEntries"}
    )


@dataclass
class RoutePolicyData:
    default_action: Union[OneOfDefaultActionOptionsDef1, OneOfDefaultActionOptionsDef2] = _field(
        metadata={"alias": "defaultAction"}
    )
    # Route Policy List
    sequences: Optional[List[Sequences]] = _field(default=None)


@dataclass
class Payload:
    """
    Route policy profile feature schema
    """

    data: RoutePolicyData
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
    # Route policy profile feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingTransportRoutePolicyPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingTransportRoutePolicyFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class TransportRoutePolicyData:
    default_action: Union[OneOfDefaultActionOptionsDef1, OneOfDefaultActionOptionsDef2] = _field(
        metadata={"alias": "defaultAction"}
    )
    # Route Policy List
    sequences: Optional[List[Sequences]] = _field(default=None)


@dataclass
class CreateSdroutingTransportRoutePolicyFeaturePostRequest:
    """
    Route policy profile feature schema
    """

    data: TransportRoutePolicyData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingTransportRoutePolicyPayload:
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
    # Route policy profile feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingTransportRoutePolicyFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingTransportRoutePolicyData:
    default_action: Union[OneOfDefaultActionOptionsDef1, OneOfDefaultActionOptionsDef2] = _field(
        metadata={"alias": "defaultAction"}
    )
    # Route Policy List
    sequences: Optional[List[Sequences]] = _field(default=None)


@dataclass
class EditSdroutingTransportRoutePolicyFeaturePutRequest:
    """
    Route policy profile feature schema
    """

    data: SdRoutingTransportRoutePolicyData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
