# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

HttpAuthenticationDef = Literal["aaa", "local"]

VersionDef = Literal["2"]

EtherchannelFlowLbDef = Literal[
    "dst-ip",
    "dst-mac",
    "sdwan",
    "src-dst-ip",
    "src-dst-mac",
    "src-dst-mixed-ip-port",
    "src-ip",
    "src-mac",
]

GlobalHttpAuthenticationDef = Literal["aaa", "local"]

GlobalVersionDef = Literal["2"]

GlobalEtherchannelFlowLbDef = Literal[
    "dst-ip",
    "dst-mac",
    "sdwan",
    "src-dst-ip",
    "src-dst-mac",
    "src-dst-mixed-ip-port",
    "src-ip",
    "src-mac",
]

SystemGlobalHttpAuthenticationDef = Literal["aaa", "local"]

SystemGlobalVersionDef = Literal["2"]

SystemGlobalEtherchannelFlowLbDef = Literal[
    "dst-ip",
    "dst-mac",
    "sdwan",
    "src-dst-ip",
    "src-dst-mac",
    "src-dst-mixed-ip-port",
    "src-ip",
    "src-mac",
]


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
class OneOfLacpSystemPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfLacpSystemPriorityOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLacpSystemPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEtherchannelFlowLbOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EtherchannelFlowLbDef


@dataclass
class OneOfEtherchannelFlowLbOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEtherchannelFlowLbOptionsDef3:
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
    etherchannel_flow_load_balance: Optional[
        Union[
            OneOfEtherchannelFlowLbOptionsDef1,
            OneOfEtherchannelFlowLbOptionsDef2,
            OneOfEtherchannelFlowLbOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "etherchannelFlowLoadBalance"})
    etherchannel_vlan_load_balance: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "etherchannelVlanLoadBalance"})
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
    global_settings_ssh_version: Optional[
        Union[OneOfVersionOptionsDef1, OneOfVersionOptionsDef2, OneOfVersionOptionsDef3]
    ] = _field(default=None, metadata={"alias": "globalSettingsSSHVersion"})
    lacp_system_priority: Optional[
        Union[
            OneOfLacpSystemPriorityOptionsDef1,
            OneOfLacpSystemPriorityOptionsDef2,
            OneOfLacpSystemPriorityOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpSystemPriority"})
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
    Global Services profile parcel schema for POST request
    """

    data: GlobalData
    name: str
    # Set the parcel description
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
    # Global Services profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanSystemGlobalPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateGlobalProfileParcelForSystemPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemGlobalData:
    services_global: ServicesGlobal


@dataclass
class CreateGlobalProfileParcelForSystemPostRequest:
    """
    Global Services profile parcel schema for POST request
    """

    data: SystemGlobalData
    name: str
    # Set the parcel description
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
class GlobalOneOfLacpSystemPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalOneOfEtherchannelFlowLbOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalEtherchannelFlowLbDef


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
    etherchannel_flow_load_balance: Optional[
        Union[
            GlobalOneOfEtherchannelFlowLbOptionsDef1,
            OneOfEtherchannelFlowLbOptionsDef2,
            OneOfEtherchannelFlowLbOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "etherchannelFlowLoadBalance"})
    etherchannel_vlan_load_balance: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "etherchannelVlanLoadBalance"})
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
    global_settings_ssh_version: Optional[
        Union[GlobalOneOfVersionOptionsDef1, OneOfVersionOptionsDef2, OneOfVersionOptionsDef3]
    ] = _field(default=None, metadata={"alias": "globalSettingsSSHVersion"})
    lacp_system_priority: Optional[
        Union[
            GlobalOneOfLacpSystemPriorityOptionsDef1,
            OneOfLacpSystemPriorityOptionsDef2,
            OneOfLacpSystemPriorityOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpSystemPriority"})
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
class SdwanSystemGlobalData:
    services_global: GlobalServicesGlobal


@dataclass
class GlobalPayload:
    """
    Global Services profile parcel schema for PUT request
    """

    data: SdwanSystemGlobalData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanSystemGlobalPayload:
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
    # Global Services profile parcel schema for PUT request
    payload: Optional[GlobalPayload] = _field(default=None)


@dataclass
class EditGlobalProfileParcelForSystemPutResponse:
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
class SystemGlobalOneOfLacpSystemPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemGlobalOneOfEtherchannelFlowLbOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemGlobalEtherchannelFlowLbDef


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
    etherchannel_flow_load_balance: Optional[
        Union[
            SystemGlobalOneOfEtherchannelFlowLbOptionsDef1,
            OneOfEtherchannelFlowLbOptionsDef2,
            OneOfEtherchannelFlowLbOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "etherchannelFlowLoadBalance"})
    etherchannel_vlan_load_balance: Optional[
        Union[
            OneOfServerDefaultFalseOptionsDef1,
            OneOfServerDefaultFalseOptionsDef2,
            OneOfServerDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "etherchannelVlanLoadBalance"})
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
    global_settings_ssh_version: Optional[
        Union[SystemGlobalOneOfVersionOptionsDef1, OneOfVersionOptionsDef2, OneOfVersionOptionsDef3]
    ] = _field(default=None, metadata={"alias": "globalSettingsSSHVersion"})
    lacp_system_priority: Optional[
        Union[
            SystemGlobalOneOfLacpSystemPriorityOptionsDef1,
            OneOfLacpSystemPriorityOptionsDef2,
            OneOfLacpSystemPriorityOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpSystemPriority"})
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
class FeatureProfileSdwanSystemGlobalData:
    services_global: SystemGlobalServicesGlobal


@dataclass
class EditGlobalProfileParcelForSystemPutRequest:
    """
    Global Services profile parcel schema for PUT request
    """

    data: FeatureProfileSdwanSystemGlobalData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
