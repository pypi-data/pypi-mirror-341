# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

IpsecReplayWindowDef = Literal["1024", "128", "256", "512", "64"]

DefaultIpsecReplayWindowDef = Literal["64"]

PfsGroupDef = Literal["14", "15", "16", "19", "20", "21"]

DefaultPfsGroupDef = Literal["16"]

SignatureTypeDef = Literal["ECDSA", "RSA"]

DefaultSignatureTypeDef = Literal["RSA"]


@dataclass
class OneOfDpdIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDpdIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDpdIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDpdRetryIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDpdRetryIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDpdRetryIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIkeSaLifeTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIkeSaLifeTimeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeSaLifeTimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpV4AddressOptionsWithoutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4AddressOptionsWithoutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfIkeV2LocalIdentityOptionsDef1:
    ipv4_addr: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipv4Addr"})


@dataclass
class OneOfIpv6NextHopAddressOptionsWithOutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6NextHopAddressOptionsWithOutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIkeV2LocalIdentityOptionsDef2:
    ipv6_addr: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ] = _field(metadata={"alias": "ipv6Addr"})


@dataclass
class OneOfIdentityValueFqdnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIdentityValueFqdnOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeV2LocalIdentityOptionsDef3:
    fqdn: Union[OneOfIdentityValueFqdnOptionsDef1, OneOfIdentityValueFqdnOptionsDef2]


@dataclass
class OneOfIdentityValueEmailOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIdentityValueEmailOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeV2LocalIdentityOptionsDef4:
    email: Union[OneOfIdentityValueEmailOptionsDef1, OneOfIdentityValueEmailOptionsDef2]


@dataclass
class OneOfIdentityValueKeyIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIdentityValueKeyIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeV2LocalIdentityOptionsDef5:
    key_id: Union[OneOfIdentityValueKeyIdOptionsDef1, OneOfIdentityValueKeyIdOptionsDef2] = _field(
        metadata={"alias": "keyId"}
    )


@dataclass
class RemoteIdentities1:
    ipv4_addr: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipv4Addr"})


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
class RemoteIdentities2:
    ipv6_prefix: Union[
        OneOfIpv6PrefixGlobalVariableWithoutDefault1, OneOfIpv6PrefixGlobalVariableWithoutDefault2
    ] = _field(metadata={"alias": "ipv6Prefix"})


@dataclass
class RemoteIdentities3:
    fqdn: Union[OneOfIdentityValueFqdnOptionsDef1, OneOfIdentityValueFqdnOptionsDef2]


@dataclass
class RemoteIdentities4:
    email: Union[OneOfIdentityValueEmailOptionsDef1, OneOfIdentityValueEmailOptionsDef2]


@dataclass
class RemoteIdentities5:
    key_id: Union[OneOfIdentityValueKeyIdOptionsDef1, OneOfIdentityValueKeyIdOptionsDef2] = _field(
        metadata={"alias": "keyId"}
    )


@dataclass
class OneOfIpsecSaLifeTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpsecSaLifeTimeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpsecSaLifeTimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpsecReplayWindowOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IpsecReplayWindowDef


@dataclass
class OneOfIpsecReplayWindowOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpsecReplayWindowOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultIpsecReplayWindowDef  # pytype: disable=annotation-type-mismatch


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
class OneOfPfsGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PfsGroupDef


@dataclass
class OneOfPfsGroupOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPfsGroupOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultPfsGroupDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPreSharedKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPreSharedKeyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeV2AuthConfigOptionsDef1:
    group_psk: Union[OneOfPreSharedKeyOptionsDef1, OneOfPreSharedKeyOptionsDef2] = _field(
        metadata={"alias": "groupPsk"}
    )


@dataclass
class OneOfKeyringPeerNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PeerIPv4AddressOrSubnetMaskOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class PeerIPv4AddressOrSubnetMaskOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkev2KeyringPeerAddressOptionsDef1:
    ipv4_address_or_subnet: Union[
        PeerIPv4AddressOrSubnetMaskOptionsDef1, PeerIPv4AddressOrSubnetMaskOptionsDef2
    ] = _field(metadata={"alias": "ipv4AddressOrSubnet"})


