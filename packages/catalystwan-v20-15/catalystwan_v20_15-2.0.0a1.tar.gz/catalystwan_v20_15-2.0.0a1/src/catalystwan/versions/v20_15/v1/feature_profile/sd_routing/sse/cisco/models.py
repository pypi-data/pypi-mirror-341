# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

SseInstanceDef = Literal["Cisco-Secure-Access"]

DefaultOptionTypeDef = Literal["default"]

VariableOptionTypeDef = Literal["variable"]

InterfaceTunnelDcPreferenceDef = Literal["primary-dc", "secondary-dc"]

InterfaceIkeCiphersuiteDef = Literal[
    "aes128-cbc-sha1", "aes128-cbc-sha2", "aes256-cbc-sha1", "aes256-cbc-sha2"
]

DefaultInterfaceIkeCiphersuiteDef = Literal["aes256-cbc-sha1"]

InterfaceIkeGroupDef = Literal["14", "15", "16", "19", "2", "20", "21", "5"]

InterfaceIpsecCiphersuiteDef = Literal[
    "aes256-cbc-sha1", "aes256-cbc-sha256", "aes256-cbc-sha384", "aes256-cbc-sha512", "aes256-gcm"
]

InterfacePerfectForwardSecrecyDef = Literal[
    "group-14",
    "group-15",
    "group-16",
    "group-19",
    "group-2",
    "group-20",
    "group-21",
    "group-5",
    "none",
]

DefaultInterfaceTrackerDef = Literal["DefaultTracker"]

DefaultRegionDef = Literal["auto"]

TrackerTrackerTypeDef = Literal["cisco-sse"]

CiscoSseInstanceDef = Literal["Cisco-Secure-Access"]

CiscoInterfaceTunnelDcPreferenceDef = Literal["primary-dc", "secondary-dc"]

CiscoInterfaceIkeCiphersuiteDef = Literal[
    "aes128-cbc-sha1", "aes128-cbc-sha2", "aes256-cbc-sha1", "aes256-cbc-sha2"
]

CiscoDefaultInterfaceIkeCiphersuiteDef = Literal["aes256-cbc-sha1"]

CiscoInterfaceIkeGroupDef = Literal["14", "15", "16", "19", "2", "20", "21", "5"]

SseCiscoInterfaceIkeGroupDef = Literal["14", "15", "16", "19", "2", "20", "21", "5"]

CiscoInterfaceIpsecCiphersuiteDef = Literal[
    "aes256-cbc-sha1", "aes256-cbc-sha256", "aes256-cbc-sha384", "aes256-cbc-sha512", "aes256-gcm"
]

SseCiscoInterfaceIpsecCiphersuiteDef = Literal[
    "aes256-cbc-sha1", "aes256-cbc-sha256", "aes256-cbc-sha384", "aes256-cbc-sha512", "aes256-gcm"
]

CiscoInterfacePerfectForwardSecrecyDef = Literal[
    "group-14",
    "group-15",
    "group-16",
    "group-19",
    "group-2",
    "group-20",
    "group-21",
    "group-5",
    "none",
]

SseCiscoInterfacePerfectForwardSecrecyDef = Literal[
    "group-14",
    "group-15",
    "group-16",
    "group-19",
    "group-2",
    "group-20",
    "group-21",
    "group-5",
    "none",
]

CiscoDefaultInterfaceTrackerDef = Literal["DefaultTracker"]

CiscoDefaultRegionDef = Literal["auto"]

CiscoTrackerTrackerTypeDef = Literal["cisco-sse"]

SseCiscoSseInstanceDef = Literal["Cisco-Secure-Access"]

SseCiscoInterfaceTunnelDcPreferenceDef = Literal["primary-dc", "secondary-dc"]

SseCiscoInterfaceIkeCiphersuiteDef = Literal[
    "aes128-cbc-sha1", "aes128-cbc-sha2", "aes256-cbc-sha1", "aes256-cbc-sha2"
]

SseCiscoDefaultInterfaceIkeCiphersuiteDef = Literal["aes256-cbc-sha1"]

SdRoutingSseCiscoInterfaceIkeGroupDef = Literal["14", "15", "16", "19", "2", "20", "21", "5"]

FeatureProfileSdRoutingSseCiscoInterfaceIkeGroupDef = Literal[
    "14", "15", "16", "19", "2", "20", "21", "5"
]

SdRoutingSseCiscoInterfaceIpsecCiphersuiteDef = Literal[
    "aes256-cbc-sha1", "aes256-cbc-sha256", "aes256-cbc-sha384", "aes256-cbc-sha512", "aes256-gcm"
]

