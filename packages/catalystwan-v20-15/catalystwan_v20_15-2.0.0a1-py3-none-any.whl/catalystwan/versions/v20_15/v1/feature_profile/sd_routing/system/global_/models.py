# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

HttpAuthenticationDef = Literal["aaa", "local"]

VersionDef = Literal["2"]

GlobalHttpAuthenticationDef = Literal["aaa", "local"]

GlobalVersionDef = Literal["2"]

SystemGlobalHttpAuthenticationDef = Literal["aaa", "local"]

SystemGlobalVersionDef = Literal["2"]


@dataclass
class OneOfServerDefaultFalseOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfServerDefaultFalseOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServerDefaultFalseOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServerDefaultTrueOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfServerDefaultTrueOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServerDefaultTrueOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfSourceInterfaceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSourceInterfaceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSourceInterfaceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


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
class OneOfNatUdpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNatUdpTimeoutOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatUdpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNatTcpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNatTcpTimeoutOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatTcpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHttpAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: HttpAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfHttpAuthenticationOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHttpAuthenticationOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VersionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVersionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVersionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class ServicesIp:
    services_global_services_ip_arp_proxy: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpArpProxy"})
    services_global_services_ip_cdp: Union[
        OneOfServerDefaultTrueOptionsDef1,
        OneOfServerDefaultTrueOptionsDef2,
        OneOfServerDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpCdp"})
    services_global_services_ip_domain_lookup: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpDomainLookup"})
    services_global_services_ip_ftp_passive: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpFtpPassive"})
    services_global_services_ip_http_server: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpHttpServer"})
    services_global_services_ip_https_server: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpHttpsServer"})
    services_global_services_ip_line_vty: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpLineVty"})
    services_global_services_ip_lldp: Union[
        OneOfServerDefaultTrueOptionsDef1,
        OneOfServerDefaultTrueOptionsDef2,
        OneOfServerDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpLldp"})
    services_global_services_ip_rcmd: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpRcmd"})
    bgp_community_new_format: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bgpCommunityNewFormat"})
    global_other_settings_console_logging: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsConsoleLogging"})
    global_other_settings_ignore_bootp: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsIgnoreBootp"})
    global_other_settings_ip_source_route: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsIPSourceRoute"})
    global_other_settings_snmp_ifindex_persist: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsSnmpIfindexPersist"})
    global_other_settings_tcp_keepalives_in: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsTcpKeepalivesIn"})
    global_other_settings_tcp_keepalives_out: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsTcpKeepalivesOut"})
    global_other_settings_tcp_small_servers: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsTcpSmallServers"})
    global_other_settings_udp_small_servers: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsUdpSmallServers"})
    global_other_settings_vty_line_logging: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsVtyLineLogging"})
    global_settings_http_authentication: Optional[
        Union[
            OneOfHttpAuthenticationOptionsDef1,
            OneOfHttpAuthenticationOptionsDef2,
            OneOfHttpAuthenticationOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalSettingsHttpAuthentication"})
    global_settings_nat64_tcp_timeout: Optional[
        Union[OneOfTcpTimeoutOptionsDef1, OneOfTcpTimeoutOptionsDef2, OneOfTcpTimeoutOptionsDef3]
    ] = _field(default=None, metadata={"alias": "globalSettingsNat64TcpTimeout"})
    global_settings_nat64_udp_timeout: Optional[
        Union[OneOfUdpTimeoutOptionsDef1, OneOfUdpTimeoutOptionsDef2, OneOfUdpTimeoutOptionsDef3]
    ] = _field(default=None, metadata={"alias": "globalSettingsNat64UdpTimeout"})
    global_settings_nat_tcp_timeout: Optional[
        Union[
            OneOfNatTcpTimeoutOptionsDef1,
            OneOfNatTcpTimeoutOptionsDef2,
            OneOfNatTcpTimeoutOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalSettingsNatTcpTimeout"})
    global_settings_nat_udp_timeout: Optional[
        Union[
            OneOfNatUdpTimeoutOptionsDef1,
            OneOfNatUdpTimeoutOptionsDef2,
            OneOfNatUdpTimeoutOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalSettingsNatUdpTimeout"})
    global_settings_ssh_version: Optional[
        Union[OneOfVersionOptionsDef1, OneOfVersionOptionsDef2, OneOfVersionOptionsDef3]
    ] = _field(default=None, metadata={"alias": "globalSettingsSSHVersion"})
    services_global_services_ip_source_intrf: Optional[
        Union[
            OneOfSourceInterfaceOptionsDef1,
            OneOfSourceInterfaceOptionsDef2,
            OneOfSourceInterfaceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "servicesGlobalServicesIpSourceIntrf"})


@dataclass
class ServicesGlobal:
    services_ip: ServicesIp


@dataclass
class GlobalData:
    services_global: ServicesGlobal


@dataclass
class Payload:
    """
    Global settings feature schema for POST request
    """

    data: GlobalData
    name: str
    # Set the feature description
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
    # Global settings feature schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingSystemGlobalPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingGlobalSettingFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemGlobalData:
    services_global: ServicesGlobal


@dataclass
class CreateSdroutingGlobalSettingFeaturePostRequest:
    """
    Global settings feature schema for POST request
    """

    data: SystemGlobalData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GlobalOneOfUdpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalOneOfUdpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalOneOfTcpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalOneOfTcpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalOneOfNatUdpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalOneOfNatUdpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalOneOfNatTcpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalOneOfNatTcpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalOneOfHttpAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalHttpAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class GlobalOneOfVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalVersionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class GlobalServicesIp:
    services_global_services_ip_arp_proxy: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpArpProxy"})
    services_global_services_ip_cdp: Union[
        OneOfServerDefaultTrueOptionsDef1,
        OneOfServerDefaultTrueOptionsDef2,
        OneOfServerDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpCdp"})
    services_global_services_ip_domain_lookup: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpDomainLookup"})
    services_global_services_ip_ftp_passive: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpFtpPassive"})
    services_global_services_ip_http_server: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpHttpServer"})
    services_global_services_ip_https_server: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpHttpsServer"})
    services_global_services_ip_line_vty: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpLineVty"})
    services_global_services_ip_lldp: Union[
        OneOfServerDefaultTrueOptionsDef1,
        OneOfServerDefaultTrueOptionsDef2,
        OneOfServerDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpLldp"})
    services_global_services_ip_rcmd: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpRcmd"})
    bgp_community_new_format: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bgpCommunityNewFormat"})
    global_other_settings_console_logging: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsConsoleLogging"})
    global_other_settings_ignore_bootp: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsIgnoreBootp"})
    global_other_settings_ip_source_route: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsIPSourceRoute"})
    global_other_settings_snmp_ifindex_persist: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsSnmpIfindexPersist"})
    global_other_settings_tcp_keepalives_in: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsTcpKeepalivesIn"})
    global_other_settings_tcp_keepalives_out: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsTcpKeepalivesOut"})
    global_other_settings_tcp_small_servers: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsTcpSmallServers"})
    global_other_settings_udp_small_servers: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsUdpSmallServers"})
    global_other_settings_vty_line_logging: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsVtyLineLogging"})
    global_settings_http_authentication: Optional[
        Union[
            GlobalOneOfHttpAuthenticationOptionsDef1,
            OneOfHttpAuthenticationOptionsDef2,
            OneOfHttpAuthenticationOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalSettingsHttpAuthentication"})
    global_settings_nat64_tcp_timeout: Optional[
        Union[
            GlobalOneOfTcpTimeoutOptionsDef1,
            OneOfTcpTimeoutOptionsDef2,
            GlobalOneOfTcpTimeoutOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalSettingsNat64TcpTimeout"})
    global_settings_nat64_udp_timeout: Optional[
        Union[
            GlobalOneOfUdpTimeoutOptionsDef1,
            OneOfUdpTimeoutOptionsDef2,
            GlobalOneOfUdpTimeoutOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalSettingsNat64UdpTimeout"})
    global_settings_nat_tcp_timeout: Optional[
        Union[
            GlobalOneOfNatTcpTimeoutOptionsDef1,
            OneOfNatTcpTimeoutOptionsDef2,
            GlobalOneOfNatTcpTimeoutOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalSettingsNatTcpTimeout"})
    global_settings_nat_udp_timeout: Optional[
        Union[
            GlobalOneOfNatUdpTimeoutOptionsDef1,
            OneOfNatUdpTimeoutOptionsDef2,
            GlobalOneOfNatUdpTimeoutOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalSettingsNatUdpTimeout"})
    global_settings_ssh_version: Optional[
        Union[GlobalOneOfVersionOptionsDef1, OneOfVersionOptionsDef2, OneOfVersionOptionsDef3]
    ] = _field(default=None, metadata={"alias": "globalSettingsSSHVersion"})
    services_global_services_ip_source_intrf: Optional[
        Union[
            OneOfSourceInterfaceOptionsDef1,
            OneOfSourceInterfaceOptionsDef2,
            OneOfSourceInterfaceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "servicesGlobalServicesIpSourceIntrf"})


@dataclass
class GlobalServicesGlobal:
    services_ip: GlobalServicesIp


@dataclass
class SdRoutingSystemGlobalData:
    services_global: GlobalServicesGlobal


@dataclass
class GlobalPayload:
    """
    Global settings feature schema for PUT request
    """

    data: SdRoutingSystemGlobalData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingSystemGlobalPayload:
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
    # Global settings feature schema for PUT request
    payload: Optional[GlobalPayload] = _field(default=None)


@dataclass
class EditSdroutingGlobalSettingFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemGlobalOneOfUdpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemGlobalOneOfUdpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemGlobalOneOfTcpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemGlobalOneOfTcpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemGlobalOneOfNatUdpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemGlobalOneOfNatUdpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemGlobalOneOfNatTcpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemGlobalOneOfNatTcpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemGlobalOneOfHttpAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemGlobalHttpAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemGlobalOneOfVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemGlobalVersionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemGlobalServicesIp:
    services_global_services_ip_arp_proxy: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpArpProxy"})
    services_global_services_ip_cdp: Union[
        OneOfServerDefaultTrueOptionsDef1,
        OneOfServerDefaultTrueOptionsDef2,
        OneOfServerDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpCdp"})
    services_global_services_ip_domain_lookup: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpDomainLookup"})
    services_global_services_ip_ftp_passive: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpFtpPassive"})
    services_global_services_ip_http_server: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpHttpServer"})
    services_global_services_ip_https_server: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpHttpsServer"})
    services_global_services_ip_line_vty: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpLineVty"})
    services_global_services_ip_lldp: Union[
        OneOfServerDefaultTrueOptionsDef1,
        OneOfServerDefaultTrueOptionsDef2,
        OneOfServerDefaultTrueOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpLldp"})
    services_global_services_ip_rcmd: Union[
        OneOfServerDefaultFalseOptionsDef1,
        OneOfServerDefaultFalseOptionsDef2,
        OneOfServerDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "servicesGlobalServicesIpRcmd"})
    bgp_community_new_format: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bgpCommunityNewFormat"})
    global_other_settings_console_logging: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsConsoleLogging"})
    global_other_settings_ignore_bootp: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsIgnoreBootp"})
    global_other_settings_ip_source_route: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsIPSourceRoute"})
    global_other_settings_snmp_ifindex_persist: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsSnmpIfindexPersist"})
    global_other_settings_tcp_keepalives_in: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsTcpKeepalivesIn"})
    global_other_settings_tcp_keepalives_out: Optional[
        Union[
            OneOfServerDefaultTrueOptionsDef1,
            OneOfServerDefaultTrueOptionsDef2,
            OneOfServerDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsTcpKeepalivesOut"})
    global_other_settings_tcp_small_servers: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsTcpSmallServers"})
    global_other_settings_udp_small_servers: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsUdpSmallServers"})
    global_other_settings_vty_line_logging: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalOtherSettingsVtyLineLogging"})
    global_settings_http_authentication: Optional[
        Union[
            SystemGlobalOneOfHttpAuthenticationOptionsDef1,
            OneOfHttpAuthenticationOptionsDef2,
            OneOfHttpAuthenticationOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalSettingsHttpAuthentication"})
    global_settings_nat64_tcp_timeout: Optional[
        Union[
            SystemGlobalOneOfTcpTimeoutOptionsDef1,
            OneOfTcpTimeoutOptionsDef2,
            SystemGlobalOneOfTcpTimeoutOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalSettingsNat64TcpTimeout"})
    global_settings_nat64_udp_timeout: Optional[
        Union[
            SystemGlobalOneOfUdpTimeoutOptionsDef1,
            OneOfUdpTimeoutOptionsDef2,
            SystemGlobalOneOfUdpTimeoutOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalSettingsNat64UdpTimeout"})
    global_settings_nat_tcp_timeout: Optional[
        Union[
            SystemGlobalOneOfNatTcpTimeoutOptionsDef1,
            OneOfNatTcpTimeoutOptionsDef2,
            SystemGlobalOneOfNatTcpTimeoutOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalSettingsNatTcpTimeout"})
    global_settings_nat_udp_timeout: Optional[
        Union[
            SystemGlobalOneOfNatUdpTimeoutOptionsDef1,
            OneOfNatUdpTimeoutOptionsDef2,
            SystemGlobalOneOfNatUdpTimeoutOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "globalSettingsNatUdpTimeout"})
    global_settings_ssh_version: Optional[
        Union[SystemGlobalOneOfVersionOptionsDef1, OneOfVersionOptionsDef2, OneOfVersionOptionsDef3]
    ] = _field(default=None, metadata={"alias": "globalSettingsSSHVersion"})
    services_global_services_ip_source_intrf: Optional[
        Union[
            OneOfSourceInterfaceOptionsDef1,
            OneOfSourceInterfaceOptionsDef2,
            OneOfSourceInterfaceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "servicesGlobalServicesIpSourceIntrf"})


@dataclass
class SystemGlobalServicesGlobal:
    services_ip: SystemGlobalServicesIp


@dataclass
class FeatureProfileSdRoutingSystemGlobalData:
    services_global: SystemGlobalServicesGlobal


@dataclass
class EditSdroutingGlobalSettingFeaturePutRequest:
    """
    Global settings feature schema for PUT request
    """

    data: FeatureProfileSdRoutingSystemGlobalData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