@dataclass
class OneOfIkev2KeyringPeerAddressOptionsDef2:
    ipv6_prefix: Union[
        OneOfIpv6PrefixGlobalVariableWithoutDefault1, OneOfIpv6PrefixGlobalVariableWithoutDefault2
    ] = _field(metadata={"alias": "ipv6Prefix"})


@dataclass
class OneOfIkev2KeyringPeerAddressOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfKeyringPeerHostNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfKeyringPeerHostNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfKeyringPeerHostNameOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIPeerIdentityOptionsDef1:
    ipv4_addr: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipv4Addr"})


@dataclass
class OneOfIPeerIdentityOptionsDef2:
    ipv6_addr: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ] = _field(metadata={"alias": "ipv6Addr"})


@dataclass
class OneOfIPeerIdentityOptionsDef3:
    fqdn: Union[OneOfIdentityValueFqdnOptionsDef1, OneOfIdentityValueFqdnOptionsDef2]


@dataclass
class OneOfIPeerIdentityOptionsDef4:
    email: Union[OneOfIdentityValueEmailOptionsDef1, OneOfIdentityValueEmailOptionsDef2]


@dataclass
class OneOfIPeerIdentityOptionsDef5:
    key_id: Union[OneOfIdentityValueKeyIdOptionsDef1, OneOfIdentityValueKeyIdOptionsDef2] = _field(
        metadata={"alias": "keyId"}
    )


@dataclass
class OneOfIPeerIdentityOptionsDef6:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Peers1:
    address_config: Union[
        OneOfIkev2KeyringPeerAddressOptionsDef1,
        OneOfIkev2KeyringPeerAddressOptionsDef2,
        OneOfIkev2KeyringPeerAddressOptionsDef3,
    ] = _field(metadata={"alias": "addressConfig"})
    peer_name: OneOfKeyringPeerNameOptionsDef = _field(metadata={"alias": "peerName"})
    pre_shared_key: Union[OneOfPreSharedKeyOptionsDef1, OneOfPreSharedKeyOptionsDef2] = _field(
        metadata={"alias": "preSharedKey"}
    )
    host_name: Optional[
        Union[
            OneOfKeyringPeerHostNameOptionsDef1,
            OneOfKeyringPeerHostNameOptionsDef2,
            OneOfKeyringPeerHostNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "hostName"})
    identity: Optional[
        Union[
            OneOfIPeerIdentityOptionsDef1,
            OneOfIPeerIdentityOptionsDef2,
            OneOfIPeerIdentityOptionsDef3,
            OneOfIPeerIdentityOptionsDef4,
            OneOfIPeerIdentityOptionsDef5,
            OneOfIPeerIdentityOptionsDef6,
        ]
    ] = _field(default=None)


@dataclass
class Peers2:
    host_name: Union[
        OneOfKeyringPeerHostNameOptionsDef1,
        OneOfKeyringPeerHostNameOptionsDef2,
        OneOfKeyringPeerHostNameOptionsDef3,
    ] = _field(metadata={"alias": "hostName"})
    peer_name: OneOfKeyringPeerNameOptionsDef = _field(metadata={"alias": "peerName"})
    pre_shared_key: Union[OneOfPreSharedKeyOptionsDef1, OneOfPreSharedKeyOptionsDef2] = _field(
        metadata={"alias": "preSharedKey"}
    )
    address_config: Optional[
        Union[
            OneOfIkev2KeyringPeerAddressOptionsDef1,
            OneOfIkev2KeyringPeerAddressOptionsDef2,
            OneOfIkev2KeyringPeerAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "addressConfig"})
    identity: Optional[
        Union[
            OneOfIPeerIdentityOptionsDef1,
            OneOfIPeerIdentityOptionsDef2,
            OneOfIPeerIdentityOptionsDef3,
            OneOfIPeerIdentityOptionsDef4,
            OneOfIPeerIdentityOptionsDef5,
            OneOfIPeerIdentityOptionsDef6,
        ]
    ] = _field(default=None)


