# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

ZoneValueStringDef = Literal["default", "self", "untrusted"]

OnStringValueDef = Literal["on"]

SettingsFailureModeDef = Literal["close", "open"]

NetworkSettingsOptionTypeDef = Literal["network-settings"]

VariableOptionTypeDef = Literal["variable"]

ResourceProfileValueDef = Literal["high", "low", "medium"]

PolicyZoneValueStringDef = Literal["default", "self", "untrusted"]

EmbeddedSecurityPolicyZoneValueStringDef = Literal["default", "self", "untrusted"]

SdwanEmbeddedSecurityPolicyZoneValueStringDef = Literal["default", "self", "untrusted"]

FeatureProfileSdwanEmbeddedSecurityPolicyZoneValueStringDef = Literal[
    "default", "self", "untrusted"
]

V1FeatureProfileSdwanEmbeddedSecurityPolicyZoneValueStringDef = Literal[
    "default", "self", "untrusted"
]

ZoneValueStringDef1 = Literal["default", "self", "untrusted"]

PolicyOnStringValueDef = Literal["on"]

EmbeddedSecurityPolicyOnStringValueDef = Literal["on"]

SdwanEmbeddedSecurityPolicyOnStringValueDef = Literal["on"]

FeatureProfileSdwanEmbeddedSecurityPolicyOnStringValueDef = Literal["on"]

PolicySettingsFailureModeDef = Literal["close", "open"]

PolicyResourceProfileValueDef = Literal["high", "low", "medium"]

ZoneValueStringDef2 = Literal["default", "self", "untrusted"]

ZoneValueStringDef3 = Literal["default", "self", "untrusted"]

ZoneValueStringDef4 = Literal["default", "self", "untrusted"]

ZoneValueStringDef5 = Literal["default", "self", "untrusted"]

ZoneValueStringDef6 = Literal["default", "self", "untrusted"]

ZoneValueStringDef7 = Literal["default", "self", "untrusted"]

V1FeatureProfileSdwanEmbeddedSecurityPolicyOnStringValueDef = Literal["on"]

OnStringValueDef1 = Literal["on"]

OnStringValueDef2 = Literal["on"]

OnStringValueDef3 = Literal["on"]

EmbeddedSecurityPolicySettingsFailureModeDef = Literal["close", "open"]

EmbeddedSecurityPolicyResourceProfileValueDef = Literal["high", "low", "medium"]


@dataclass
class RefIdDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef:
    ref_id: RefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class ZoneDef1:
    ref_id: RefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class ZoneDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ZoneValueStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries:
    dst_zone: Union[ZoneDef1, ZoneDef2] = _field(metadata={"alias": "dstZone"})
    src_zone: Union[ZoneDef1, ZoneDef2] = _field(metadata={"alias": "srcZone"})


@dataclass
class NgFirewallDef:
    entries: List[Entries]
    ref_id: RefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class Assembly1:
    ssl_decryption: ReferenceDef = _field(metadata={"alias": "sslDecryption"})
    advanced_inspection_profile: Optional[ReferenceDef] = _field(
        default=None, metadata={"alias": "advancedInspectionProfile"}
    )
    ngfirewall: Optional[NgFirewallDef] = _field(default=None)


@dataclass
class Assembly2:
    ngfirewall: NgFirewallDef
    advanced_inspection_profile: Optional[ReferenceDef] = _field(
        default=None, metadata={"alias": "advancedInspectionProfile"}
    )
    ssl_decryption: Optional[ReferenceDef] = _field(
        default=None, metadata={"alias": "sslDecryption"}
    )


@dataclass
class Assembly3:
    advanced_inspection_profile: ReferenceDef = _field(
        metadata={"alias": "advancedInspectionProfile"}
    )
    ngfirewall: Optional[NgFirewallDef] = _field(default=None)
    ssl_decryption: Optional[ReferenceDef] = _field(
        default=None, metadata={"alias": "sslDecryption"}
    )