FeatureProfileSdRoutingSseCiscoInterfaceIpsecCiphersuiteDef = Literal[
    "aes256-cbc-sha1", "aes256-cbc-sha256", "aes256-cbc-sha384", "aes256-cbc-sha512", "aes256-gcm"
]

SdRoutingSseCiscoInterfacePerfectForwardSecrecyDef = Literal[
    "group-14",
    "group-15",
    "group-16",
    "group-19",
    "group-2",
    "group-20",
    "group-21",
    "group-5",
    "none",
]

FeatureProfileSdRoutingSseCiscoInterfacePerfectForwardSecrecyDef = Literal[
    "group-14",
    "group-15",
    "group-16",
    "group-19",
    "group-2",
    "group-20",
    "group-21",
    "group-5",
    "none",
]

SseCiscoDefaultInterfaceTrackerDef = Literal["DefaultTracker"]

SseCiscoDefaultRegionDef = Literal["auto"]

SseCiscoTrackerTrackerTypeDef = Literal["cisco-sse"]


@dataclass
class OneOfSseInstanceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SseInstanceDef


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
class OneOfInterfaceIfNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


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
class OneOfInterfaceTunnelSourceInterfaceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceTunnelSourceInterfaceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceTunnelRouteViaOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceTunnelRouteViaOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceTunnelDcPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceTunnelDcPreferenceDef


@dataclass
class OneOfInterfaceTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceTcpMssAdjustOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceTcpMssAdjustOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceMtuOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceDpdIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceDpdIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceDpdIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceDpdRetriesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceDpdRetriesOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceDpdRetriesOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceIkeVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceIkeVersionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIkeVersionOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceIkeRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceIkeRekeyIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIkeRekeyIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceIkeCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceIkeCiphersuiteDef


@dataclass
class OneOfInterfaceIkeCiphersuiteOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIkeCiphersuiteOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[DefaultInterfaceIkeCiphersuiteDef] = _field(default=None)


@dataclass
class OneOfInterfaceIkeGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceIkeGroupDef


@dataclass
class OneOfInterfaceIkeGroupOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIkeGroupOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[InterfaceIkeGroupDef] = _field(default="16")


@dataclass
class OneOfInterfaceIpsecRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceIpsecRekeyIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecRekeyIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecReplayWindowOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceIpsecReplayWindowOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecReplayWindowOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceIpsecCiphersuiteDef


@dataclass
class OneOfInterfaceIpsecCiphersuiteOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecCiphersuiteOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[InterfaceIpsecCiphersuiteDef] = _field(default="aes256-cbc-sha512")


@dataclass
class OneOfInterfacePerfectForwardSecrecyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfacePerfectForwardSecrecyDef


@dataclass
class OneOfInterfacePerfectForwardSecrecyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfacePerfectForwardSecrecyOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[InterfacePerfectForwardSecrecyDef] = _field(default="group-16")