@dataclass
class Peers3:
    identity: Union[
        OneOfIPeerIdentityOptionsDef1,
        OneOfIPeerIdentityOptionsDef2,
        OneOfIPeerIdentityOptionsDef3,
        OneOfIPeerIdentityOptionsDef4,
        OneOfIPeerIdentityOptionsDef5,
        OneOfIPeerIdentityOptionsDef6,
    ]
    peer_name: OneOfKeyringPeerNameOptionsDef = _field(metadata={"alias": "peerName"})
    pre_shared_key: Union[OneOfPreSharedKeyOptionsDef1, OneOfPreSharedKeyOptionsDef2] = _field(
        metadata={"alias": "preSharedKey"}
    )
    address_config: Optional[
        Union[
            OneOfIkev2KeyringPeerAddressOptionsDef1,
            OneOfIkev2KeyringPeerAddressOptionsDef2,
            OneOfIkev2KeyringPeerAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "addressConfig"})
    host_name: Optional[
        Union[
            OneOfKeyringPeerHostNameOptionsDef1,
            OneOfKeyringPeerHostNameOptionsDef2,
            OneOfKeyringPeerHostNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "hostName"})


@dataclass
class Peers4:
    address_config: Union[
        OneOfIkev2KeyringPeerAddressOptionsDef1,
        OneOfIkev2KeyringPeerAddressOptionsDef2,
        OneOfIkev2KeyringPeerAddressOptionsDef3,
    ] = _field(metadata={"alias": "addressConfig"})
    host_name: Union[
        OneOfKeyringPeerHostNameOptionsDef1,
        OneOfKeyringPeerHostNameOptionsDef2,
        OneOfKeyringPeerHostNameOptionsDef3,
    ] = _field(metadata={"alias": "hostName"})
    peer_name: OneOfKeyringPeerNameOptionsDef = _field(metadata={"alias": "peerName"})
    pre_shared_key: Union[OneOfPreSharedKeyOptionsDef1, OneOfPreSharedKeyOptionsDef2] = _field(
        metadata={"alias": "preSharedKey"}
    )
    identity: Optional[
        Union[
            OneOfIPeerIdentityOptionsDef1,
            OneOfIPeerIdentityOptionsDef2,
            OneOfIPeerIdentityOptionsDef3,
            OneOfIPeerIdentityOptionsDef4,
            OneOfIPeerIdentityOptionsDef5,
            OneOfIPeerIdentityOptionsDef6,
        ]
    ] = _field(default=None)


@dataclass
class Peers5:
    address_config: Union[
        OneOfIkev2KeyringPeerAddressOptionsDef1,
        OneOfIkev2KeyringPeerAddressOptionsDef2,
        OneOfIkev2KeyringPeerAddressOptionsDef3,
    ] = _field(metadata={"alias": "addressConfig"})
    identity: Union[
        OneOfIPeerIdentityOptionsDef1,
        OneOfIPeerIdentityOptionsDef2,
        OneOfIPeerIdentityOptionsDef3,
        OneOfIPeerIdentityOptionsDef4,
        OneOfIPeerIdentityOptionsDef5,
        OneOfIPeerIdentityOptionsDef6,
    ]
    peer_name: OneOfKeyringPeerNameOptionsDef = _field(metadata={"alias": "peerName"})
    pre_shared_key: Union[OneOfPreSharedKeyOptionsDef1, OneOfPreSharedKeyOptionsDef2] = _field(
        metadata={"alias": "preSharedKey"}
    )
    host_name: Optional[
        Union[
            OneOfKeyringPeerHostNameOptionsDef1,
            OneOfKeyringPeerHostNameOptionsDef2,
            OneOfKeyringPeerHostNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "hostName"})


@dataclass
class Peers6:
    host_name: Union[
        OneOfKeyringPeerHostNameOptionsDef1,
        OneOfKeyringPeerHostNameOptionsDef2,
        OneOfKeyringPeerHostNameOptionsDef3,
    ] = _field(metadata={"alias": "hostName"})
    identity: Union[
        OneOfIPeerIdentityOptionsDef1,
        OneOfIPeerIdentityOptionsDef2,
        OneOfIPeerIdentityOptionsDef3,
        OneOfIPeerIdentityOptionsDef4,
        OneOfIPeerIdentityOptionsDef5,
        OneOfIPeerIdentityOptionsDef6,
    ]
    peer_name: OneOfKeyringPeerNameOptionsDef = _field(metadata={"alias": "peerName"})
    pre_shared_key: Union[OneOfPreSharedKeyOptionsDef1, OneOfPreSharedKeyOptionsDef2] = _field(
        metadata={"alias": "preSharedKey"}
    )
    address_config: Optional[
        Union[
            OneOfIkev2KeyringPeerAddressOptionsDef1,
            OneOfIkev2KeyringPeerAddressOptionsDef2,
            OneOfIkev2KeyringPeerAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "addressConfig"})