@dataclass
class OneOfSettingsTcpSynFloodLimitOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSettingsMaxIncompleteTcpLimitOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSettingsMaxIncompleteUdpLimitOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSettingsMaxIncompleteIcmpLimitOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OnStringDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: OnStringValueDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSettingsFailureModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SettingsFailureModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class NetworkSettingsOptionTypeObjectDef:
    option_type: NetworkSettingsOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Settings:
    audit_trail: Optional[OnStringDef] = _field(default=None, metadata={"alias": "auditTrail"})
    failure_mode: Optional[OneOfSettingsFailureModeOptionsDef] = _field(
        default=None, metadata={"alias": "failureMode"}
    )
    icmp_unreachable_allow: Optional[OnStringDef] = _field(
        default=None, metadata={"alias": "icmpUnreachableAllow"}
    )
    max_incomplete_icmp_limit: Optional[OneOfSettingsMaxIncompleteIcmpLimitOptionsDef] = _field(
        default=None, metadata={"alias": "maxIncompleteIcmpLimit"}
    )
    max_incomplete_tcp_limit: Optional[OneOfSettingsMaxIncompleteTcpLimitOptionsDef] = _field(
        default=None, metadata={"alias": "maxIncompleteTcpLimit"}
    )
    max_incomplete_udp_limit: Optional[OneOfSettingsMaxIncompleteUdpLimitOptionsDef] = _field(
        default=None, metadata={"alias": "maxIncompleteUdpLimit"}
    )
    security_logging: Optional[NetworkSettingsOptionTypeObjectDef] = _field(
        default=None, metadata={"alias": "securityLogging"}
    )
    session_reclassify_allow: Optional[OnStringDef] = _field(
        default=None, metadata={"alias": "sessionReclassifyAllow"}
    )
    tcp_syn_flood_limit: Optional[OneOfSettingsTcpSynFloodLimitOptionsDef] = _field(
        default=None, metadata={"alias": "tcpSynFloodLimit"}
    )
    unified_logging: Optional[OnStringDef] = _field(
        default=None, metadata={"alias": "unifiedLogging"}
    )


@dataclass
class OneOfAppHostingNatOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAppHostingNatOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAppHostingDataBaseUrlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAppHostingDataBaseUrlOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAppHostingResourceProfileOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ResourceProfileValueDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAppHostingResourceProfileOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class AppHosting:
    database_url: Union[
        OneOfAppHostingDataBaseUrlOptionsDef1, OneOfAppHostingDataBaseUrlOptionsDef2
    ] = _field(metadata={"alias": "databaseUrl"})
    nat: Union[OneOfAppHostingNatOptionsDef1, OneOfAppHostingNatOptionsDef2]
    resource_profile: Union[
        OneOfAppHostingResourceProfileOptionsDef1, OneOfAppHostingResourceProfileOptionsDef2
    ] = _field(metadata={"alias": "resourceProfile"})


@dataclass
class PolicyData:
    assembly: List[Union[Assembly1, Assembly2, Assembly3]]
    app_hosting: Optional[AppHosting] = _field(default=None, metadata={"alias": "appHosting"})
    settings: Optional[Settings] = _field(default=None)


@dataclass
class Payload:
    """
    Policy profile Feature schema for POST request
    """

    data: PolicyData
    description: str
    name: str
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
    # Policy profile Feature schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanEmbeddedSecurityPolicyPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateEmbeddedSecurityProfileParcelPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EmbeddedSecurityPolicyData:
    assembly: List[Union[Assembly1, Assembly2, Assembly3]]
    app_hosting: Optional[AppHosting] = _field(default=None, metadata={"alias": "appHosting"})
    settings: Optional[Settings] = _field(default=None)