@dataclass
class OneOfInterfaceTrackerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceTrackerOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultInterfaceTrackerDef  # pytype: disable=annotation-type-mismatch


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
class Interface:
    if_name: OneOfInterfaceIfNameOptionsDef = _field(metadata={"alias": "ifName"})
    dpd_interval: Optional[
        Union[
            OneOfInterfaceDpdIntervalOptionsDef1,
            OneOfInterfaceDpdIntervalOptionsDef2,
            OneOfInterfaceDpdIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dpdInterval"})
    dpd_retries: Optional[
        Union[
            OneOfInterfaceDpdRetriesOptionsDef1,
            OneOfInterfaceDpdRetriesOptionsDef2,
            OneOfInterfaceDpdRetriesOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dpdRetries"})
    ike_ciphersuite: Optional[
        Union[
            OneOfInterfaceIkeCiphersuiteOptionsDef1,
            OneOfInterfaceIkeCiphersuiteOptionsDef2,
            OneOfInterfaceIkeCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeCiphersuite"})
    ike_group: Optional[
        Union[
            OneOfInterfaceIkeGroupOptionsDef1,
            OneOfInterfaceIkeGroupOptionsDef2,
            OneOfInterfaceIkeGroupOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeGroup"})
    ike_rekey_interval: Optional[
        Union[
            OneOfInterfaceIkeRekeyIntervalOptionsDef1,
            OneOfInterfaceIkeRekeyIntervalOptionsDef2,
            OneOfInterfaceIkeRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeRekeyInterval"})
    ike_version: Optional[
        Union[
            OneOfInterfaceIkeVersionOptionsDef1,
            OneOfInterfaceIkeVersionOptionsDef2,
            OneOfInterfaceIkeVersionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeVersion"})
    ipsec_ciphersuite: Optional[
        Union[
            OneOfInterfaceIpsecCiphersuiteOptionsDef1,
            OneOfInterfaceIpsecCiphersuiteOptionsDef2,
            OneOfInterfaceIpsecCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecCiphersuite"})
    ipsec_rekey_interval: Optional[
        Union[
            OneOfInterfaceIpsecRekeyIntervalOptionsDef1,
            OneOfInterfaceIpsecRekeyIntervalOptionsDef2,
            OneOfInterfaceIpsecRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecRekeyInterval"})
    ipsec_replay_window: Optional[
        Union[
            OneOfInterfaceIpsecReplayWindowOptionsDef1,
            OneOfInterfaceIpsecReplayWindowOptionsDef2,
            OneOfInterfaceIpsecReplayWindowOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecReplayWindow"})
    mtu: Optional[Union[OneOfInterfaceMtuOptionsDef1, OneOfInterfaceMtuOptionsDef2]] = _field(
        default=None
    )
    perfect_forward_secrecy: Optional[
        Union[
            OneOfInterfacePerfectForwardSecrecyOptionsDef1,
            OneOfInterfacePerfectForwardSecrecyOptionsDef2,
            OneOfInterfacePerfectForwardSecrecyOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "perfectForwardSecrecy"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    tcp_mss_adjust: Optional[
        Union[
            OneOfInterfaceTcpMssAdjustOptionsDef1,
            OneOfInterfaceTcpMssAdjustOptionsDef2,
            OneOfInterfaceTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})
    track_enable: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackEnable"})
    tracker: Optional[Union[OneOfInterfaceTrackerOptionsDef1, OneOfInterfaceTrackerOptionsDef2]] = (
        _field(default=None)
    )
    tunnel_dc_preference: Optional[OneOfInterfaceTunnelDcPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "tunnelDcPreference"}
    )
    tunnel_route_via: Optional[
        Union[OneOfInterfaceTunnelRouteViaOptionsDef1, OneOfInterfaceTunnelRouteViaOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    tunnel_source_interface: Optional[
        Union[
            OneOfInterfaceTunnelSourceInterfaceOptionsDef1,
            OneOfInterfaceTunnelSourceInterfaceOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelSourceInterface"})


@dataclass
class OneOfServiceInterfacePairActiveInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfServiceInterfacePairActiveInterfaceWeightOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfServiceInterfacePairBackupInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfServiceInterfacePairBackupInterfaceWeightOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfacePair:
    active_interface: OneOfServiceInterfacePairActiveInterfaceOptionsDef = _field(
        metadata={"alias": "activeInterface"}
    )
    backup_interface: OneOfServiceInterfacePairBackupInterfaceOptionsDef = _field(
        metadata={"alias": "backupInterface"}
    )
    active_interface_weight: Optional[OneOfServiceInterfacePairActiveInterfaceWeightOptionsDef] = (
        _field(default=None, metadata={"alias": "activeInterfaceWeight"})
    )
    backup_interface_weight: Optional[OneOfServiceInterfacePairBackupInterfaceWeightOptionsDef] = (
        _field(default=None, metadata={"alias": "backupInterfaceWeight"})
    )


@dataclass
class OneOfRegionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRegionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRegionOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[DefaultRegionDef] = _field(default=None)


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
class OneOfTrackerNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTrackerEndpointApiUrlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTrackerEndpointApiUrlOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTrackerThresholdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerThresholdOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfTrackerIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTrackerIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfTrackerMultiplierOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTrackerMultiplierOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerMultiplierOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfTrackerTrackerTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TrackerTrackerTypeDef


@dataclass
class Tracker:
    endpoint_api_url: Union[
        OneOfTrackerEndpointApiUrlOptionsDef1, OneOfTrackerEndpointApiUrlOptionsDef2
    ] = _field(metadata={"alias": "endpointApiUrl"})
    name: OneOfTrackerNameOptionsDef
    tracker_type: OneOfTrackerTrackerTypeOptionsDef = _field(metadata={"alias": "trackerType"})
    interval: Optional[
        Union[
            OneOfTrackerIntervalOptionsDef1,
            OneOfTrackerIntervalOptionsDef2,
            OneOfTrackerIntervalOptionsDef3,
        ]
    ] = _field(default=None)
    multiplier: Optional[
        Union[
            OneOfTrackerMultiplierOptionsDef1,
            OneOfTrackerMultiplierOptionsDef2,
            OneOfTrackerMultiplierOptionsDef3,
        ]
    ] = _field(default=None)
    threshold: Optional[
        Union[
            OneOfTrackerThresholdOptionsDef1,
            OneOfTrackerThresholdOptionsDef2,
            OneOfTrackerThresholdOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class CiscoData:
    # Interface name: IPsec when present
    interface: List[Interface]
    # Interface Pair for active and backup
    interface_pair: List[InterfacePair] = _field(metadata={"alias": "interfacePair"})
    region: Union[OneOfRegionOptionsDef1, OneOfRegionOptionsDef2, OneOfRegionOptionsDef3]
    sse_instance: OneOfSseInstanceOptionsDef
    tracker_src_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "trackerSrcIp"}
    )
    context_sharing_for_sgt: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForSgt"})
    context_sharing_for_vpn: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForVpn"})
    # Tracker configuration
    tracker: Optional[List[Tracker]] = _field(default=None)


@dataclass
class Payload:
    """
    Cisco-SSE schema for POST request
    """

    data: CiscoData
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
    # Cisco-SSE schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingSseCiscoSsePayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateCiscoSseFeatureForSsePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SseCiscoData:
    # Interface name: IPsec when present
    interface: List[Interface]
    # Interface Pair for active and backup
    interface_pair: List[InterfacePair] = _field(metadata={"alias": "interfacePair"})
    region: Union[OneOfRegionOptionsDef1, OneOfRegionOptionsDef2, OneOfRegionOptionsDef3]
    sse_instance: OneOfSseInstanceOptionsDef
    tracker_src_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "trackerSrcIp"}
    )
    context_sharing_for_sgt: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForSgt"})
    context_sharing_for_vpn: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForVpn"})
    # Tracker configuration
    tracker: Optional[List[Tracker]] = _field(default=None)


@dataclass
class CreateCiscoSseFeatureForSsePostRequest:
    """
    Cisco-SSE schema for POST request
    """

    data: SseCiscoData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class CiscoOneOfSseInstanceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CiscoSseInstanceDef


@dataclass
class CiscoOneOfInterfaceIfNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CiscoOneOfInterfaceTunnelRouteViaOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CiscoOneOfInterfaceTunnelDcPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CiscoInterfaceTunnelDcPreferenceDef


@dataclass
class CiscoOneOfInterfaceTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CiscoOneOfInterfaceMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CiscoOneOfInterfaceDpdIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CiscoOneOfInterfaceDpdIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class CiscoOneOfInterfaceDpdRetriesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CiscoOneOfInterfaceDpdRetriesOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class CiscoOneOfInterfaceIkeVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CiscoOneOfInterfaceIkeVersionOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class CiscoOneOfInterfaceIkeRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CiscoOneOfInterfaceIkeRekeyIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class CiscoOneOfInterfaceIkeCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CiscoInterfaceIkeCiphersuiteDef


@dataclass
class CiscoOneOfInterfaceIkeCiphersuiteOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[CiscoDefaultInterfaceIkeCiphersuiteDef] = _field(default=None)


@dataclass
class CiscoOneOfInterfaceIkeGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CiscoInterfaceIkeGroupDef


@dataclass
class CiscoOneOfInterfaceIkeGroupOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SseCiscoInterfaceIkeGroupDef] = _field(default="16")


@dataclass
class CiscoOneOfInterfaceIpsecRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CiscoOneOfInterfaceIpsecRekeyIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class CiscoOneOfInterfaceIpsecReplayWindowOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CiscoOneOfInterfaceIpsecReplayWindowOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class CiscoOneOfInterfaceIpsecCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CiscoInterfaceIpsecCiphersuiteDef


@dataclass
class CiscoOneOfInterfaceIpsecCiphersuiteOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SseCiscoInterfaceIpsecCiphersuiteDef] = _field(default="aes256-cbc-sha512")


@dataclass
class CiscoOneOfInterfacePerfectForwardSecrecyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CiscoInterfacePerfectForwardSecrecyDef


@dataclass
class CiscoOneOfInterfacePerfectForwardSecrecyOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SseCiscoInterfacePerfectForwardSecrecyDef] = _field(default="group-16")


@dataclass
class CiscoOneOfInterfaceTrackerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CiscoOneOfInterfaceTrackerOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CiscoDefaultInterfaceTrackerDef  # pytype: disable=annotation-type-mismatch


@dataclass
class CiscoInterface:
    if_name: CiscoOneOfInterfaceIfNameOptionsDef = _field(metadata={"alias": "ifName"})
    dpd_interval: Optional[
        Union[
            CiscoOneOfInterfaceDpdIntervalOptionsDef1,
            OneOfInterfaceDpdIntervalOptionsDef2,
            CiscoOneOfInterfaceDpdIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dpdInterval"})
    dpd_retries: Optional[
        Union[
            CiscoOneOfInterfaceDpdRetriesOptionsDef1,
            OneOfInterfaceDpdRetriesOptionsDef2,
            CiscoOneOfInterfaceDpdRetriesOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dpdRetries"})
    ike_ciphersuite: Optional[
        Union[
            CiscoOneOfInterfaceIkeCiphersuiteOptionsDef1,
            OneOfInterfaceIkeCiphersuiteOptionsDef2,
            CiscoOneOfInterfaceIkeCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeCiphersuite"})
    ike_group: Optional[
        Union[
            CiscoOneOfInterfaceIkeGroupOptionsDef1,
            OneOfInterfaceIkeGroupOptionsDef2,
            CiscoOneOfInterfaceIkeGroupOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeGroup"})
    ike_rekey_interval: Optional[
        Union[
            CiscoOneOfInterfaceIkeRekeyIntervalOptionsDef1,
            OneOfInterfaceIkeRekeyIntervalOptionsDef2,
            CiscoOneOfInterfaceIkeRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeRekeyInterval"})
    ike_version: Optional[
        Union[
            CiscoOneOfInterfaceIkeVersionOptionsDef1,
            OneOfInterfaceIkeVersionOptionsDef2,
            CiscoOneOfInterfaceIkeVersionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeVersion"})
    ipsec_ciphersuite: Optional[
        Union[
            CiscoOneOfInterfaceIpsecCiphersuiteOptionsDef1,
            OneOfInterfaceIpsecCiphersuiteOptionsDef2,
            CiscoOneOfInterfaceIpsecCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecCiphersuite"})
    ipsec_rekey_interval: Optional[
        Union[
            CiscoOneOfInterfaceIpsecRekeyIntervalOptionsDef1,
            OneOfInterfaceIpsecRekeyIntervalOptionsDef2,
            CiscoOneOfInterfaceIpsecRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecRekeyInterval"})
    ipsec_replay_window: Optional[
        Union[
            CiscoOneOfInterfaceIpsecReplayWindowOptionsDef1,
            OneOfInterfaceIpsecReplayWindowOptionsDef2,
            CiscoOneOfInterfaceIpsecReplayWindowOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecReplayWindow"})
    mtu: Optional[Union[CiscoOneOfInterfaceMtuOptionsDef1, OneOfInterfaceMtuOptionsDef2]] = _field(
        default=None
    )
    perfect_forward_secrecy: Optional[
        Union[
            CiscoOneOfInterfacePerfectForwardSecrecyOptionsDef1,
            OneOfInterfacePerfectForwardSecrecyOptionsDef2,
            CiscoOneOfInterfacePerfectForwardSecrecyOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "perfectForwardSecrecy"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    tcp_mss_adjust: Optional[
        Union[
            CiscoOneOfInterfaceTcpMssAdjustOptionsDef1,
            OneOfInterfaceTcpMssAdjustOptionsDef2,
            OneOfInterfaceTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})
    track_enable: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackEnable"})
    tracker: Optional[
        Union[CiscoOneOfInterfaceTrackerOptionsDef1, CiscoOneOfInterfaceTrackerOptionsDef2]
    ] = _field(default=None)
    tunnel_dc_preference: Optional[CiscoOneOfInterfaceTunnelDcPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "tunnelDcPreference"}
    )
    tunnel_route_via: Optional[
        Union[CiscoOneOfInterfaceTunnelRouteViaOptionsDef1, OneOfInterfaceTunnelRouteViaOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    tunnel_source_interface: Optional[
        Union[
            OneOfInterfaceTunnelSourceInterfaceOptionsDef1,
            OneOfInterfaceTunnelSourceInterfaceOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelSourceInterface"})


@dataclass
class CiscoOneOfServiceInterfacePairActiveInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CiscoOneOfServiceInterfacePairActiveInterfaceWeightOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CiscoOneOfServiceInterfacePairBackupInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CiscoOneOfServiceInterfacePairBackupInterfaceWeightOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CiscoInterfacePair:
    active_interface: CiscoOneOfServiceInterfacePairActiveInterfaceOptionsDef = _field(
        metadata={"alias": "activeInterface"}
    )
    backup_interface: CiscoOneOfServiceInterfacePairBackupInterfaceOptionsDef = _field(
        metadata={"alias": "backupInterface"}
    )
    active_interface_weight: Optional[
        CiscoOneOfServiceInterfacePairActiveInterfaceWeightOptionsDef
    ] = _field(default=None, metadata={"alias": "activeInterfaceWeight"})
    backup_interface_weight: Optional[
        CiscoOneOfServiceInterfacePairBackupInterfaceWeightOptionsDef
    ] = _field(default=None, metadata={"alias": "backupInterfaceWeight"})


@dataclass
class CiscoOneOfRegionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CiscoOneOfRegionOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[CiscoDefaultRegionDef] = _field(default=None)


@dataclass
class CiscoOneOfTrackerNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CiscoOneOfTrackerEndpointApiUrlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CiscoOneOfTrackerThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CiscoOneOfTrackerThresholdOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class CiscoOneOfTrackerIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CiscoOneOfTrackerIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class CiscoOneOfTrackerMultiplierOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class CiscoOneOfTrackerMultiplierOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class CiscoOneOfTrackerTrackerTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CiscoTrackerTrackerTypeDef


@dataclass
class CiscoTracker:
    endpoint_api_url: Union[
        CiscoOneOfTrackerEndpointApiUrlOptionsDef1, OneOfTrackerEndpointApiUrlOptionsDef2
    ] = _field(metadata={"alias": "endpointApiUrl"})
    name: CiscoOneOfTrackerNameOptionsDef
    tracker_type: CiscoOneOfTrackerTrackerTypeOptionsDef = _field(metadata={"alias": "trackerType"})
    interval: Optional[
        Union[
            CiscoOneOfTrackerIntervalOptionsDef1,
            OneOfTrackerIntervalOptionsDef2,
            CiscoOneOfTrackerIntervalOptionsDef3,
        ]
    ] = _field(default=None)
    multiplier: Optional[
        Union[
            CiscoOneOfTrackerMultiplierOptionsDef1,
            OneOfTrackerMultiplierOptionsDef2,
            CiscoOneOfTrackerMultiplierOptionsDef3,
        ]
    ] = _field(default=None)
    threshold: Optional[
        Union[
            CiscoOneOfTrackerThresholdOptionsDef1,
            OneOfTrackerThresholdOptionsDef2,
            CiscoOneOfTrackerThresholdOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class SdRoutingSseCiscoData:
    # Interface name: IPsec when present
    interface: List[CiscoInterface]
    # Interface Pair for active and backup
    interface_pair: List[CiscoInterfacePair] = _field(metadata={"alias": "interfacePair"})
    region: Union[CiscoOneOfRegionOptionsDef1, OneOfRegionOptionsDef2, CiscoOneOfRegionOptionsDef3]
    sse_instance: CiscoOneOfSseInstanceOptionsDef
    tracker_src_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "trackerSrcIp"}
    )
    context_sharing_for_sgt: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForSgt"})
    context_sharing_for_vpn: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForVpn"})
    # Tracker configuration
    tracker: Optional[List[CiscoTracker]] = _field(default=None)


@dataclass
class CiscoPayload:
    """
    Cisco-SSE schema for PUT request
    """

    data: SdRoutingSseCiscoData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdRoutingSseCiscoSsePayload:
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
    # Cisco-SSE schema for PUT request
    payload: Optional[CiscoPayload] = _field(default=None)


@dataclass
class EditCiscoSseFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SseCiscoOneOfSseInstanceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SseCiscoSseInstanceDef


@dataclass
class SseCiscoOneOfInterfaceIfNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SseCiscoOneOfInterfaceTunnelRouteViaOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SseCiscoOneOfInterfaceTunnelDcPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SseCiscoInterfaceTunnelDcPreferenceDef


@dataclass
class SseCiscoOneOfInterfaceTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SseCiscoOneOfInterfaceMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SseCiscoOneOfInterfaceDpdIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SseCiscoOneOfInterfaceDpdIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SseCiscoOneOfInterfaceDpdRetriesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SseCiscoOneOfInterfaceDpdRetriesOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SseCiscoOneOfInterfaceIkeVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SseCiscoOneOfInterfaceIkeVersionOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SseCiscoOneOfInterfaceIkeRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SseCiscoOneOfInterfaceIkeRekeyIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SseCiscoOneOfInterfaceIkeCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SseCiscoInterfaceIkeCiphersuiteDef


@dataclass
class SseCiscoOneOfInterfaceIkeCiphersuiteOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SseCiscoDefaultInterfaceIkeCiphersuiteDef] = _field(default=None)


@dataclass
class SseCiscoOneOfInterfaceIkeGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdRoutingSseCiscoInterfaceIkeGroupDef


@dataclass
class SseCiscoOneOfInterfaceIkeGroupOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[FeatureProfileSdRoutingSseCiscoInterfaceIkeGroupDef] = _field(default="16")


@dataclass
class SseCiscoOneOfInterfaceIpsecRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SseCiscoOneOfInterfaceIpsecRekeyIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SseCiscoOneOfInterfaceIpsecReplayWindowOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SseCiscoOneOfInterfaceIpsecReplayWindowOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SseCiscoOneOfInterfaceIpsecCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdRoutingSseCiscoInterfaceIpsecCiphersuiteDef


@dataclass
class SseCiscoOneOfInterfaceIpsecCiphersuiteOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[FeatureProfileSdRoutingSseCiscoInterfaceIpsecCiphersuiteDef] = _field(
        default="aes256-cbc-sha512"
    )


@dataclass
class SseCiscoOneOfInterfacePerfectForwardSecrecyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdRoutingSseCiscoInterfacePerfectForwardSecrecyDef


@dataclass
class SseCiscoOneOfInterfacePerfectForwardSecrecyOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[FeatureProfileSdRoutingSseCiscoInterfacePerfectForwardSecrecyDef] = _field(
        default="group-16"
    )


@dataclass
class SseCiscoOneOfInterfaceTrackerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SseCiscoOneOfInterfaceTrackerOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SseCiscoDefaultInterfaceTrackerDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SseCiscoInterface:
    if_name: SseCiscoOneOfInterfaceIfNameOptionsDef = _field(metadata={"alias": "ifName"})
    dpd_interval: Optional[
        Union[
            SseCiscoOneOfInterfaceDpdIntervalOptionsDef1,
            OneOfInterfaceDpdIntervalOptionsDef2,
            SseCiscoOneOfInterfaceDpdIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dpdInterval"})
    dpd_retries: Optional[
        Union[
            SseCiscoOneOfInterfaceDpdRetriesOptionsDef1,
            OneOfInterfaceDpdRetriesOptionsDef2,
            SseCiscoOneOfInterfaceDpdRetriesOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dpdRetries"})
    ike_ciphersuite: Optional[
        Union[
            SseCiscoOneOfInterfaceIkeCiphersuiteOptionsDef1,
            OneOfInterfaceIkeCiphersuiteOptionsDef2,
            SseCiscoOneOfInterfaceIkeCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeCiphersuite"})
    ike_group: Optional[
        Union[
            SseCiscoOneOfInterfaceIkeGroupOptionsDef1,
            OneOfInterfaceIkeGroupOptionsDef2,
            SseCiscoOneOfInterfaceIkeGroupOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeGroup"})
    ike_rekey_interval: Optional[
        Union[
            SseCiscoOneOfInterfaceIkeRekeyIntervalOptionsDef1,
            OneOfInterfaceIkeRekeyIntervalOptionsDef2,
            SseCiscoOneOfInterfaceIkeRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeRekeyInterval"})
    ike_version: Optional[
        Union[
            SseCiscoOneOfInterfaceIkeVersionOptionsDef1,
            OneOfInterfaceIkeVersionOptionsDef2,
            SseCiscoOneOfInterfaceIkeVersionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeVersion"})
    ipsec_ciphersuite: Optional[
        Union[
            SseCiscoOneOfInterfaceIpsecCiphersuiteOptionsDef1,
            OneOfInterfaceIpsecCiphersuiteOptionsDef2,
            SseCiscoOneOfInterfaceIpsecCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecCiphersuite"})
    ipsec_rekey_interval: Optional[
        Union[
            SseCiscoOneOfInterfaceIpsecRekeyIntervalOptionsDef1,
            OneOfInterfaceIpsecRekeyIntervalOptionsDef2,
            SseCiscoOneOfInterfaceIpsecRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecRekeyInterval"})
    ipsec_replay_window: Optional[
        Union[
            SseCiscoOneOfInterfaceIpsecReplayWindowOptionsDef1,
            OneOfInterfaceIpsecReplayWindowOptionsDef2,
            SseCiscoOneOfInterfaceIpsecReplayWindowOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecReplayWindow"})
    mtu: Optional[Union[SseCiscoOneOfInterfaceMtuOptionsDef1, OneOfInterfaceMtuOptionsDef2]] = (
        _field(default=None)
    )
    perfect_forward_secrecy: Optional[
        Union[
            SseCiscoOneOfInterfacePerfectForwardSecrecyOptionsDef1,
            OneOfInterfacePerfectForwardSecrecyOptionsDef2,
            SseCiscoOneOfInterfacePerfectForwardSecrecyOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "perfectForwardSecrecy"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    tcp_mss_adjust: Optional[
        Union[
            SseCiscoOneOfInterfaceTcpMssAdjustOptionsDef1,
            OneOfInterfaceTcpMssAdjustOptionsDef2,
            OneOfInterfaceTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})
    track_enable: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackEnable"})
    tracker: Optional[
        Union[SseCiscoOneOfInterfaceTrackerOptionsDef1, SseCiscoOneOfInterfaceTrackerOptionsDef2]
    ] = _field(default=None)
    tunnel_dc_preference: Optional[SseCiscoOneOfInterfaceTunnelDcPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "tunnelDcPreference"}
    )
    tunnel_route_via: Optional[
        Union[
            SseCiscoOneOfInterfaceTunnelRouteViaOptionsDef1, OneOfInterfaceTunnelRouteViaOptionsDef2
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    tunnel_source_interface: Optional[
        Union[
            OneOfInterfaceTunnelSourceInterfaceOptionsDef1,
            OneOfInterfaceTunnelSourceInterfaceOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelSourceInterface"})


@dataclass
class SseCiscoOneOfServiceInterfacePairActiveInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SseCiscoOneOfServiceInterfacePairActiveInterfaceWeightOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SseCiscoOneOfServiceInterfacePairBackupInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SseCiscoOneOfServiceInterfacePairBackupInterfaceWeightOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SseCiscoInterfacePair:
    active_interface: SseCiscoOneOfServiceInterfacePairActiveInterfaceOptionsDef = _field(
        metadata={"alias": "activeInterface"}
    )
    backup_interface: SseCiscoOneOfServiceInterfacePairBackupInterfaceOptionsDef = _field(
        metadata={"alias": "backupInterface"}
    )
    active_interface_weight: Optional[
        SseCiscoOneOfServiceInterfacePairActiveInterfaceWeightOptionsDef
    ] = _field(default=None, metadata={"alias": "activeInterfaceWeight"})
    backup_interface_weight: Optional[
        SseCiscoOneOfServiceInterfacePairBackupInterfaceWeightOptionsDef
    ] = _field(default=None, metadata={"alias": "backupInterfaceWeight"})


@dataclass
class SseCiscoOneOfRegionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SseCiscoOneOfRegionOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SseCiscoDefaultRegionDef] = _field(default=None)


@dataclass
class SseCiscoOneOfTrackerNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SseCiscoOneOfTrackerEndpointApiUrlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SseCiscoOneOfTrackerThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SseCiscoOneOfTrackerThresholdOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SseCiscoOneOfTrackerIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SseCiscoOneOfTrackerIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SseCiscoOneOfTrackerMultiplierOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SseCiscoOneOfTrackerMultiplierOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SseCiscoOneOfTrackerTrackerTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SseCiscoTrackerTrackerTypeDef


@dataclass
class SseCiscoTracker:
    endpoint_api_url: Union[
        SseCiscoOneOfTrackerEndpointApiUrlOptionsDef1, OneOfTrackerEndpointApiUrlOptionsDef2
    ] = _field(metadata={"alias": "endpointApiUrl"})
    name: SseCiscoOneOfTrackerNameOptionsDef
    tracker_type: SseCiscoOneOfTrackerTrackerTypeOptionsDef = _field(
        metadata={"alias": "trackerType"}
    )
    interval: Optional[
        Union[
            SseCiscoOneOfTrackerIntervalOptionsDef1,
            OneOfTrackerIntervalOptionsDef2,
            SseCiscoOneOfTrackerIntervalOptionsDef3,
        ]
    ] = _field(default=None)
    multiplier: Optional[
        Union[
            SseCiscoOneOfTrackerMultiplierOptionsDef1,
            OneOfTrackerMultiplierOptionsDef2,
            SseCiscoOneOfTrackerMultiplierOptionsDef3,
        ]
    ] = _field(default=None)
    threshold: Optional[
        Union[
            SseCiscoOneOfTrackerThresholdOptionsDef1,
            OneOfTrackerThresholdOptionsDef2,
            SseCiscoOneOfTrackerThresholdOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class FeatureProfileSdRoutingSseCiscoData:
    # Interface name: IPsec when present
    interface: List[SseCiscoInterface]
    # Interface Pair for active and backup
    interface_pair: List[SseCiscoInterfacePair] = _field(metadata={"alias": "interfacePair"})
    region: Union[
        SseCiscoOneOfRegionOptionsDef1, OneOfRegionOptionsDef2, SseCiscoOneOfRegionOptionsDef3
    ]
    sse_instance: SseCiscoOneOfSseInstanceOptionsDef
    tracker_src_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "trackerSrcIp"}
    )
    context_sharing_for_sgt: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForSgt"})
    context_sharing_for_vpn: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForVpn"})
    # Tracker configuration
    tracker: Optional[List[SseCiscoTracker]] = _field(default=None)


@dataclass
class EditCiscoSseFeaturePutRequest:
    """
    Cisco-SSE schema for PUT request
    """

    data: FeatureProfileSdRoutingSseCiscoData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
