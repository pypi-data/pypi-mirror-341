# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

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

DefaultOptionTypeDef = Literal["default"]


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
class AddressPool:
    """
    Configure IPv4 prefix range of the DHCP address pool
    """

    network_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "networkAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class OneOfExcludeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[Any, Any]]


@dataclass
class OneOfExcludeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfExcludeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLeaseTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfLeaseTimeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLeaseTimeOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


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
class OneOfInterfaceMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDomainNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDomainNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDomainNameOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDefaultGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDefaultGatewayOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDefaultGatewayOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDnsServersOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfDnsServersOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDnsServersOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTftpServersOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfTftpServersOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTftpServersOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfStaticLeaseMacAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfStaticLeaseMacAddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticLeaseIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfStaticLeaseIpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class StaticLease:
    ip: Union[OneOfStaticLeaseIpOptionsDef1, OneOfStaticLeaseIpOptionsDef2]
    mac_address: Union[
        OneOfStaticLeaseMacAddressOptionsDef1, OneOfStaticLeaseMacAddressOptionsDef2
    ] = _field(metadata={"alias": "macAddress"})


@dataclass
class OneOfOptionCodeCodeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfOptionCodeCodeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOptionCodeAsciiOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfOptionCodeAsciiOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OptionCode1:
    ascii: Union[OneOfOptionCodeAsciiOptionsDef1, OneOfOptionCodeAsciiOptionsDef2]
    code: Union[OneOfOptionCodeCodeOptionsDef1, OneOfOptionCodeCodeOptionsDef2]


@dataclass
class OneOfOptionCodeHexOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfOptionCodeHexOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OptionCode2:
    code: Union[OneOfOptionCodeCodeOptionsDef1, OneOfOptionCodeCodeOptionsDef2]
    hex: Union[OneOfOptionCodeHexOptionsDef1, OneOfOptionCodeHexOptionsDef2]


@dataclass
class OneOfOptionCodeIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfOptionCodeIpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OptionCode3:
    code: Union[OneOfOptionCodeCodeOptionsDef1, OneOfOptionCodeCodeOptionsDef2]
    ip: Union[OneOfOptionCodeIpOptionsDef1, OneOfOptionCodeIpOptionsDef2]


@dataclass
class Data:
    # Configure IPv4 prefix range of the DHCP address pool
    address_pool: AddressPool = _field(metadata={"alias": "addressPool"})
    default_gateway: Optional[
        Union[
            OneOfDefaultGatewayOptionsDef1,
            OneOfDefaultGatewayOptionsDef2,
            OneOfDefaultGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "defaultGateway"})
    dns_servers: Optional[
        Union[OneOfDnsServersOptionsDef1, OneOfDnsServersOptionsDef2, OneOfDnsServersOptionsDef3]
    ] = _field(default=None, metadata={"alias": "dnsServers"})
    domain_name: Optional[
        Union[OneOfDomainNameOptionsDef1, OneOfDomainNameOptionsDef2, OneOfDomainNameOptionsDef3]
    ] = _field(default=None, metadata={"alias": "domainName"})
    exclude: Optional[
        Union[OneOfExcludeOptionsDef1, OneOfExcludeOptionsDef2, OneOfExcludeOptionsDef3]
    ] = _field(default=None)
    interface_mtu: Optional[
        Union[
            OneOfInterfaceMtuOptionsDef1, OneOfInterfaceMtuOptionsDef2, OneOfInterfaceMtuOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "interfaceMtu"})
    lease_time: Optional[
        Union[OneOfLeaseTimeOptionsDef1, OneOfLeaseTimeOptionsDef2, OneOfLeaseTimeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "leaseTime"})
    # Configure Options Code
    option_code: Optional[List[Union[OptionCode1, OptionCode2, OptionCode3]]] = _field(
        default=None, metadata={"alias": "optionCode"}
    )
    # Configure static IP addresses
    static_lease: Optional[List[StaticLease]] = _field(
        default=None, metadata={"alias": "staticLease"}
    )
    tftp_servers: Optional[
        Union[OneOfTftpServersOptionsDef1, OneOfTftpServersOptionsDef2, OneOfTftpServersOptionsDef3]
    ] = _field(default=None, metadata={"alias": "tftpServers"})