@dataclass
class CreateEmbeddedSecurityProfileParcelPostRequest:
    """
    Policy profile Feature schema for POST request
    """

    data: EmbeddedSecurityPolicyData
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyRefIdDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyReferenceDef:
    ref_id: PolicyRefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class EmbeddedSecurityPolicyRefIdDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EmbeddedSecurityPolicyReferenceDef:
    ref_id: EmbeddedSecurityPolicyRefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class SdwanEmbeddedSecurityPolicyRefIdDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanEmbeddedSecurityPolicyRefIdDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyZoneDef1:
    ref_id: FeatureProfileSdwanEmbeddedSecurityPolicyRefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class PolicyZoneDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyZoneValueStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class V1FeatureProfileSdwanEmbeddedSecurityPolicyRefIdDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EmbeddedSecurityPolicyZoneDef1:
    ref_id: V1FeatureProfileSdwanEmbeddedSecurityPolicyRefIdDef = _field(
        metadata={"alias": "refId"}
    )


@dataclass
class EmbeddedSecurityPolicyZoneDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EmbeddedSecurityPolicyZoneValueStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyEntries:
    dst_zone: Union[EmbeddedSecurityPolicyZoneDef1, EmbeddedSecurityPolicyZoneDef2] = _field(
        metadata={"alias": "dstZone"}
    )
    src_zone: Union[PolicyZoneDef1, PolicyZoneDef2] = _field(metadata={"alias": "srcZone"})


@dataclass
class PolicyNgFirewallDef:
    entries: List[PolicyEntries]
    ref_id: SdwanEmbeddedSecurityPolicyRefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class PolicyAssembly1:
    ssl_decryption: EmbeddedSecurityPolicyReferenceDef = _field(metadata={"alias": "sslDecryption"})
    advanced_inspection_profile: Optional[PolicyReferenceDef] = _field(
        default=None, metadata={"alias": "advancedInspectionProfile"}
    )
    ngfirewall: Optional[PolicyNgFirewallDef] = _field(default=None)


@dataclass
class RefIdDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanEmbeddedSecurityPolicyReferenceDef:
    ref_id: RefIdDef1 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanEmbeddedSecurityPolicyReferenceDef:
    ref_id: RefIdDef2 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef3:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RefIdDef4:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanEmbeddedSecurityPolicyZoneDef1:
    ref_id: RefIdDef4 = _field(metadata={"alias": "refId"})


@dataclass
class SdwanEmbeddedSecurityPolicyZoneDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanEmbeddedSecurityPolicyZoneValueStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class RefIdDef5:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanEmbeddedSecurityPolicyZoneDef1:
    ref_id: RefIdDef5 = _field(metadata={"alias": "refId"})


@dataclass
class FeatureProfileSdwanEmbeddedSecurityPolicyZoneDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileSdwanEmbeddedSecurityPolicyZoneValueStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EmbeddedSecurityPolicyEntries:
    dst_zone: Union[
        FeatureProfileSdwanEmbeddedSecurityPolicyZoneDef1,
        FeatureProfileSdwanEmbeddedSecurityPolicyZoneDef2,
    ] = _field(metadata={"alias": "dstZone"})
    src_zone: Union[SdwanEmbeddedSecurityPolicyZoneDef1, SdwanEmbeddedSecurityPolicyZoneDef2] = (
        _field(metadata={"alias": "srcZone"})
    )


@dataclass
class EmbeddedSecurityPolicyNgFirewallDef:
    entries: List[EmbeddedSecurityPolicyEntries]
    ref_id: RefIdDef3 = _field(metadata={"alias": "refId"})


@dataclass
class PolicyAssembly2:
    ngfirewall: EmbeddedSecurityPolicyNgFirewallDef
    advanced_inspection_profile: Optional[SdwanEmbeddedSecurityPolicyReferenceDef] = _field(
        default=None, metadata={"alias": "advancedInspectionProfile"}
    )
    ssl_decryption: Optional[FeatureProfileSdwanEmbeddedSecurityPolicyReferenceDef] = _field(
        default=None, metadata={"alias": "sslDecryption"}
    )