@dataclass
class Peers7:
    address_config: Union[
        OneOfIkev2KeyringPeerAddressOptionsDef1,
        OneOfIkev2KeyringPeerAddressOptionsDef2,
        OneOfIkev2KeyringPeerAddressOptionsDef3,
    ] = _field(metadata={"alias": "addressConfig"})
    host_name: Union[
        OneOfKeyringPeerHostNameOptionsDef1,
        OneOfKeyringPeerHostNameOptionsDef2,
        OneOfKeyringPeerHostNameOptionsDef3,
    ] = _field(metadata={"alias": "hostName"})
    identity: Union[
        OneOfIPeerIdentityOptionsDef1,
        OneOfIPeerIdentityOptionsDef2,
        OneOfIPeerIdentityOptionsDef3,
        OneOfIPeerIdentityOptionsDef4,
        OneOfIPeerIdentityOptionsDef5,
        OneOfIPeerIdentityOptionsDef6,
    ]
    peer_name: OneOfKeyringPeerNameOptionsDef = _field(metadata={"alias": "peerName"})
    pre_shared_key: Union[OneOfPreSharedKeyOptionsDef1, OneOfPreSharedKeyOptionsDef2] = _field(
        metadata={"alias": "preSharedKey"}
    )


@dataclass
class PerPeerPskAuth:
    """
    Per-peer pre-shared key authentication, different peer use different key
    """

    # PSK authentication for different peers, peerName and preSharedKey are mandatory,addressConfig, hostName and identity at least configure one.
    peers: List[Union[Peers1, Peers2, Peers3, Peers4, Peers5, Peers6, Peers7]]


@dataclass
class OneOfIkeV2AuthConfigOptionsDef2:
    # Per-peer pre-shared key authentication, different peer use different key
    per_peer_psk_auth: PerPeerPskAuth = _field(metadata={"alias": "perPeerPskAuth"})


@dataclass
class OneOfTrustPointNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTrustPointNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSignatureTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SignatureTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSignatureTypeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSignatureTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultSignatureTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EnterpriseCaAuth:
    """
    Enterprise CA authentication
    """

    trust_point: Union[OneOfTrustPointNameOptionsDef1, OneOfTrustPointNameOptionsDef2] = _field(
        metadata={"alias": "trustPoint"}
    )
    signature_type: Optional[
        Union[
            OneOfSignatureTypeOptionsDef1,
            OneOfSignatureTypeOptionsDef2,
            OneOfSignatureTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "signatureType"})


@dataclass
class OneOfIkeV2AuthConfigOptionsDef3:
    # Enterprise CA authentication
    enterprise_ca_auth: EnterpriseCaAuth = _field(metadata={"alias": "enterpriseCaAuth"})