@dataclass
class Payload:
    """
    LAN VPN DHCP Server profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetLanVpnInterfaceEthernetAssociatedDhcpServerParcelsForTransportGetResponse:
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
    # LAN VPN DHCP Server profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class DhcpServerOneOfExcludeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[Any, Any]]


@dataclass
class DhcpServerOneOfLeaseTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class DhcpServerOneOfLeaseTimeOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class DhcpServerOneOfInterfaceMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class DhcpServerOneOfDomainNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class DhcpServerOneOfDefaultGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class DhcpServerOneOfDnsServersOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class DhcpServerOneOfTftpServersOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class DhcpServerOneOfStaticLeaseMacAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class DhcpServerOneOfStaticLeaseIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class DhcpServerStaticLease:
    ip: Union[DhcpServerOneOfStaticLeaseIpOptionsDef1, OneOfStaticLeaseIpOptionsDef2]
    mac_address: Union[
        DhcpServerOneOfStaticLeaseMacAddressOptionsDef1, OneOfStaticLeaseMacAddressOptionsDef2
    ] = _field(metadata={"alias": "macAddress"})


@dataclass
class DhcpServerOneOfOptionCodeCodeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class DhcpServerOneOfOptionCodeAsciiOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class DhcpServerOptionCode1:
    ascii: Union[DhcpServerOneOfOptionCodeAsciiOptionsDef1, OneOfOptionCodeAsciiOptionsDef2]
    code: Union[DhcpServerOneOfOptionCodeCodeOptionsDef1, OneOfOptionCodeCodeOptionsDef2]


@dataclass
class EthernetDhcpServerOneOfOptionCodeCodeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class DhcpServerOneOfOptionCodeHexOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class DhcpServerOptionCode2:
    code: Union[EthernetDhcpServerOneOfOptionCodeCodeOptionsDef1, OneOfOptionCodeCodeOptionsDef2]
    hex: Union[DhcpServerOneOfOptionCodeHexOptionsDef1, OneOfOptionCodeHexOptionsDef2]


@dataclass
class InterfaceEthernetDhcpServerOneOfOptionCodeCodeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class DhcpServerOneOfOptionCodeIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class DhcpServerOptionCode3:
    code: Union[
        InterfaceEthernetDhcpServerOneOfOptionCodeCodeOptionsDef1, OneOfOptionCodeCodeOptionsDef2
    ]
    ip: Union[DhcpServerOneOfOptionCodeIpOptionsDef1, OneOfOptionCodeIpOptionsDef2]


@dataclass
class DhcpServerData:
    # Configure IPv4 prefix range of the DHCP address pool
    address_pool: AddressPool = _field(metadata={"alias": "addressPool"})
    default_gateway: Optional[
        Union[
            DhcpServerOneOfDefaultGatewayOptionsDef1,
            OneOfDefaultGatewayOptionsDef2,
            OneOfDefaultGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "defaultGateway"})
    dns_servers: Optional[
        Union[
            DhcpServerOneOfDnsServersOptionsDef1,
            OneOfDnsServersOptionsDef2,
            OneOfDnsServersOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dnsServers"})
    domain_name: Optional[
        Union[
            DhcpServerOneOfDomainNameOptionsDef1,
            OneOfDomainNameOptionsDef2,
            OneOfDomainNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "domainName"})
    exclude: Optional[
        Union[DhcpServerOneOfExcludeOptionsDef1, OneOfExcludeOptionsDef2, OneOfExcludeOptionsDef3]
    ] = _field(default=None)
    interface_mtu: Optional[
        Union[
            DhcpServerOneOfInterfaceMtuOptionsDef1,
            OneOfInterfaceMtuOptionsDef2,
            OneOfInterfaceMtuOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "interfaceMtu"})
    lease_time: Optional[
        Union[
            DhcpServerOneOfLeaseTimeOptionsDef1,
            OneOfLeaseTimeOptionsDef2,
            DhcpServerOneOfLeaseTimeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "leaseTime"})
    # Configure Options Code
    option_code: Optional[
        List[Union[DhcpServerOptionCode1, DhcpServerOptionCode2, DhcpServerOptionCode3]]
    ] = _field(default=None, metadata={"alias": "optionCode"})
    # Configure static IP addresses
    static_lease: Optional[List[DhcpServerStaticLease]] = _field(
        default=None, metadata={"alias": "staticLease"}
    )
    tftp_servers: Optional[
        Union[
            DhcpServerOneOfTftpServersOptionsDef1,
            OneOfTftpServersOptionsDef2,
            OneOfTftpServersOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tftpServers"})


@dataclass
class DhcpServerPayload:
    """
    LAN VPN DHCP Server profile parcel schema for PUT request
    """

    data: DhcpServerData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanServiceLanVpnInterfaceEthernetDhcpServerPayload:
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
    # LAN VPN DHCP Server profile parcel schema for PUT request
    payload: Optional[DhcpServerPayload] = _field(default=None)


@dataclass
class EditLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EditLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPutRequest:
    """
    Profile Parcel POST Request schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateLanVpnInterfaceEthernetAndDhcpServerParcelAssociationForTransportPostRequest:
    """
    Profile Parcel POST Request schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)