@dataclass
class RefIdDef6:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class V1FeatureProfileSdwanEmbeddedSecurityPolicyReferenceDef:
    ref_id: RefIdDef6 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef7:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef1:
    ref_id: RefIdDef7 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef8:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RefIdDef9:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class V1FeatureProfileSdwanEmbeddedSecurityPolicyZoneDef1:
    ref_id: RefIdDef9 = _field(metadata={"alias": "refId"})


@dataclass
class V1FeatureProfileSdwanEmbeddedSecurityPolicyZoneDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: V1FeatureProfileSdwanEmbeddedSecurityPolicyZoneValueStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class RefIdDef10:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ZoneDef11:
    ref_id: RefIdDef10 = _field(metadata={"alias": "refId"})


@dataclass
class ZoneDef21:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ZoneValueStringDef1  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanEmbeddedSecurityPolicyEntries:
    dst_zone: Union[ZoneDef11, ZoneDef21] = _field(metadata={"alias": "dstZone"})
    src_zone: Union[
        V1FeatureProfileSdwanEmbeddedSecurityPolicyZoneDef1,
        V1FeatureProfileSdwanEmbeddedSecurityPolicyZoneDef2,
    ] = _field(metadata={"alias": "srcZone"})


@dataclass
class SdwanEmbeddedSecurityPolicyNgFirewallDef:
    entries: List[SdwanEmbeddedSecurityPolicyEntries]
    ref_id: RefIdDef8 = _field(metadata={"alias": "refId"})


@dataclass
class PolicyAssembly3:
    advanced_inspection_profile: V1FeatureProfileSdwanEmbeddedSecurityPolicyReferenceDef = _field(
        metadata={"alias": "advancedInspectionProfile"}
    )
    ngfirewall: Optional[SdwanEmbeddedSecurityPolicyNgFirewallDef] = _field(default=None)
    ssl_decryption: Optional[ReferenceDef1] = _field(
        default=None, metadata={"alias": "sslDecryption"}
    )


@dataclass
class PolicyOneOfSettingsTcpSynFloodLimitOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyOneOfSettingsMaxIncompleteTcpLimitOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyOneOfSettingsMaxIncompleteUdpLimitOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyOneOfSettingsMaxIncompleteIcmpLimitOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyOnStringDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyOnStringValueDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EmbeddedSecurityPolicyOnStringDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EmbeddedSecurityPolicyOnStringValueDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanEmbeddedSecurityPolicyOnStringDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanEmbeddedSecurityPolicyOnStringValueDef  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileSdwanEmbeddedSecurityPolicyOnStringDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileSdwanEmbeddedSecurityPolicyOnStringValueDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyOneOfSettingsFailureModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicySettingsFailureModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicySettings:
    audit_trail: Optional[PolicyOnStringDef] = _field(
        default=None, metadata={"alias": "auditTrail"}
    )
    failure_mode: Optional[PolicyOneOfSettingsFailureModeOptionsDef] = _field(
        default=None, metadata={"alias": "failureMode"}
    )
    icmp_unreachable_allow: Optional[FeatureProfileSdwanEmbeddedSecurityPolicyOnStringDef] = _field(
        default=None, metadata={"alias": "icmpUnreachableAllow"}
    )
    max_incomplete_icmp_limit: Optional[PolicyOneOfSettingsMaxIncompleteIcmpLimitOptionsDef] = (
        _field(default=None, metadata={"alias": "maxIncompleteIcmpLimit"})
    )
    max_incomplete_tcp_limit: Optional[PolicyOneOfSettingsMaxIncompleteTcpLimitOptionsDef] = _field(
        default=None, metadata={"alias": "maxIncompleteTcpLimit"}
    )
    max_incomplete_udp_limit: Optional[PolicyOneOfSettingsMaxIncompleteUdpLimitOptionsDef] = _field(
        default=None, metadata={"alias": "maxIncompleteUdpLimit"}
    )
    security_logging: Optional[NetworkSettingsOptionTypeObjectDef] = _field(
        default=None, metadata={"alias": "securityLogging"}
    )
    session_reclassify_allow: Optional[SdwanEmbeddedSecurityPolicyOnStringDef] = _field(
        default=None, metadata={"alias": "sessionReclassifyAllow"}
    )
    tcp_syn_flood_limit: Optional[PolicyOneOfSettingsTcpSynFloodLimitOptionsDef] = _field(
        default=None, metadata={"alias": "tcpSynFloodLimit"}
    )
    unified_logging: Optional[EmbeddedSecurityPolicyOnStringDef] = _field(
        default=None, metadata={"alias": "unifiedLogging"}
    )