@dataclass
class IpsecProfileData:
    """
    IKEv2 and IPSec profile config parameters
    """

    auth_config: Union[
        OneOfIkeV2AuthConfigOptionsDef1,
        OneOfIkeV2AuthConfigOptionsDef2,
        OneOfIkeV2AuthConfigOptionsDef3,
    ] = _field(metadata={"alias": "authConfig"})
    dpd_keep_alive_interval: Union[
        OneOfDpdIntervalOptionsDef1, OneOfDpdIntervalOptionsDef2, OneOfDpdIntervalOptionsDef3
    ] = _field(metadata={"alias": "dpdKeepAliveInterval"})
    dpd_retry_interval: Union[
        OneOfDpdRetryIntervalOptionsDef1,
        OneOfDpdRetryIntervalOptionsDef2,
        OneOfDpdRetryIntervalOptionsDef3,
    ] = _field(metadata={"alias": "dpdRetryInterval"})
    ike_sa_life_time: Union[
        OneOfIkeSaLifeTimeOptionsDef1, OneOfIkeSaLifeTimeOptionsDef2, OneOfIkeSaLifeTimeOptionsDef3
    ] = _field(metadata={"alias": "ikeSaLifeTime"})
    ipsec_replay_window: Union[
        OneOfIpsecReplayWindowOptionsDef1,
        OneOfIpsecReplayWindowOptionsDef2,
        OneOfIpsecReplayWindowOptionsDef3,
    ] = _field(metadata={"alias": "ipsecReplayWindow"})
    ipsec_sa_life_time: Union[
        OneOfIpsecSaLifeTimeOptionsDef1,
        OneOfIpsecSaLifeTimeOptionsDef2,
        OneOfIpsecSaLifeTimeOptionsDef3,
    ] = _field(metadata={"alias": "ipsecSaLifeTime"})
    local_identity: Union[
        OneOfIkeV2LocalIdentityOptionsDef1,
        OneOfIkeV2LocalIdentityOptionsDef2,
        OneOfIkeV2LocalIdentityOptionsDef3,
        OneOfIkeV2LocalIdentityOptionsDef4,
        OneOfIkeV2LocalIdentityOptionsDef5,
    ] = _field(metadata={"alias": "localIdentity"})
    pfs_enabled: Union[
        OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
        OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
    ] = _field(metadata={"alias": "pfsEnabled"})
    # IKE matched remote identity list, at least one configured
    remote_identities: List[
        Union[
            RemoteIdentities1,
            RemoteIdentities2,
            RemoteIdentities3,
            RemoteIdentities4,
            RemoteIdentities5,
        ]
    ] = _field(metadata={"alias": "remoteIdentities"})
    pfs_group: Optional[
        Union[OneOfPfsGroupOptionsDef1, OneOfPfsGroupOptionsDef2, OneOfPfsGroupOptionsDef3]
    ] = _field(default=None, metadata={"alias": "pfsGroup"})


@dataclass
class Payload:
    """
    IPsec Profile feature schema for POST/PUT request
    """

    # IKEv2 and IPSec profile config parameters
    data: IpsecProfileData
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
    # IPsec Profile feature schema for POST/PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingServiceIpsecProfilePayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingServiceIpsecProfileFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ServiceIpsecProfileData:
    """
    IKEv2 and IPSec profile config parameters
    """

    auth_config: Union[
        OneOfIkeV2AuthConfigOptionsDef1,
        OneOfIkeV2AuthConfigOptionsDef2,
        OneOfIkeV2AuthConfigOptionsDef3,
    ] = _field(metadata={"alias": "authConfig"})
    dpd_keep_alive_interval: Union[
        OneOfDpdIntervalOptionsDef1, OneOfDpdIntervalOptionsDef2, OneOfDpdIntervalOptionsDef3
    ] = _field(metadata={"alias": "dpdKeepAliveInterval"})
    dpd_retry_interval: Union[
        OneOfDpdRetryIntervalOptionsDef1,
        OneOfDpdRetryIntervalOptionsDef2,
        OneOfDpdRetryIntervalOptionsDef3,
    ] = _field(metadata={"alias": "dpdRetryInterval"})
    ike_sa_life_time: Union[
        OneOfIkeSaLifeTimeOptionsDef1, OneOfIkeSaLifeTimeOptionsDef2, OneOfIkeSaLifeTimeOptionsDef3
    ] = _field(metadata={"alias": "ikeSaLifeTime"})
    ipsec_replay_window: Union[
        OneOfIpsecReplayWindowOptionsDef1,
        OneOfIpsecReplayWindowOptionsDef2,
        OneOfIpsecReplayWindowOptionsDef3,
    ] = _field(metadata={"alias": "ipsecReplayWindow"})
    ipsec_sa_life_time: Union[
        OneOfIpsecSaLifeTimeOptionsDef1,
        OneOfIpsecSaLifeTimeOptionsDef2,
        OneOfIpsecSaLifeTimeOptionsDef3,
    ] = _field(metadata={"alias": "ipsecSaLifeTime"})
    local_identity: Union[
        OneOfIkeV2LocalIdentityOptionsDef1,
        OneOfIkeV2LocalIdentityOptionsDef2,
        OneOfIkeV2LocalIdentityOptionsDef3,
        OneOfIkeV2LocalIdentityOptionsDef4,
        OneOfIkeV2LocalIdentityOptionsDef5,
    ] = _field(metadata={"alias": "localIdentity"})
    pfs_enabled: Union[
        OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
        OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
    ] = _field(metadata={"alias": "pfsEnabled"})
    # IKE matched remote identity list, at least one configured
    remote_identities: List[
        Union[
            RemoteIdentities1,
            RemoteIdentities2,
            RemoteIdentities3,
            RemoteIdentities4,
            RemoteIdentities5,
        ]
    ] = _field(metadata={"alias": "remoteIdentities"})
    pfs_group: Optional[
        Union[OneOfPfsGroupOptionsDef1, OneOfPfsGroupOptionsDef2, OneOfPfsGroupOptionsDef3]
    ] = _field(default=None, metadata={"alias": "pfsGroup"})


