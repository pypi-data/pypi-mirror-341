# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]


@dataclass
class DnsData:
    target_vpns: Optional[Any] = _field(default=None, metadata={"alias": "targetVpns"})


@dataclass
class Payload1:
    data: DnsData
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


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
class BooleanDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDnsServerIpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfChildOrgIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # can be empty string
    value: str


@dataclass
class VpnsObjDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfUidOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # An Integer and cannot be empty string
    value: str


@dataclass
class TargetVpns:
    local_domain_bypass_enabled: BooleanDef = _field(metadata={"alias": "localDomainBypassEnabled"})
    uid: OneOfUidOptionsDef
    umbrella_default: BooleanDef = _field(metadata={"alias": "umbrellaDefault"})
    vpns: VpnsObjDef
    dns_server_ip: Optional[OneOfDnsServerIpOptionsDef] = _field(
        default=None, metadata={"alias": "dnsServerIP"}
    )


@dataclass
class DnsSecurityDnsData:
    dns_crypt: BooleanDef = _field(metadata={"alias": "dnsCrypt"})
    match_all_vpn: BooleanDef = _field(metadata={"alias": "matchAllVpn"})
    child_org_id: Optional[OneOfChildOrgIdOptionsDef] = _field(
        default=None, metadata={"alias": "childOrgId"}
    )
    dns_server_ip: Optional[OneOfDnsServerIpOptionsDef] = _field(
        default=None, metadata={"alias": "dnsServerIP"}
    )
    local_domain_bypass_enabled: Optional[BooleanDef] = _field(
        default=None, metadata={"alias": "localDomainBypassEnabled"}
    )
    local_domain_bypass_list: Optional[ReferenceDef] = _field(
        default=None, metadata={"alias": "localDomainBypassList"}
    )
    # Will be under data field only if matchAllVpn is false, if matchAllVpn is true field should not be in payload
    target_vpns: Optional[List[TargetVpns]] = _field(default=None, metadata={"alias": "targetVpns"})
    umbrella_default: Optional[BooleanDef] = _field(
        default=None, metadata={"alias": "umbrellaDefault"}
    )


@dataclass
class Payload2:
    data: DnsSecurityDnsData
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
    # dns profile parcel schema for POST request
    payload: Optional[Union[Payload1, Payload2]] = _field(default=None)


@dataclass
class GetListSdwanDnsSecurityDnsPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSigSecurityProfileParcelPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanDnsSecurityDnsData:
    target_vpns: Optional[Any] = _field(default=None, metadata={"alias": "targetVpns"})


@dataclass
class CreateSigSecurityProfileParcelPostRequest1:
    data: SdwanDnsSecurityDnsData
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class FeatureProfileSdwanDnsSecurityDnsData:
    dns_crypt: BooleanDef = _field(metadata={"alias": "dnsCrypt"})
    match_all_vpn: BooleanDef = _field(metadata={"alias": "matchAllVpn"})
    child_org_id: Optional[OneOfChildOrgIdOptionsDef] = _field(
        default=None, metadata={"alias": "childOrgId"}
    )
    dns_server_ip: Optional[OneOfDnsServerIpOptionsDef] = _field(
        default=None, metadata={"alias": "dnsServerIP"}
    )
    local_domain_bypass_enabled: Optional[BooleanDef] = _field(
        default=None, metadata={"alias": "localDomainBypassEnabled"}
    )
    local_domain_bypass_list: Optional[ReferenceDef] = _field(
        default=None, metadata={"alias": "localDomainBypassList"}
    )
    # Will be under data field only if matchAllVpn is false, if matchAllVpn is true field should not be in payload
    target_vpns: Optional[List[TargetVpns]] = _field(default=None, metadata={"alias": "targetVpns"})
    umbrella_default: Optional[BooleanDef] = _field(
        default=None, metadata={"alias": "umbrellaDefault"}
    )


@dataclass
class CreateSigSecurityProfileParcelPostRequest2:
    data: FeatureProfileSdwanDnsSecurityDnsData
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class V1FeatureProfileSdwanDnsSecurityDnsData:
    target_vpns: Optional[Any] = _field(default=None, metadata={"alias": "targetVpns"})