@dataclass
class PolicyOneOfAppHostingResourceProfileOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyResourceProfileValueDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyAppHosting:
    database_url: Union[
        OneOfAppHostingDataBaseUrlOptionsDef1, OneOfAppHostingDataBaseUrlOptionsDef2
    ] = _field(metadata={"alias": "databaseUrl"})
    nat: Union[OneOfAppHostingNatOptionsDef1, OneOfAppHostingNatOptionsDef2]
    resource_profile: Union[
        PolicyOneOfAppHostingResourceProfileOptionsDef1, OneOfAppHostingResourceProfileOptionsDef2
    ] = _field(metadata={"alias": "resourceProfile"})


@dataclass
class SdwanEmbeddedSecurityPolicyData:
    assembly: List[Union[PolicyAssembly1, PolicyAssembly2, PolicyAssembly3]]
    app_hosting: Optional[PolicyAppHosting] = _field(default=None, metadata={"alias": "appHosting"})
    settings: Optional[PolicySettings] = _field(default=None)


@dataclass
class PolicyPayload:
    """
    Policy profile Feature schema for PUT request
    """

    data: SdwanEmbeddedSecurityPolicyData
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanEmbeddedSecurityPolicyPayload:
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
    # Policy profile Feature schema for PUT request
    payload: Optional[PolicyPayload] = _field(default=None)


@dataclass
class EditSecurityProfileParcelPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class RefIdDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef2:
    ref_id: RefIdDef11 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef12:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef3:
    ref_id: RefIdDef12 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef13:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RefIdDef14:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ZoneDef12:
    ref_id: RefIdDef14 = _field(metadata={"alias": "refId"})


@dataclass
class ZoneDef22:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ZoneValueStringDef2  # pytype: disable=annotation-type-mismatch


@dataclass
class RefIdDef15:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ZoneDef13:
    ref_id: RefIdDef15 = _field(metadata={"alias": "refId"})


@dataclass
class ZoneDef23:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ZoneValueStringDef3  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileSdwanEmbeddedSecurityPolicyEntries:
    dst_zone: Union[ZoneDef13, ZoneDef23] = _field(metadata={"alias": "dstZone"})
    src_zone: Union[ZoneDef12, ZoneDef22] = _field(metadata={"alias": "srcZone"})


@dataclass
class FeatureProfileSdwanEmbeddedSecurityPolicyNgFirewallDef:
    entries: List[FeatureProfileSdwanEmbeddedSecurityPolicyEntries]
    ref_id: RefIdDef13 = _field(metadata={"alias": "refId"})


@dataclass
class EmbeddedSecurityPolicyAssembly1:
    ssl_decryption: ReferenceDef3 = _field(metadata={"alias": "sslDecryption"})
    advanced_inspection_profile: Optional[ReferenceDef2] = _field(
        default=None, metadata={"alias": "advancedInspectionProfile"}
    )
    ngfirewall: Optional[FeatureProfileSdwanEmbeddedSecurityPolicyNgFirewallDef] = _field(
        default=None
    )