@dataclass
class CreateSdroutingServiceIpsecProfileFeaturePostRequest:
    """
    IPsec Profile feature schema for POST/PUT request
    """

    # IKEv2 and IPSec profile config parameters
    data: ServiceIpsecProfileData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdRoutingServiceIpsecProfilePayload:
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
    # IPsec Profile feature schema for POST/PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingServiceIpsecProfileFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingServiceIpsecProfileData:
    """
    IKEv2 and IPSec profile config parameters
    """

    auth_config: Union[
        OneOfIkeV2AuthConfigOptionsDef1,
        OneOfIkeV2AuthConfigOptionsDef2,
        OneOfIkeV2AuthConfigOptionsDef3,
    ] = _field(metadata={"alias": "authConfig"})
    dpd_keep_alive_interval: Union[
        OneOfDpdIntervalOptionsDef1, OneOfDpdIntervalOptionsDef2, OneOfDpdIntervalOptionsDef3
    ] = _field(metadata={"alias": "dpdKeepAliveInterval"})
    dpd_retry_interval: Union[
        OneOfDpdRetryIntervalOptionsDef1,
        OneOfDpdRetryIntervalOptionsDef2,
        OneOfDpdRetryIntervalOptionsDef3,
    ] = _field(metadata={"alias": "dpdRetryInterval"})
    ike_sa_life_time: Union[
        OneOfIkeSaLifeTimeOptionsDef1, OneOfIkeSaLifeTimeOptionsDef2, OneOfIkeSaLifeTimeOptionsDef3
    ] = _field(metadata={"alias": "ikeSaLifeTime"})
    ipsec_replay_window: Union[
        OneOfIpsecReplayWindowOptionsDef1,
        OneOfIpsecReplayWindowOptionsDef2,
        OneOfIpsecReplayWindowOptionsDef3,
    ] = _field(metadata={"alias": "ipsecReplayWindow"})
    ipsec_sa_life_time: Union[
        OneOfIpsecSaLifeTimeOptionsDef1,
        OneOfIpsecSaLifeTimeOptionsDef2,
        OneOfIpsecSaLifeTimeOptionsDef3,
    ] = _field(metadata={"alias": "ipsecSaLifeTime"})
    local_identity: Union[
        OneOfIkeV2LocalIdentityOptionsDef1,
        OneOfIkeV2LocalIdentityOptionsDef2,
        OneOfIkeV2LocalIdentityOptionsDef3,
        OneOfIkeV2LocalIdentityOptionsDef4,
        OneOfIkeV2LocalIdentityOptionsDef5,
    ] = _field(metadata={"alias": "localIdentity"})
    pfs_enabled: Union[
        OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
        OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
    ] = _field(metadata={"alias": "pfsEnabled"})
    # IKE matched remote identity list, at least one configured
    remote_identities: List[
        Union[
            RemoteIdentities1,
            RemoteIdentities2,
            RemoteIdentities3,
            RemoteIdentities4,
            RemoteIdentities5,
        ]
    ] = _field(metadata={"alias": "remoteIdentities"})
    pfs_group: Optional[
        Union[OneOfPfsGroupOptionsDef1, OneOfPfsGroupOptionsDef2, OneOfPfsGroupOptionsDef3]
    ] = _field(default=None, metadata={"alias": "pfsGroup"})


@dataclass
class EditSdroutingServiceIpsecProfileFeaturePutRequest:
    """
    IPsec Profile feature schema for POST/PUT request
    """

    # IKEv2 and IPSec profile config parameters
    data: SdRoutingServiceIpsecProfileData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