@dataclass
class DnsPayload1:
    data: V1FeatureProfileSdwanDnsSecurityDnsData
    description: str
    name: str
    cg_fp_pp_name_def: Optional[str] = _field(default=None, metadata={"alias": "cgFpPpNameDef"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class DnsRefIdDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class DnsReferenceDef:
    ref_id: DnsRefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class DnsOneOfChildOrgIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # can be empty string
    value: str


@dataclass
class DnsOneOfUidOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # An Integer and cannot be empty string
    value: str


@dataclass
class DnsTargetVpns:
    local_domain_bypass_enabled: BooleanDef = _field(metadata={"alias": "localDomainBypassEnabled"})
    uid: DnsOneOfUidOptionsDef
    umbrella_default: BooleanDef = _field(metadata={"alias": "umbrellaDefault"})
    vpns: VpnsObjDef
    dns_server_ip: Optional[OneOfDnsServerIpOptionsDef] = _field(
        default=None, metadata={"alias": "dnsServerIP"}
    )


@dataclass
class Data1:
    dns_crypt: BooleanDef = _field(metadata={"alias": "dnsCrypt"})
    match_all_vpn: BooleanDef = _field(metadata={"alias": "matchAllVpn"})
    child_org_id: Optional[DnsOneOfChildOrgIdOptionsDef] = _field(
        default=None, metadata={"alias": "childOrgId"}
    )
    dns_server_ip: Optional[OneOfDnsServerIpOptionsDef] = _field(
        default=None, metadata={"alias": "dnsServerIP"}
    )
    local_domain_bypass_enabled: Optional[BooleanDef] = _field(
        default=None, metadata={"alias": "localDomainBypassEnabled"}
    )
    local_domain_bypass_list: Optional[DnsReferenceDef] = _field(
        default=None, metadata={"alias": "localDomainBypassList"}
    )
    # Will be under data field only if matchAllVpn is false, if matchAllVpn is true field should not be in payload
    target_vpns: Optional[List[DnsTargetVpns]] = _field(
        default=None, metadata={"alias": "targetVpns"}
    )
    umbrella_default: Optional[BooleanDef] = _field(
        default=None, metadata={"alias": "umbrellaDefault"}
    )


@dataclass
class DnsPayload2:
    data: Data1
    description: str
    name: str
    cg_fp_pp_name_def: Optional[str] = _field(default=None, metadata={"alias": "cgFpPpNameDef"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanDnsSecurityDnsPayload:
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
    # dns profile parcel schema for PUT request
    payload: Optional[Union[DnsPayload1, DnsPayload2]] = _field(default=None)


@dataclass
class EditSigSecurityProfileParcelPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data2:
    target_vpns: Optional[Any] = _field(default=None, metadata={"alias": "targetVpns"})


@dataclass
class EditSigSecurityProfileParcelPutRequest1:
    data: Data2
    description: str
    name: str
    cg_fp_pp_name_def: Optional[str] = _field(default=None, metadata={"alias": "cgFpPpNameDef"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class DnsSecurityDnsRefIdDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class DnsSecurityDnsReferenceDef:
    ref_id: DnsSecurityDnsRefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class DnsSecurityDnsOneOfChildOrgIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # can be empty string
    value: str


@dataclass
class DnsSecurityDnsOneOfUidOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # An Integer and cannot be empty string
    value: str


@dataclass
class DnsSecurityDnsTargetVpns:
    local_domain_bypass_enabled: BooleanDef = _field(metadata={"alias": "localDomainBypassEnabled"})
    uid: DnsSecurityDnsOneOfUidOptionsDef
    umbrella_default: BooleanDef = _field(metadata={"alias": "umbrellaDefault"})
    vpns: VpnsObjDef
    dns_server_ip: Optional[OneOfDnsServerIpOptionsDef] = _field(
        default=None, metadata={"alias": "dnsServerIP"}
    )


@dataclass
class Data3:
    dns_crypt: BooleanDef = _field(metadata={"alias": "dnsCrypt"})
    match_all_vpn: BooleanDef = _field(metadata={"alias": "matchAllVpn"})
    child_org_id: Optional[DnsSecurityDnsOneOfChildOrgIdOptionsDef] = _field(
        default=None, metadata={"alias": "childOrgId"}
    )
    dns_server_ip: Optional[OneOfDnsServerIpOptionsDef] = _field(
        default=None, metadata={"alias": "dnsServerIP"}
    )
    local_domain_bypass_enabled: Optional[BooleanDef] = _field(
        default=None, metadata={"alias": "localDomainBypassEnabled"}
    )
    local_domain_bypass_list: Optional[DnsSecurityDnsReferenceDef] = _field(
        default=None, metadata={"alias": "localDomainBypassList"}
    )
    # Will be under data field only if matchAllVpn is false, if matchAllVpn is true field should not be in payload
    target_vpns: Optional[List[DnsSecurityDnsTargetVpns]] = _field(
        default=None, metadata={"alias": "targetVpns"}
    )
    umbrella_default: Optional[BooleanDef] = _field(
        default=None, metadata={"alias": "umbrellaDefault"}
    )


@dataclass
class EditSigSecurityProfileParcelPutRequest2:
    data: Data3
    description: str
    name: str
    cg_fp_pp_name_def: Optional[str] = _field(default=None, metadata={"alias": "cgFpPpNameDef"})
    metadata: Optional[Any] = _field(default=None)