@dataclass
class RefIdDef16:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef4:
    ref_id: RefIdDef16 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef17:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef5:
    ref_id: RefIdDef17 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef18:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RefIdDef19:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ZoneDef14:
    ref_id: RefIdDef19 = _field(metadata={"alias": "refId"})


@dataclass
class ZoneDef24:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ZoneValueStringDef4  # pytype: disable=annotation-type-mismatch


@dataclass
class RefIdDef20:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ZoneDef15:
    ref_id: RefIdDef20 = _field(metadata={"alias": "refId"})


@dataclass
class ZoneDef25:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ZoneValueStringDef5  # pytype: disable=annotation-type-mismatch


@dataclass
class V1FeatureProfileSdwanEmbeddedSecurityPolicyEntries:
    dst_zone: Union[ZoneDef15, ZoneDef25] = _field(metadata={"alias": "dstZone"})
    src_zone: Union[ZoneDef14, ZoneDef24] = _field(metadata={"alias": "srcZone"})


@dataclass
class V1FeatureProfileSdwanEmbeddedSecurityPolicyNgFirewallDef:
    entries: List[V1FeatureProfileSdwanEmbeddedSecurityPolicyEntries]
    ref_id: RefIdDef18 = _field(metadata={"alias": "refId"})


@dataclass
class EmbeddedSecurityPolicyAssembly2:
    ngfirewall: V1FeatureProfileSdwanEmbeddedSecurityPolicyNgFirewallDef
    advanced_inspection_profile: Optional[ReferenceDef4] = _field(
        default=None, metadata={"alias": "advancedInspectionProfile"}
    )
    ssl_decryption: Optional[ReferenceDef5] = _field(
        default=None, metadata={"alias": "sslDecryption"}
    )


@dataclass
class RefIdDef21:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef6:
    ref_id: RefIdDef21 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef22:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef7:
    ref_id: RefIdDef22 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef23:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RefIdDef24:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ZoneDef16:
    ref_id: RefIdDef24 = _field(metadata={"alias": "refId"})


@dataclass
class ZoneDef26:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ZoneValueStringDef6  # pytype: disable=annotation-type-mismatch


@dataclass
class RefIdDef25:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ZoneDef17:
    ref_id: RefIdDef25 = _field(metadata={"alias": "refId"})


@dataclass
class ZoneDef27:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ZoneValueStringDef7  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries1:
    dst_zone: Union[ZoneDef17, ZoneDef27] = _field(metadata={"alias": "dstZone"})
    src_zone: Union[ZoneDef16, ZoneDef26] = _field(metadata={"alias": "srcZone"})


@dataclass
class NgFirewallDef1:
    entries: List[Entries1]
    ref_id: RefIdDef23 = _field(metadata={"alias": "refId"})


@dataclass
class EmbeddedSecurityPolicyAssembly3:
    advanced_inspection_profile: ReferenceDef6 = _field(
        metadata={"alias": "advancedInspectionProfile"}
    )
    ngfirewall: Optional[NgFirewallDef1] = _field(default=None)
    ssl_decryption: Optional[ReferenceDef7] = _field(
        default=None, metadata={"alias": "sslDecryption"}
    )


@dataclass
class EmbeddedSecurityPolicyOneOfSettingsTcpSynFloodLimitOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EmbeddedSecurityPolicyOneOfSettingsMaxIncompleteTcpLimitOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EmbeddedSecurityPolicyOneOfSettingsMaxIncompleteUdpLimitOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EmbeddedSecurityPolicyOneOfSettingsMaxIncompleteIcmpLimitOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class V1FeatureProfileSdwanEmbeddedSecurityPolicyOnStringDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: V1FeatureProfileSdwanEmbeddedSecurityPolicyOnStringValueDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OnStringDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: OnStringValueDef1  # pytype: disable=annotation-type-mismatch


