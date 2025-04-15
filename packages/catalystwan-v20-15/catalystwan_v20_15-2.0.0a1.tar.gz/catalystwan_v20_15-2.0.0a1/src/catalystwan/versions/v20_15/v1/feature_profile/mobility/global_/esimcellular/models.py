# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

WanConfigDef = Literal["Active", "Standby"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

DefaultAuthenticationDef = Literal["none"]

AuthenticationDef = Literal["chap", "pap", "pap_chap"]

PdnTypeDef = Literal["IPv4", "IPv4v6", "IPv6"]

DefaultPdnTypeDef = Literal["IPv4"]

EsimcellularWanConfigDef = Literal["Active", "Standby"]

EsimcellularDefaultAuthenticationDef = Literal["none"]

EsimcellularAuthenticationDef = Literal["chap", "pap", "pap_chap"]

EsimcellularPdnTypeDef = Literal["IPv4", "IPv4v6", "IPv6"]

EsimcellularDefaultPdnTypeDef = Literal["IPv4"]

GlobalEsimcellularDefaultAuthenticationDef = Literal["none"]

GlobalEsimcellularAuthenticationDef = Literal["chap", "pap", "pap_chap"]

GlobalEsimcellularPdnTypeDef = Literal["IPv4", "IPv4v6", "IPv6"]

GlobalEsimcellularDefaultPdnTypeDef = Literal["IPv4"]

GlobalEsimcellularWanConfigDef = Literal["Active", "Standby"]

MobilityGlobalEsimcellularDefaultAuthenticationDef = Literal["none"]

MobilityGlobalEsimcellularAuthenticationDef = Literal["chap", "pap", "pap_chap"]

MobilityGlobalEsimcellularPdnTypeDef = Literal["IPv4", "IPv4v6", "IPv6"]

MobilityGlobalEsimcellularDefaultPdnTypeDef = Literal["IPv4"]

FeatureProfileMobilityGlobalEsimcellularDefaultAuthenticationDef = Literal["none"]

FeatureProfileMobilityGlobalEsimcellularAuthenticationDef = Literal["chap", "pap", "pap_chap"]

FeatureProfileMobilityGlobalEsimcellularPdnTypeDef = Literal["IPv4", "IPv4v6", "IPv6"]

FeatureProfileMobilityGlobalEsimcellularDefaultPdnTypeDef = Literal["IPv4"]


@dataclass
class WanConfigOptionTypesDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: WanConfigDef  # pytype: disable=annotation-type-mismatch


@dataclass
class WanConfigOptionTypesDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class AccountId:
    """
    Set provider account Id used for this configuration
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CommPlan:
    """
    Set communication plan used for this configuration
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RatePlan:
    """
    Set rate plan used for this configuration
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ESimAccountInfoDef:
    # Set provider account Id used for this configuration
    account_id: AccountId = _field(metadata={"alias": "accountId"})
    # Set communication plan used for this configuration
    comm_plan: CommPlan = _field(metadata={"alias": "commPlan"})
    # Set rate plan used for this configuration
    rate_plan: RatePlan = _field(metadata={"alias": "ratePlan"})


@dataclass
class OneOfApnOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDefaultAuthenticationOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Authentication1:
    no_authentication: OneOfDefaultAuthenticationOptionsDef = _field(
        metadata={"alias": "noAuthentication"}
    )


@dataclass
class OneOfAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAuthenticationOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUsernameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUsernameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPasswordOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class NeedAuthentication:
    password: Union[OneOfPasswordOptionsDef1, OneOfPasswordOptionsDef2]
    type_: Union[OneOfAuthenticationOptionsDef1, OneOfAuthenticationOptionsDef2] = _field(
        metadata={"alias": "type"}
    )
    username: Union[OneOfUsernameOptionsDef1, OneOfUsernameOptionsDef2]


@dataclass
class Authentication2:
    need_authentication: NeedAuthentication = _field(metadata={"alias": "needAuthentication"})


@dataclass
class OneOfPdnTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PdnTypeDef


@dataclass
class OneOfPdnTypeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPdnTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultPdnTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class CommonCellularProfileInfoDef:
    apn: OneOfApnOptionsDef
    authentication: Optional[Union[Authentication1, Authentication2]] = _field(default=None)
    pdn_type: Optional[
        Union[OneOfPdnTypeOptionsDef1, OneOfPdnTypeOptionsDef2, OneOfPdnTypeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "pdnType"})


@dataclass
class ESimCellularSlotConfigDef:
    account_info: ESimAccountInfoDef = _field(metadata={"alias": "accountInfo"})
    attach_profile_config: CommonCellularProfileInfoDef = _field(
        metadata={"alias": "attachProfileConfig"}
    )
    data_profile_config: Optional[CommonCellularProfileInfoDef] = _field(
        default=None, metadata={"alias": "dataProfileConfig"}
    )


@dataclass
class SlotConfigDef:
    """
    Set the slot specific eSim cellular configuration
    """

    slot0_config: ESimCellularSlotConfigDef = _field(metadata={"alias": "slot0Config"})


@dataclass
class EsimcellularData:
    # Set the slot specific eSim cellular configuration
    slot_config: SlotConfigDef = _field(metadata={"alias": "slotConfig"})
    wan_config: Optional[Union[WanConfigOptionTypesDef1, WanConfigOptionTypesDef2]] = _field(
        default=None, metadata={"alias": "wanConfig"}
    )


@dataclass
class Payload:
    """
    eSim Cellular profile feature schema for POST request
    """

    data: EsimcellularData
    name: str
    # Set the eSim Cellular profile feature description
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
    # eSim Cellular profile feature schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListMobilityGlobalEsimcellularPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateEsimCellularProfileFeatureForMobilityPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GlobalEsimcellularData:
    # Set the slot specific eSim cellular configuration
    slot_config: SlotConfigDef = _field(metadata={"alias": "slotConfig"})
    wan_config: Optional[Union[WanConfigOptionTypesDef1, WanConfigOptionTypesDef2]] = _field(
        default=None, metadata={"alias": "wanConfig"}
    )


@dataclass
class CreateEsimCellularProfileFeatureForMobilityPostRequest:
    """
    eSim Cellular profile feature schema for POST request
    """

    data: GlobalEsimcellularData
    name: str
    # Set the eSim Cellular profile feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EsimcellularWanConfigOptionTypesDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EsimcellularWanConfigDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EsimcellularESimAccountInfoDef:
    # Set provider account Id used for this configuration
    account_id: AccountId = _field(metadata={"alias": "accountId"})
    # Set communication plan used for this configuration
    comm_plan: CommPlan = _field(metadata={"alias": "commPlan"})
    # Set rate plan used for this configuration
    rate_plan: RatePlan = _field(metadata={"alias": "ratePlan"})


@dataclass
class EsimcellularOneOfApnOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EsimcellularOneOfDefaultAuthenticationOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EsimcellularDefaultAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EsimcellularAuthentication1:
    no_authentication: EsimcellularOneOfDefaultAuthenticationOptionsDef = _field(
        metadata={"alias": "noAuthentication"}
    )


@dataclass
class EsimcellularOneOfAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EsimcellularAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EsimcellularOneOfUsernameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EsimcellularOneOfPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EsimcellularNeedAuthentication:
    password: Union[EsimcellularOneOfPasswordOptionsDef1, OneOfPasswordOptionsDef2]
    type_: Union[EsimcellularOneOfAuthenticationOptionsDef1, OneOfAuthenticationOptionsDef2] = (
        _field(metadata={"alias": "type"})
    )
    username: Union[EsimcellularOneOfUsernameOptionsDef1, OneOfUsernameOptionsDef2]


@dataclass
class EsimcellularAuthentication2:
    need_authentication: EsimcellularNeedAuthentication = _field(
        metadata={"alias": "needAuthentication"}
    )


@dataclass
class EsimcellularOneOfPdnTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EsimcellularPdnTypeDef


@dataclass
class EsimcellularOneOfPdnTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EsimcellularDefaultPdnTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EsimcellularCommonCellularProfileInfoDef:
    apn: EsimcellularOneOfApnOptionsDef
    authentication: Optional[Union[EsimcellularAuthentication1, EsimcellularAuthentication2]] = (
        _field(default=None)
    )
    pdn_type: Optional[
        Union[
            EsimcellularOneOfPdnTypeOptionsDef1,
            OneOfPdnTypeOptionsDef2,
            EsimcellularOneOfPdnTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "pdnType"})


@dataclass
class GlobalEsimcellularOneOfApnOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalEsimcellularOneOfDefaultAuthenticationOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalEsimcellularDefaultAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class GlobalEsimcellularAuthentication1:
    no_authentication: GlobalEsimcellularOneOfDefaultAuthenticationOptionsDef = _field(
        metadata={"alias": "noAuthentication"}
    )


@dataclass
class GlobalEsimcellularOneOfAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalEsimcellularAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class GlobalEsimcellularOneOfUsernameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalEsimcellularOneOfPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalEsimcellularNeedAuthentication:
    password: Union[GlobalEsimcellularOneOfPasswordOptionsDef1, OneOfPasswordOptionsDef2]
    type_: Union[
        GlobalEsimcellularOneOfAuthenticationOptionsDef1, OneOfAuthenticationOptionsDef2
    ] = _field(metadata={"alias": "type"})
    username: Union[GlobalEsimcellularOneOfUsernameOptionsDef1, OneOfUsernameOptionsDef2]


@dataclass
class GlobalEsimcellularAuthentication2:
    need_authentication: GlobalEsimcellularNeedAuthentication = _field(
        metadata={"alias": "needAuthentication"}
    )


@dataclass
class GlobalEsimcellularOneOfPdnTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalEsimcellularPdnTypeDef


@dataclass
class GlobalEsimcellularOneOfPdnTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalEsimcellularDefaultPdnTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class GlobalEsimcellularCommonCellularProfileInfoDef:
    apn: GlobalEsimcellularOneOfApnOptionsDef
    authentication: Optional[
        Union[GlobalEsimcellularAuthentication1, GlobalEsimcellularAuthentication2]
    ] = _field(default=None)
    pdn_type: Optional[
        Union[
            GlobalEsimcellularOneOfPdnTypeOptionsDef1,
            OneOfPdnTypeOptionsDef2,
            GlobalEsimcellularOneOfPdnTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "pdnType"})


@dataclass
class EsimcellularESimCellularSlotConfigDef:
    account_info: EsimcellularESimAccountInfoDef = _field(metadata={"alias": "accountInfo"})
    attach_profile_config: EsimcellularCommonCellularProfileInfoDef = _field(
        metadata={"alias": "attachProfileConfig"}
    )
    data_profile_config: Optional[GlobalEsimcellularCommonCellularProfileInfoDef] = _field(
        default=None, metadata={"alias": "dataProfileConfig"}
    )


@dataclass
class EsimcellularSlotConfigDef:
    """
    Set the slot specific eSim cellular configuration
    """

    slot0_config: EsimcellularESimCellularSlotConfigDef = _field(metadata={"alias": "slot0Config"})


@dataclass
class MobilityGlobalEsimcellularData:
    # Set the slot specific eSim cellular configuration
    slot_config: EsimcellularSlotConfigDef = _field(metadata={"alias": "slotConfig"})
    wan_config: Optional[Union[EsimcellularWanConfigOptionTypesDef1, WanConfigOptionTypesDef2]] = (
        _field(default=None, metadata={"alias": "wanConfig"})
    )


@dataclass
class EsimcellularPayload:
    """
    eSim Cellular profile feature schema for PUT request
    """

    data: MobilityGlobalEsimcellularData
    name: str
    # Set the eSim Cellular profile feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleMobilityGlobalEsimcellularPayload:
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
    # eSim Cellular profile feature schema for PUT request
    payload: Optional[EsimcellularPayload] = _field(default=None)


@dataclass
class EditEsimCellularProfileFeatureForMobilityPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GlobalEsimcellularWanConfigOptionTypesDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalEsimcellularWanConfigDef  # pytype: disable=annotation-type-mismatch


@dataclass
class GlobalEsimcellularESimAccountInfoDef:
    # Set provider account Id used for this configuration
    account_id: AccountId = _field(metadata={"alias": "accountId"})
    # Set communication plan used for this configuration
    comm_plan: CommPlan = _field(metadata={"alias": "commPlan"})
    # Set rate plan used for this configuration
    rate_plan: RatePlan = _field(metadata={"alias": "ratePlan"})


@dataclass
class MobilityGlobalEsimcellularOneOfApnOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class MobilityGlobalEsimcellularOneOfDefaultAuthenticationOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: MobilityGlobalEsimcellularDefaultAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class MobilityGlobalEsimcellularAuthentication1:
    no_authentication: MobilityGlobalEsimcellularOneOfDefaultAuthenticationOptionsDef = _field(
        metadata={"alias": "noAuthentication"}
    )


@dataclass
class MobilityGlobalEsimcellularOneOfAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: MobilityGlobalEsimcellularAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class MobilityGlobalEsimcellularOneOfUsernameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class MobilityGlobalEsimcellularOneOfPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class MobilityGlobalEsimcellularNeedAuthentication:
    password: Union[MobilityGlobalEsimcellularOneOfPasswordOptionsDef1, OneOfPasswordOptionsDef2]
    type_: Union[
        MobilityGlobalEsimcellularOneOfAuthenticationOptionsDef1, OneOfAuthenticationOptionsDef2
    ] = _field(metadata={"alias": "type"})
    username: Union[MobilityGlobalEsimcellularOneOfUsernameOptionsDef1, OneOfUsernameOptionsDef2]


@dataclass
class MobilityGlobalEsimcellularAuthentication2:
    need_authentication: MobilityGlobalEsimcellularNeedAuthentication = _field(
        metadata={"alias": "needAuthentication"}
    )


@dataclass
class MobilityGlobalEsimcellularOneOfPdnTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: MobilityGlobalEsimcellularPdnTypeDef


@dataclass
class MobilityGlobalEsimcellularOneOfPdnTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: MobilityGlobalEsimcellularDefaultPdnTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class MobilityGlobalEsimcellularCommonCellularProfileInfoDef:
    apn: MobilityGlobalEsimcellularOneOfApnOptionsDef
    authentication: Optional[
        Union[MobilityGlobalEsimcellularAuthentication1, MobilityGlobalEsimcellularAuthentication2]
    ] = _field(default=None)
    pdn_type: Optional[
        Union[
            MobilityGlobalEsimcellularOneOfPdnTypeOptionsDef1,
            OneOfPdnTypeOptionsDef2,
            MobilityGlobalEsimcellularOneOfPdnTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "pdnType"})


@dataclass
class FeatureProfileMobilityGlobalEsimcellularOneOfApnOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileMobilityGlobalEsimcellularOneOfDefaultAuthenticationOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileMobilityGlobalEsimcellularDefaultAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileMobilityGlobalEsimcellularAuthentication1:
    no_authentication: FeatureProfileMobilityGlobalEsimcellularOneOfDefaultAuthenticationOptionsDef = _field(
        metadata={"alias": "noAuthentication"}
    )


@dataclass
class FeatureProfileMobilityGlobalEsimcellularOneOfAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileMobilityGlobalEsimcellularAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileMobilityGlobalEsimcellularOneOfUsernameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileMobilityGlobalEsimcellularOneOfPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileMobilityGlobalEsimcellularNeedAuthentication:
    password: Union[
        FeatureProfileMobilityGlobalEsimcellularOneOfPasswordOptionsDef1, OneOfPasswordOptionsDef2
    ]
    type_: Union[
        FeatureProfileMobilityGlobalEsimcellularOneOfAuthenticationOptionsDef1,
        OneOfAuthenticationOptionsDef2,
    ] = _field(metadata={"alias": "type"})
    username: Union[
        FeatureProfileMobilityGlobalEsimcellularOneOfUsernameOptionsDef1, OneOfUsernameOptionsDef2
    ]


@dataclass
class FeatureProfileMobilityGlobalEsimcellularAuthentication2:
    need_authentication: FeatureProfileMobilityGlobalEsimcellularNeedAuthentication = _field(
        metadata={"alias": "needAuthentication"}
    )


@dataclass
class FeatureProfileMobilityGlobalEsimcellularOneOfPdnTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileMobilityGlobalEsimcellularPdnTypeDef


@dataclass
class FeatureProfileMobilityGlobalEsimcellularOneOfPdnTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileMobilityGlobalEsimcellularDefaultPdnTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileMobilityGlobalEsimcellularCommonCellularProfileInfoDef:
    apn: FeatureProfileMobilityGlobalEsimcellularOneOfApnOptionsDef
    authentication: Optional[
        Union[
            FeatureProfileMobilityGlobalEsimcellularAuthentication1,
            FeatureProfileMobilityGlobalEsimcellularAuthentication2,
        ]
    ] = _field(default=None)
    pdn_type: Optional[
        Union[
            FeatureProfileMobilityGlobalEsimcellularOneOfPdnTypeOptionsDef1,
            OneOfPdnTypeOptionsDef2,
            FeatureProfileMobilityGlobalEsimcellularOneOfPdnTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "pdnType"})


@dataclass
class GlobalEsimcellularESimCellularSlotConfigDef:
    account_info: GlobalEsimcellularESimAccountInfoDef = _field(metadata={"alias": "accountInfo"})
    attach_profile_config: MobilityGlobalEsimcellularCommonCellularProfileInfoDef = _field(
        metadata={"alias": "attachProfileConfig"}
    )
    data_profile_config: Optional[
        FeatureProfileMobilityGlobalEsimcellularCommonCellularProfileInfoDef
    ] = _field(default=None, metadata={"alias": "dataProfileConfig"})


@dataclass
class GlobalEsimcellularSlotConfigDef:
    """
    Set the slot specific eSim cellular configuration
    """

    slot0_config: GlobalEsimcellularESimCellularSlotConfigDef = _field(
        metadata={"alias": "slot0Config"}
    )


@dataclass
class FeatureProfileMobilityGlobalEsimcellularData:
    # Set the slot specific eSim cellular configuration
    slot_config: GlobalEsimcellularSlotConfigDef = _field(metadata={"alias": "slotConfig"})
    wan_config: Optional[
        Union[GlobalEsimcellularWanConfigOptionTypesDef1, WanConfigOptionTypesDef2]
    ] = _field(default=None, metadata={"alias": "wanConfig"})


@dataclass
class EditEsimCellularProfileFeatureForMobilityPutRequest:
    """
    eSim Cellular profile feature schema for PUT request
    """

    data: FeatureProfileMobilityGlobalEsimcellularData
    name: str
    # Set the eSim Cellular profile feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
