# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

OptionType = Literal["variable"]

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


@dataclass
class OneOfVirtualApplicationTokenOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVirtualApplicationTokenOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVirtualApplicationVpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVirtualApplicationVpnOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVirtualApplicationVpnOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class TeMgmtIp:
    option_type: Optional[OptionType] = _field(default=None, metadata={"alias": "optionType"})


@dataclass
class TeMgmtSubnetMask:
    option_type: Optional[OptionType] = _field(default=None, metadata={"alias": "optionType"})


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
class OneOfVirtualApplicationNameServerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVirtualApplicationNameServerOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVirtualApplicationNameServerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVirtualApplicationHostnameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVirtualApplicationHostnameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVirtualApplicationHostnameOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class ProxyType:
    """
    Select Web Proxy Type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfVirtualApplicationProxyHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVirtualApplicationProxyHostOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class ProxyConfig1:
    proxy_host: Union[
        OneOfVirtualApplicationProxyHostOptionsDef1, OneOfVirtualApplicationProxyHostOptionsDef2
    ] = _field(metadata={"alias": "proxyHost"})
    proxy_port: Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2] = _field(
        metadata={"alias": "proxyPort"}
    )
    # Select Web Proxy Type
    proxy_type: ProxyType = _field(metadata={"alias": "proxyType"})


@dataclass
class ThousandeyesProxyType:
    """
    Select Web Proxy Type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfVirtualApplicationPacUrlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVirtualApplicationPacUrlOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class ProxyConfig2:
    pac_url: Union[
        OneOfVirtualApplicationPacUrlOptionsDef1, OneOfVirtualApplicationPacUrlOptionsDef2
    ] = _field(metadata={"alias": "pacUrl"})
    # Select Web Proxy Type
    proxy_type: ThousandeyesProxyType = _field(metadata={"alias": "proxyType"})


@dataclass
class OtherThousandeyesProxyType:
    """
    Select Web Proxy Type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class ProxyConfig3:
    # Select Web Proxy Type
    proxy_type: OtherThousandeyesProxyType = _field(metadata={"alias": "proxyType"})


@dataclass
class VirtualApplication1:
    # Web Proxy Type Config
    proxy_config: Union[ProxyConfig1, ProxyConfig2, ProxyConfig3] = _field(
        metadata={"alias": "proxyConfig"}
    )
    token: Union[OneOfVirtualApplicationTokenOptionsDef1, OneOfVirtualApplicationTokenOptionsDef2]
    hostname: Optional[
        Union[
            OneOfVirtualApplicationHostnameOptionsDef1,
            OneOfVirtualApplicationHostnameOptionsDef2,
            OneOfVirtualApplicationHostnameOptionsDef3,
        ]
    ] = _field(default=None)
    name_server: Optional[
        Union[
            OneOfVirtualApplicationNameServerOptionsDef1,
            OneOfVirtualApplicationNameServerOptionsDef2,
            OneOfVirtualApplicationNameServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nameServer"})
    te_mgmt_ip: Optional[TeMgmtIp] = _field(default=None, metadata={"alias": "teMgmtIp"})
    te_mgmt_subnet_mask: Optional[TeMgmtSubnetMask] = _field(
        default=None, metadata={"alias": "teMgmtSubnetMask"}
    )
    te_vpg_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None, metadata={"alias": "teVpgIp"}
    )
    vpn: Optional[
        Union[
            OneOfVirtualApplicationVpnOptionsDef1,
            OneOfVirtualApplicationVpnOptionsDef2,
            OneOfVirtualApplicationVpnOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfIpV4SubnetMaskOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4SubnetMaskOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4SubnetMaskDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VirtualApplication2:
    # Web Proxy Type Config
    proxy_config: Union[ProxyConfig1, ProxyConfig2, ProxyConfig3] = _field(
        metadata={"alias": "proxyConfig"}
    )
    token: Union[OneOfVirtualApplicationTokenOptionsDef1, OneOfVirtualApplicationTokenOptionsDef2]
    hostname: Optional[
        Union[
            OneOfVirtualApplicationHostnameOptionsDef1,
            OneOfVirtualApplicationHostnameOptionsDef2,
            OneOfVirtualApplicationHostnameOptionsDef3,
        ]
    ] = _field(default=None)
    name_server: Optional[
        Union[
            OneOfVirtualApplicationNameServerOptionsDef1,
            OneOfVirtualApplicationNameServerOptionsDef2,
            OneOfVirtualApplicationNameServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nameServer"})
    te_mgmt_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None, metadata={"alias": "teMgmtIp"}
    )
    te_mgmt_subnet_mask: Optional[
        Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]
    ] = _field(default=None, metadata={"alias": "teMgmtSubnetMask"})
    te_vpg_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None, metadata={"alias": "teVpgIp"}
    )
    vpn: Optional[
        Union[
            OneOfVirtualApplicationVpnOptionsDef1,
            OneOfVirtualApplicationVpnOptionsDef2,
            OneOfVirtualApplicationVpnOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class ThousandeyesData:
    # Virtual application Instance
    virtual_application: Optional[List[Union[VirtualApplication1, VirtualApplication2]]] = _field(
        default=None, metadata={"alias": "virtualApplication"}
    )


@dataclass
class Payload:
    """
    thousandeyes profile parcel schema for POST request
    """

    data: ThousandeyesData
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
    # thousandeyes profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanOtherThousandeyesPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateThousandeyesProfileParcelForOtherPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OtherThousandeyesData:
    # Virtual application Instance
    virtual_application: Optional[List[Union[VirtualApplication1, VirtualApplication2]]] = _field(
        default=None, metadata={"alias": "virtualApplication"}
    )


@dataclass
class CreateThousandeyesProfileParcelForOtherPostRequest:
    """
    thousandeyes profile parcel schema for POST request
    """

    data: OtherThousandeyesData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class ThousandeyesOneOfVirtualApplicationTokenOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ThousandeyesOneOfVirtualApplicationNameServerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ThousandeyesOneOfVirtualApplicationHostnameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ThousandeyesOneOfVirtualApplicationProxyHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ThousandeyesProxyConfig1:
    proxy_host: Union[
        ThousandeyesOneOfVirtualApplicationProxyHostOptionsDef1,
        OneOfVirtualApplicationProxyHostOptionsDef2,
    ] = _field(metadata={"alias": "proxyHost"})
    proxy_port: Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2] = _field(
        metadata={"alias": "proxyPort"}
    )
    # Select Web Proxy Type
    proxy_type: ProxyType = _field(metadata={"alias": "proxyType"})


@dataclass
class SdwanOtherThousandeyesProxyType:
    """
    Select Web Proxy Type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class ThousandeyesOneOfVirtualApplicationPacUrlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ThousandeyesProxyConfig2:
    pac_url: Union[
        ThousandeyesOneOfVirtualApplicationPacUrlOptionsDef1,
        OneOfVirtualApplicationPacUrlOptionsDef2,
    ] = _field(metadata={"alias": "pacUrl"})
    # Select Web Proxy Type
    proxy_type: SdwanOtherThousandeyesProxyType = _field(metadata={"alias": "proxyType"})