@dataclass
class OnStringDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: OnStringValueDef2  # pytype: disable=annotation-type-mismatch


@dataclass
class OnStringDef3:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: OnStringValueDef3  # pytype: disable=annotation-type-mismatch


@dataclass
class EmbeddedSecurityPolicyOneOfSettingsFailureModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EmbeddedSecurityPolicySettingsFailureModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EmbeddedSecurityPolicySettings:
    audit_trail: Optional[V1FeatureProfileSdwanEmbeddedSecurityPolicyOnStringDef] = _field(
        default=None, metadata={"alias": "auditTrail"}
    )
    failure_mode: Optional[EmbeddedSecurityPolicyOneOfSettingsFailureModeOptionsDef] = _field(
        default=None, metadata={"alias": "failureMode"}
    )
    icmp_unreachable_allow: Optional[OnStringDef3] = _field(
        default=None, metadata={"alias": "icmpUnreachableAllow"}
    )
    max_incomplete_icmp_limit: Optional[
        EmbeddedSecurityPolicyOneOfSettingsMaxIncompleteIcmpLimitOptionsDef
    ] = _field(default=None, metadata={"alias": "maxIncompleteIcmpLimit"})
    max_incomplete_tcp_limit: Optional[
        EmbeddedSecurityPolicyOneOfSettingsMaxIncompleteTcpLimitOptionsDef
    ] = _field(default=None, metadata={"alias": "maxIncompleteTcpLimit"})
    max_incomplete_udp_limit: Optional[
        EmbeddedSecurityPolicyOneOfSettingsMaxIncompleteUdpLimitOptionsDef
    ] = _field(default=None, metadata={"alias": "maxIncompleteUdpLimit"})
    security_logging: Optional[NetworkSettingsOptionTypeObjectDef] = _field(
        default=None, metadata={"alias": "securityLogging"}
    )
    session_reclassify_allow: Optional[OnStringDef2] = _field(
        default=None, metadata={"alias": "sessionReclassifyAllow"}
    )
    tcp_syn_flood_limit: Optional[EmbeddedSecurityPolicyOneOfSettingsTcpSynFloodLimitOptionsDef] = (
        _field(default=None, metadata={"alias": "tcpSynFloodLimit"})
    )
    unified_logging: Optional[OnStringDef1] = _field(
        default=None, metadata={"alias": "unifiedLogging"}
    )


@dataclass
class EmbeddedSecurityPolicyOneOfAppHostingResourceProfileOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EmbeddedSecurityPolicyResourceProfileValueDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EmbeddedSecurityPolicyAppHosting:
    database_url: Union[
        OneOfAppHostingDataBaseUrlOptionsDef1, OneOfAppHostingDataBaseUrlOptionsDef2
    ] = _field(metadata={"alias": "databaseUrl"})
    nat: Union[OneOfAppHostingNatOptionsDef1, OneOfAppHostingNatOptionsDef2]
    resource_profile: Union[
        EmbeddedSecurityPolicyOneOfAppHostingResourceProfileOptionsDef1,
        OneOfAppHostingResourceProfileOptionsDef2,
    ] = _field(metadata={"alias": "resourceProfile"})


@dataclass
class FeatureProfileSdwanEmbeddedSecurityPolicyData:
    assembly: List[
        Union[
            EmbeddedSecurityPolicyAssembly1,
            EmbeddedSecurityPolicyAssembly2,
            EmbeddedSecurityPolicyAssembly3,
        ]
    ]
    app_hosting: Optional[EmbeddedSecurityPolicyAppHosting] = _field(
        default=None, metadata={"alias": "appHosting"}
    )
    settings: Optional[EmbeddedSecurityPolicySettings] = _field(default=None)


@dataclass
class EditSecurityProfileParcelPutRequest:
    """
    Policy profile Feature schema for PUT request
    """

    data: FeatureProfileSdwanEmbeddedSecurityPolicyData
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)