@dataclass
class ThousandeyesVirtualApplication1:
    # Web Proxy Type Config
    proxy_config: Union[ThousandeyesProxyConfig1, ThousandeyesProxyConfig2, ProxyConfig3] = _field(
        metadata={"alias": "proxyConfig"}
    )
    token: Union[
        ThousandeyesOneOfVirtualApplicationTokenOptionsDef1, OneOfVirtualApplicationTokenOptionsDef2
    ]
    hostname: Optional[
        Union[
            ThousandeyesOneOfVirtualApplicationHostnameOptionsDef1,
            OneOfVirtualApplicationHostnameOptionsDef2,
            OneOfVirtualApplicationHostnameOptionsDef3,
        ]
    ] = _field(default=None)
    name_server: Optional[
        Union[
            ThousandeyesOneOfVirtualApplicationNameServerOptionsDef1,
            OneOfVirtualApplicationNameServerOptionsDef2,
            OneOfVirtualApplicationNameServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nameServer"})
    te_mgmt_ip: Optional[TeMgmtIp] = _field(default=None, metadata={"alias": "teMgmtIp"})
    te_mgmt_subnet_mask: Optional[TeMgmtSubnetMask] = _field(
        default=None, metadata={"alias": "teMgmtSubnetMask"}
    )
    te_vpg_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None, metadata={"alias": "teVpgIp"}
    )
    vpn: Optional[
        Union[
            OneOfVirtualApplicationVpnOptionsDef1,
            OneOfVirtualApplicationVpnOptionsDef2,
            OneOfVirtualApplicationVpnOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OtherThousandeyesOneOfVirtualApplicationTokenOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OtherThousandeyesOneOfVirtualApplicationNameServerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OtherThousandeyesOneOfVirtualApplicationHostnameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OtherThousandeyesOneOfVirtualApplicationProxyHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OtherThousandeyesProxyConfig1:
    proxy_host: Union[
        OtherThousandeyesOneOfVirtualApplicationProxyHostOptionsDef1,
        OneOfVirtualApplicationProxyHostOptionsDef2,
    ] = _field(metadata={"alias": "proxyHost"})
    proxy_port: Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2] = _field(
        metadata={"alias": "proxyPort"}
    )
    # Select Web Proxy Type
    proxy_type: ProxyType = _field(metadata={"alias": "proxyType"})


@dataclass
class FeatureProfileSdwanOtherThousandeyesProxyType:
    """
    Select Web Proxy Type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OtherThousandeyesOneOfVirtualApplicationPacUrlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OtherThousandeyesProxyConfig2:
    pac_url: Union[
        OtherThousandeyesOneOfVirtualApplicationPacUrlOptionsDef1,
        OneOfVirtualApplicationPacUrlOptionsDef2,
    ] = _field(metadata={"alias": "pacUrl"})
    # Select Web Proxy Type
    proxy_type: FeatureProfileSdwanOtherThousandeyesProxyType = _field(
        metadata={"alias": "proxyType"}
    )


@dataclass
class ThousandeyesVirtualApplication2:
    # Web Proxy Type Config
    proxy_config: Union[
        OtherThousandeyesProxyConfig1, OtherThousandeyesProxyConfig2, ProxyConfig3
    ] = _field(metadata={"alias": "proxyConfig"})
    token: Union[
        OtherThousandeyesOneOfVirtualApplicationTokenOptionsDef1,
        OneOfVirtualApplicationTokenOptionsDef2,
    ]
    hostname: Optional[
        Union[
            OtherThousandeyesOneOfVirtualApplicationHostnameOptionsDef1,
            OneOfVirtualApplicationHostnameOptionsDef2,
            OneOfVirtualApplicationHostnameOptionsDef3,
        ]
    ] = _field(default=None)
    name_server: Optional[
        Union[
            OtherThousandeyesOneOfVirtualApplicationNameServerOptionsDef1,
            OneOfVirtualApplicationNameServerOptionsDef2,
            OneOfVirtualApplicationNameServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nameServer"})
    te_mgmt_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None, metadata={"alias": "teMgmtIp"}
    )
    te_mgmt_subnet_mask: Optional[
        Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]
    ] = _field(default=None, metadata={"alias": "teMgmtSubnetMask"})
    te_vpg_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None, metadata={"alias": "teVpgIp"}
    )
    vpn: Optional[
        Union[
            OneOfVirtualApplicationVpnOptionsDef1,
            OneOfVirtualApplicationVpnOptionsDef2,
            OneOfVirtualApplicationVpnOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class SdwanOtherThousandeyesData:
    # Virtual application Instance
    virtual_application: Optional[
        List[Union[ThousandeyesVirtualApplication1, ThousandeyesVirtualApplication2]]
    ] = _field(default=None, metadata={"alias": "virtualApplication"})


@dataclass
class ThousandeyesPayload:
    """
    thousandeyes profile parcel schema for PUT request
    """

    data: SdwanOtherThousandeyesData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanOtherThousandeyesPayload:
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
    # thousandeyes profile parcel schema for PUT request
    payload: Optional[ThousandeyesPayload] = _field(default=None)


@dataclass
class EditThousandeyesProfileParcelForOtherPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanOtherThousandeyesOneOfVirtualApplicationTokenOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanOtherThousandeyesOneOfVirtualApplicationNameServerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanOtherThousandeyesOneOfVirtualApplicationHostnameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanOtherThousandeyesOneOfVirtualApplicationProxyHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanOtherThousandeyesProxyConfig1:
    proxy_host: Union[
        SdwanOtherThousandeyesOneOfVirtualApplicationProxyHostOptionsDef1,
        OneOfVirtualApplicationProxyHostOptionsDef2,
    ] = _field(metadata={"alias": "proxyHost"})
    proxy_port: Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2] = _field(
        metadata={"alias": "proxyPort"}
    )
    # Select Web Proxy Type
    proxy_type: ProxyType = _field(metadata={"alias": "proxyType"})


@dataclass
class V1FeatureProfileSdwanOtherThousandeyesProxyType:
    """
    Select Web Proxy Type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SdwanOtherThousandeyesOneOfVirtualApplicationPacUrlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanOtherThousandeyesProxyConfig2:
    pac_url: Union[
        SdwanOtherThousandeyesOneOfVirtualApplicationPacUrlOptionsDef1,
        OneOfVirtualApplicationPacUrlOptionsDef2,
    ] = _field(metadata={"alias": "pacUrl"})
    # Select Web Proxy Type
    proxy_type: V1FeatureProfileSdwanOtherThousandeyesProxyType = _field(
        metadata={"alias": "proxyType"}
    )


@dataclass
class OtherThousandeyesVirtualApplication1:
    # Web Proxy Type Config
    proxy_config: Union[
        SdwanOtherThousandeyesProxyConfig1, SdwanOtherThousandeyesProxyConfig2, ProxyConfig3
    ] = _field(metadata={"alias": "proxyConfig"})
    token: Union[
        SdwanOtherThousandeyesOneOfVirtualApplicationTokenOptionsDef1,
        OneOfVirtualApplicationTokenOptionsDef2,
    ]
    hostname: Optional[
        Union[
            SdwanOtherThousandeyesOneOfVirtualApplicationHostnameOptionsDef1,
            OneOfVirtualApplicationHostnameOptionsDef2,
            OneOfVirtualApplicationHostnameOptionsDef3,
        ]
    ] = _field(default=None)
    name_server: Optional[
        Union[
            SdwanOtherThousandeyesOneOfVirtualApplicationNameServerOptionsDef1,
            OneOfVirtualApplicationNameServerOptionsDef2,
            OneOfVirtualApplicationNameServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nameServer"})
    te_mgmt_ip: Optional[TeMgmtIp] = _field(default=None, metadata={"alias": "teMgmtIp"})
    te_mgmt_subnet_mask: Optional[TeMgmtSubnetMask] = _field(
        default=None, metadata={"alias": "teMgmtSubnetMask"}
    )
    te_vpg_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None, metadata={"alias": "teVpgIp"}
    )
    vpn: Optional[
        Union[
            OneOfVirtualApplicationVpnOptionsDef1,
            OneOfVirtualApplicationVpnOptionsDef2,
            OneOfVirtualApplicationVpnOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class FeatureProfileSdwanOtherThousandeyesOneOfVirtualApplicationTokenOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanOtherThousandeyesOneOfVirtualApplicationNameServerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanOtherThousandeyesOneOfVirtualApplicationHostnameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanOtherThousandeyesOneOfVirtualApplicationProxyHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanOtherThousandeyesProxyConfig1:
    proxy_host: Union[
        FeatureProfileSdwanOtherThousandeyesOneOfVirtualApplicationProxyHostOptionsDef1,
        OneOfVirtualApplicationProxyHostOptionsDef2,
    ] = _field(metadata={"alias": "proxyHost"})
    proxy_port: Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2] = _field(
        metadata={"alias": "proxyPort"}
    )
    # Select Web Proxy Type
    proxy_type: ProxyType = _field(metadata={"alias": "proxyType"})


@dataclass
class ProxyType1:
    """
    Select Web Proxy Type
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class FeatureProfileSdwanOtherThousandeyesOneOfVirtualApplicationPacUrlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanOtherThousandeyesProxyConfig2:
    pac_url: Union[
        FeatureProfileSdwanOtherThousandeyesOneOfVirtualApplicationPacUrlOptionsDef1,
        OneOfVirtualApplicationPacUrlOptionsDef2,
    ] = _field(metadata={"alias": "pacUrl"})
    # Select Web Proxy Type
    proxy_type: ProxyType1 = _field(metadata={"alias": "proxyType"})


@dataclass
class OtherThousandeyesVirtualApplication2:
    # Web Proxy Type Config
    proxy_config: Union[
        FeatureProfileSdwanOtherThousandeyesProxyConfig1,
        FeatureProfileSdwanOtherThousandeyesProxyConfig2,
        ProxyConfig3,
    ] = _field(metadata={"alias": "proxyConfig"})
    token: Union[
        FeatureProfileSdwanOtherThousandeyesOneOfVirtualApplicationTokenOptionsDef1,
        OneOfVirtualApplicationTokenOptionsDef2,
    ]
    hostname: Optional[
        Union[
            FeatureProfileSdwanOtherThousandeyesOneOfVirtualApplicationHostnameOptionsDef1,
            OneOfVirtualApplicationHostnameOptionsDef2,
            OneOfVirtualApplicationHostnameOptionsDef3,
        ]
    ] = _field(default=None)
    name_server: Optional[
        Union[
            FeatureProfileSdwanOtherThousandeyesOneOfVirtualApplicationNameServerOptionsDef1,
            OneOfVirtualApplicationNameServerOptionsDef2,
            OneOfVirtualApplicationNameServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nameServer"})
    te_mgmt_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None, metadata={"alias": "teMgmtIp"}
    )
    te_mgmt_subnet_mask: Optional[
        Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]
    ] = _field(default=None, metadata={"alias": "teMgmtSubnetMask"})
    te_vpg_ip: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None, metadata={"alias": "teVpgIp"}
    )
    vpn: Optional[
        Union[
            OneOfVirtualApplicationVpnOptionsDef1,
            OneOfVirtualApplicationVpnOptionsDef2,
            OneOfVirtualApplicationVpnOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class FeatureProfileSdwanOtherThousandeyesData:
    # Virtual application Instance
    virtual_application: Optional[
        List[Union[OtherThousandeyesVirtualApplication1, OtherThousandeyesVirtualApplication2]]
    ] = _field(default=None, metadata={"alias": "virtualApplication"})


@dataclass
class EditThousandeyesProfileParcelForOtherPutRequest:
    """
    thousandeyes profile parcel schema for PUT request
    """

    data: FeatureProfileSdwanOtherThousandeyesData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
