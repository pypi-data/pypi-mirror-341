# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

UserPrivilegeDef = Literal["1", "15"]

DefaultUserPrivilegeDef = Literal["15"]

UserPubkeyChainKeyTypeDef = Literal["ssh-rsa"]

RadiusServerKeyEnumDef = Literal["6", "7"]

RadiusServerKeyTypeDef = Literal["key", "pac"]

DefaultRadiusServerKeyTypeDef = Literal["key"]

TacacsServerKeyEnumDef = Literal["6", "7"]

AccountingRuleMethodDef = Literal["commands", "exec", "network", "system"]

AccountingRuleLevelDef = Literal["1", "15"]

AuthorizationRuleMethodDef = Literal["commands"]

AuthorizationRuleLevelDef = Literal["1", "15"]

AaaUserPrivilegeDef = Literal["1", "15"]

AaaDefaultUserPrivilegeDef = Literal["15"]

AaaUserPubkeyChainKeyTypeDef = Literal["ssh-rsa"]

AaaRadiusServerKeyEnumDef = Literal["6", "7"]

AaaRadiusServerKeyTypeDef = Literal["key", "pac"]

AaaDefaultRadiusServerKeyTypeDef = Literal["key"]

AaaTacacsServerKeyEnumDef = Literal["6", "7"]

AaaAccountingRuleMethodDef = Literal["commands", "exec", "network", "system"]

AaaAccountingRuleLevelDef = Literal["1", "15"]

AaaAuthorizationRuleMethodDef = Literal["commands"]

AaaAuthorizationRuleLevelDef = Literal["1", "15"]

SystemAaaUserPrivilegeDef = Literal["1", "15"]

SystemAaaDefaultUserPrivilegeDef = Literal["15"]

SystemAaaUserPubkeyChainKeyTypeDef = Literal["ssh-rsa"]

SystemAaaRadiusServerKeyEnumDef = Literal["6", "7"]

SystemAaaRadiusServerKeyTypeDef = Literal["key", "pac"]

SystemAaaDefaultRadiusServerKeyTypeDef = Literal["key"]

SystemAaaTacacsServerKeyEnumDef = Literal["6", "7"]

SystemAaaAccountingRuleMethodDef = Literal["commands", "exec", "network", "system"]

SystemAaaAccountingRuleLevelDef = Literal["1", "15"]

SystemAaaAuthorizationRuleMethodDef = Literal["commands"]

SystemAaaAuthorizationRuleLevelDef = Literal["1", "15"]


@dataclass
class OneOfAuthenticationGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAuthenticationGroupOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAuthenticationGroupOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAccountingGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAccountingGroupOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAccountingGroupOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServerAuthOrderOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfUserNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUserNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUserPasswordOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserPrivilegeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UserPrivilegeDef


@dataclass
class OneOfUserPrivilegeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserPrivilegeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultUserPrivilegeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUserPubkeyChainKeyStringOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUserPubkeyChainKeyStringOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserPubkeyChainKeyTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UserPubkeyChainKeyTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PubkeyChain:
    key_string: Union[
        OneOfUserPubkeyChainKeyStringOptionsDef1, OneOfUserPubkeyChainKeyStringOptionsDef2
    ] = _field(metadata={"alias": "keyString"})
    key_type: Optional[OneOfUserPubkeyChainKeyTypeOptionsDef] = _field(
        default=None, metadata={"alias": "keyType"}
    )


@dataclass
class User:
    name: Union[OneOfUserNameOptionsDef1, OneOfUserNameOptionsDef2]
    password: Union[OneOfUserPasswordOptionsDef1, OneOfUserPasswordOptionsDef2]
    privilege: Optional[
        Union[
            OneOfUserPrivilegeOptionsDef1,
            OneOfUserPrivilegeOptionsDef2,
            OneOfUserPrivilegeOptionsDef3,
        ]
    ] = _field(default=None)
    # List of RSA public-keys per user
    pubkey_chain: Optional[List[PubkeyChain]] = _field(
        default=None, metadata={"alias": "pubkeyChain"}
    )


@dataclass
class OneOfRadiusGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRadiusVpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusVpnOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceNameOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRadiusServerAddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfRadiusServerAuthPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerAuthPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusServerAuthPortOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerAcctPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerAcctPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusServerAcctPortOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerTimeoutOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusServerTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerRetransmitOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerRetransmitOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusServerRetransmitOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRadiusServerKeyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusServerSecretKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRadiusServerSecretKeyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusServerSecretKeyOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRadiusServerKeyEnumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RadiusServerKeyEnumDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRadiusServerKeyEnumOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRadiusServerKeyTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RadiusServerKeyTypeDef


@dataclass
class OneOfRadiusServerKeyTypeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusServerKeyTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultRadiusServerKeyTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Server:
    address: OneOfRadiusServerAddressOptionsDef
    key: Union[OneOfRadiusServerKeyOptionsDef1, OneOfRadiusServerKeyOptionsDef2]
    acct_port: Optional[
        Union[
            OneOfRadiusServerAcctPortOptionsDef1,
            OneOfRadiusServerAcctPortOptionsDef2,
            OneOfRadiusServerAcctPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "acctPort"})
    auth_port: Optional[
        Union[
            OneOfRadiusServerAuthPortOptionsDef1,
            OneOfRadiusServerAuthPortOptionsDef2,
            OneOfRadiusServerAuthPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "authPort"})
    key_enum: Optional[
        Union[OneOfRadiusServerKeyEnumOptionsDef1, OneOfRadiusServerKeyEnumOptionsDef2]
    ] = _field(default=None, metadata={"alias": "keyEnum"})
    key_type: Optional[
        Union[
            OneOfRadiusServerKeyTypeOptionsDef1,
            OneOfRadiusServerKeyTypeOptionsDef2,
            OneOfRadiusServerKeyTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "keyType"})
    retransmit: Optional[
        Union[
            OneOfRadiusServerRetransmitOptionsDef1,
            OneOfRadiusServerRetransmitOptionsDef2,
            OneOfRadiusServerRetransmitOptionsDef3,
        ]
    ] = _field(default=None)
    secret_key: Optional[
        Union[
            OneOfRadiusServerSecretKeyOptionsDef1,
            OneOfRadiusServerSecretKeyOptionsDef2,
            OneOfRadiusServerSecretKeyOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secretKey"})
    timeout: Optional[
        Union[
            OneOfRadiusServerTimeoutOptionsDef1,
            OneOfRadiusServerTimeoutOptionsDef2,
            OneOfRadiusServerTimeoutOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class Radius:
    group_name: OneOfRadiusGroupNameOptionsDef = _field(metadata={"alias": "groupName"})
    # Configure the Radius server
    server: List[Server]
    source_interface: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})
    vpn: Optional[Union[OneOfRadiusVpnOptionsDef1, OneOfRadiusVpnOptionsDef2]] = _field(
        default=None
    )


@dataclass
class OneOfTacacsGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTacacsVpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTacacsVpnOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTacacsServerAddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfTacacsServerPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTacacsServerPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTacacsServerPortOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTacacsServerTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTacacsServerTimeoutOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTacacsServerTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTacacsServerKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTacacsServerKeyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTacacsServerSecretKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTacacsServerSecretKeyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTacacsServerKeyEnumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TacacsServerKeyEnumDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTacacsServerKeyEnumOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class AaaServer:
    address: OneOfTacacsServerAddressOptionsDef
    key: Union[OneOfTacacsServerKeyOptionsDef1, OneOfTacacsServerKeyOptionsDef2]
    key_enum: Optional[
        Union[OneOfTacacsServerKeyEnumOptionsDef1, OneOfTacacsServerKeyEnumOptionsDef2]
    ] = _field(default=None, metadata={"alias": "keyEnum"})
    port: Optional[
        Union[
            OneOfTacacsServerPortOptionsDef1,
            OneOfTacacsServerPortOptionsDef2,
            OneOfTacacsServerPortOptionsDef3,
        ]
    ] = _field(default=None)
    secret_key: Optional[
        Union[OneOfTacacsServerSecretKeyOptionsDef1, OneOfTacacsServerSecretKeyOptionsDef2]
    ] = _field(default=None, metadata={"alias": "secretKey"})
    timeout: Optional[
        Union[
            OneOfTacacsServerTimeoutOptionsDef1,
            OneOfTacacsServerTimeoutOptionsDef2,
            OneOfTacacsServerTimeoutOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class Tacacs:
    group_name: OneOfTacacsGroupNameOptionsDef = _field(metadata={"alias": "groupName"})
    # Configure the TACACS server
    server: List[AaaServer]
    source_interface: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})
    vpn: Optional[Union[OneOfTacacsVpnOptionsDef1, OneOfTacacsVpnOptionsDef2]] = _field(
        default=None
    )


@dataclass
class OneOfAccountingRuleRuleIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAccountingRuleMethodOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AccountingRuleMethodDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAccountingRuleLevelOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AccountingRuleLevelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAccountingRuleLevelOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAccountingRuleStartStopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAccountingRuleStartStopOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAccountingRuleStartStopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAccountingRuleGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class AccountingRule:
    group: OneOfAccountingRuleGroupOptionsDef
    method: OneOfAccountingRuleMethodOptionsDef
    rule_id: OneOfAccountingRuleRuleIdOptionsDef = _field(metadata={"alias": "ruleId"})
    level: Optional[
        Union[OneOfAccountingRuleLevelOptionsDef1, OneOfAccountingRuleLevelOptionsDef2]
    ] = _field(default=None)
    start_stop: Optional[
        Union[
            OneOfAccountingRuleStartStopOptionsDef1,
            OneOfAccountingRuleStartStopOptionsDef2,
            OneOfAccountingRuleStartStopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "startStop"})


@dataclass
class OneOfAuthorizationConsoleOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAuthorizationConsoleOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAuthorizationConsoleOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAuthorizationConfigCommandsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAuthorizationConfigCommandsOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAuthorizationConfigCommandsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAuthorizationRuleRuleIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAuthorizationRuleMethodOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AuthorizationRuleMethodDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAuthorizationRuleLevelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AuthorizationRuleLevelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAuthorizationRuleGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfAuthorizationRuleIfAuthenticatedOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAuthorizationRuleIfAuthenticatedOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class AuthorizationRule:
    group: OneOfAuthorizationRuleGroupOptionsDef
    level: OneOfAuthorizationRuleLevelOptionsDef
    method: OneOfAuthorizationRuleMethodOptionsDef
    rule_id: OneOfAuthorizationRuleRuleIdOptionsDef = _field(metadata={"alias": "ruleId"})
    if_authenticated: Optional[
        Union[
            OneOfAuthorizationRuleIfAuthenticatedOptionsDef1,
            OneOfAuthorizationRuleIfAuthenticatedOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "ifAuthenticated"})


@dataclass
class AaaData:
    accounting_group: Union[
        OneOfAccountingGroupOptionsDef1,
        OneOfAccountingGroupOptionsDef2,
        OneOfAccountingGroupOptionsDef3,
    ] = _field(metadata={"alias": "accountingGroup"})
    authentication_group: Union[
        OneOfAuthenticationGroupOptionsDef1,
        OneOfAuthenticationGroupOptionsDef2,
        OneOfAuthenticationGroupOptionsDef3,
    ] = _field(metadata={"alias": "authenticationGroup"})
    authorization_config_commands: Union[
        OneOfAuthorizationConfigCommandsOptionsDef1,
        OneOfAuthorizationConfigCommandsOptionsDef2,
        OneOfAuthorizationConfigCommandsOptionsDef3,
    ] = _field(metadata={"alias": "authorizationConfigCommands"})
    authorization_console: Union[
        OneOfAuthorizationConsoleOptionsDef1,
        OneOfAuthorizationConsoleOptionsDef2,
        OneOfAuthorizationConsoleOptionsDef3,
    ] = _field(metadata={"alias": "authorizationConsole"})
    server_auth_order: OneOfServerAuthOrderOptionsDef = _field(
        metadata={"alias": "serverAuthOrder"}
    )
    # Configure the accounting rules
    accounting_rule: Optional[List[AccountingRule]] = _field(
        default=None, metadata={"alias": "accountingRule"}
    )
    # Configure the Authorization Rules
    authorization_rule: Optional[List[AuthorizationRule]] = _field(
        default=None, metadata={"alias": "authorizationRule"}
    )
    # Configure the Radius serverGroup
    radius: Optional[List[Radius]] = _field(default=None)
    # Configure the TACACS serverGroup
    tacacs: Optional[List[Tacacs]] = _field(default=None)
    # Create local login account
    user: Optional[List[User]] = _field(default=None)


@dataclass
class Payload:
    """
    AAA profile parcel schema for POST request
    """

    data: AaaData
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
    # AAA profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanSystemAaaPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateAaaProfileParcelForSystemPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemAaaData:
    accounting_group: Union[
        OneOfAccountingGroupOptionsDef1,
        OneOfAccountingGroupOptionsDef2,
        OneOfAccountingGroupOptionsDef3,
    ] = _field(metadata={"alias": "accountingGroup"})
    authentication_group: Union[
        OneOfAuthenticationGroupOptionsDef1,
        OneOfAuthenticationGroupOptionsDef2,
        OneOfAuthenticationGroupOptionsDef3,
    ] = _field(metadata={"alias": "authenticationGroup"})
    authorization_config_commands: Union[
        OneOfAuthorizationConfigCommandsOptionsDef1,
        OneOfAuthorizationConfigCommandsOptionsDef2,
        OneOfAuthorizationConfigCommandsOptionsDef3,
    ] = _field(metadata={"alias": "authorizationConfigCommands"})
    authorization_console: Union[
        OneOfAuthorizationConsoleOptionsDef1,
        OneOfAuthorizationConsoleOptionsDef2,
        OneOfAuthorizationConsoleOptionsDef3,
    ] = _field(metadata={"alias": "authorizationConsole"})
    server_auth_order: OneOfServerAuthOrderOptionsDef = _field(
        metadata={"alias": "serverAuthOrder"}
    )
    # Configure the accounting rules
    accounting_rule: Optional[List[AccountingRule]] = _field(
        default=None, metadata={"alias": "accountingRule"}
    )
    # Configure the Authorization Rules
    authorization_rule: Optional[List[AuthorizationRule]] = _field(
        default=None, metadata={"alias": "authorizationRule"}
    )
    # Configure the Radius serverGroup
    radius: Optional[List[Radius]] = _field(default=None)
    # Configure the TACACS serverGroup
    tacacs: Optional[List[Tacacs]] = _field(default=None)
    # Create local login account
    user: Optional[List[User]] = _field(default=None)


@dataclass
class CreateAaaProfileParcelForSystemPostRequest:
    """
    AAA profile parcel schema for POST request
    """

    data: SystemAaaData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class AaaOneOfServerAuthOrderOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class AaaOneOfUserNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AaaOneOfUserPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AaaOneOfUserPrivilegeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaUserPrivilegeDef


@dataclass
class AaaOneOfUserPrivilegeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaDefaultUserPrivilegeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class AaaOneOfUserPubkeyChainKeyTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaUserPubkeyChainKeyTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class AaaPubkeyChain:
    key_string: Union[
        OneOfUserPubkeyChainKeyStringOptionsDef1, OneOfUserPubkeyChainKeyStringOptionsDef2
    ] = _field(metadata={"alias": "keyString"})
    key_type: Optional[AaaOneOfUserPubkeyChainKeyTypeOptionsDef] = _field(
        default=None, metadata={"alias": "keyType"}
    )


@dataclass
class AaaUser:
    name: Union[AaaOneOfUserNameOptionsDef1, OneOfUserNameOptionsDef2]
    password: Union[AaaOneOfUserPasswordOptionsDef1, OneOfUserPasswordOptionsDef2]
    privilege: Optional[
        Union[
            AaaOneOfUserPrivilegeOptionsDef1,
            OneOfUserPrivilegeOptionsDef2,
            AaaOneOfUserPrivilegeOptionsDef3,
        ]
    ] = _field(default=None)
    # List of RSA public-keys per user
    pubkey_chain: Optional[List[AaaPubkeyChain]] = _field(
        default=None, metadata={"alias": "pubkeyChain"}
    )


@dataclass
class AaaOneOfRadiusGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AaaOneOfRadiusServerAddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class AaaOneOfRadiusServerAuthPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaOneOfRadiusServerAuthPortOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaOneOfRadiusServerAcctPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaOneOfRadiusServerAcctPortOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaOneOfRadiusServerTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaOneOfRadiusServerTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaOneOfRadiusServerRetransmitOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaOneOfRadiusServerRetransmitOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaOneOfRadiusServerKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AaaOneOfRadiusServerSecretKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AaaOneOfRadiusServerKeyEnumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaRadiusServerKeyEnumDef  # pytype: disable=annotation-type-mismatch


@dataclass
class AaaOneOfRadiusServerKeyTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaRadiusServerKeyTypeDef


@dataclass
class AaaOneOfRadiusServerKeyTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaDefaultRadiusServerKeyTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemAaaServer:
    address: AaaOneOfRadiusServerAddressOptionsDef
    key: Union[AaaOneOfRadiusServerKeyOptionsDef1, OneOfRadiusServerKeyOptionsDef2]
    acct_port: Optional[
        Union[
            AaaOneOfRadiusServerAcctPortOptionsDef1,
            OneOfRadiusServerAcctPortOptionsDef2,
            AaaOneOfRadiusServerAcctPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "acctPort"})
    auth_port: Optional[
        Union[
            AaaOneOfRadiusServerAuthPortOptionsDef1,
            OneOfRadiusServerAuthPortOptionsDef2,
            AaaOneOfRadiusServerAuthPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "authPort"})
    key_enum: Optional[
        Union[AaaOneOfRadiusServerKeyEnumOptionsDef1, OneOfRadiusServerKeyEnumOptionsDef2]
    ] = _field(default=None, metadata={"alias": "keyEnum"})
    key_type: Optional[
        Union[
            AaaOneOfRadiusServerKeyTypeOptionsDef1,
            OneOfRadiusServerKeyTypeOptionsDef2,
            AaaOneOfRadiusServerKeyTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "keyType"})
    retransmit: Optional[
        Union[
            AaaOneOfRadiusServerRetransmitOptionsDef1,
            OneOfRadiusServerRetransmitOptionsDef2,
            AaaOneOfRadiusServerRetransmitOptionsDef3,
        ]
    ] = _field(default=None)
    secret_key: Optional[
        Union[
            AaaOneOfRadiusServerSecretKeyOptionsDef1,
            OneOfRadiusServerSecretKeyOptionsDef2,
            OneOfRadiusServerSecretKeyOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secretKey"})
    timeout: Optional[
        Union[
            AaaOneOfRadiusServerTimeoutOptionsDef1,
            OneOfRadiusServerTimeoutOptionsDef2,
            AaaOneOfRadiusServerTimeoutOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class AaaRadius:
    group_name: AaaOneOfRadiusGroupNameOptionsDef = _field(metadata={"alias": "groupName"})
    # Configure the Radius server
    server: List[SystemAaaServer]
    source_interface: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})
    vpn: Optional[Union[OneOfRadiusVpnOptionsDef1, OneOfRadiusVpnOptionsDef2]] = _field(
        default=None
    )


@dataclass
class AaaOneOfTacacsGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AaaOneOfTacacsServerAddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class AaaOneOfTacacsServerPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaOneOfTacacsServerPortOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaOneOfTacacsServerTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaOneOfTacacsServerTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaOneOfTacacsServerKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AaaOneOfTacacsServerSecretKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AaaOneOfTacacsServerKeyEnumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaTacacsServerKeyEnumDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanSystemAaaServer:
    address: AaaOneOfTacacsServerAddressOptionsDef
    key: Union[AaaOneOfTacacsServerKeyOptionsDef1, OneOfTacacsServerKeyOptionsDef2]
    key_enum: Optional[
        Union[AaaOneOfTacacsServerKeyEnumOptionsDef1, OneOfTacacsServerKeyEnumOptionsDef2]
    ] = _field(default=None, metadata={"alias": "keyEnum"})
    port: Optional[
        Union[
            AaaOneOfTacacsServerPortOptionsDef1,
            OneOfTacacsServerPortOptionsDef2,
            AaaOneOfTacacsServerPortOptionsDef3,
        ]
    ] = _field(default=None)
    secret_key: Optional[
        Union[AaaOneOfTacacsServerSecretKeyOptionsDef1, OneOfTacacsServerSecretKeyOptionsDef2]
    ] = _field(default=None, metadata={"alias": "secretKey"})
    timeout: Optional[
        Union[
            AaaOneOfTacacsServerTimeoutOptionsDef1,
            OneOfTacacsServerTimeoutOptionsDef2,
            AaaOneOfTacacsServerTimeoutOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class AaaTacacs:
    group_name: AaaOneOfTacacsGroupNameOptionsDef = _field(metadata={"alias": "groupName"})
    # Configure the TACACS server
    server: List[SdwanSystemAaaServer]
    source_interface: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})
    vpn: Optional[Union[OneOfTacacsVpnOptionsDef1, OneOfTacacsVpnOptionsDef2]] = _field(
        default=None
    )


@dataclass
class AaaOneOfAccountingRuleRuleIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AaaOneOfAccountingRuleMethodOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaAccountingRuleMethodDef  # pytype: disable=annotation-type-mismatch


@dataclass
class AaaOneOfAccountingRuleLevelOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaAccountingRuleLevelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class AaaOneOfAccountingRuleGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class AaaAccountingRule:
    group: AaaOneOfAccountingRuleGroupOptionsDef
    method: AaaOneOfAccountingRuleMethodOptionsDef
    rule_id: AaaOneOfAccountingRuleRuleIdOptionsDef = _field(metadata={"alias": "ruleId"})
    level: Optional[
        Union[AaaOneOfAccountingRuleLevelOptionsDef1, OneOfAccountingRuleLevelOptionsDef2]
    ] = _field(default=None)
    start_stop: Optional[
        Union[
            OneOfAccountingRuleStartStopOptionsDef1,
            OneOfAccountingRuleStartStopOptionsDef2,
            OneOfAccountingRuleStartStopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "startStop"})


@dataclass
class AaaOneOfAuthorizationRuleRuleIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AaaOneOfAuthorizationRuleMethodOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaAuthorizationRuleMethodDef  # pytype: disable=annotation-type-mismatch


@dataclass
class AaaOneOfAuthorizationRuleLevelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaAuthorizationRuleLevelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class AaaOneOfAuthorizationRuleGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class AaaAuthorizationRule:
    group: AaaOneOfAuthorizationRuleGroupOptionsDef
    level: AaaOneOfAuthorizationRuleLevelOptionsDef
    method: AaaOneOfAuthorizationRuleMethodOptionsDef
    rule_id: AaaOneOfAuthorizationRuleRuleIdOptionsDef = _field(metadata={"alias": "ruleId"})
    if_authenticated: Optional[
        Union[
            OneOfAuthorizationRuleIfAuthenticatedOptionsDef1,
            OneOfAuthorizationRuleIfAuthenticatedOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "ifAuthenticated"})


@dataclass
class SdwanSystemAaaData:
    accounting_group: Union[
        OneOfAccountingGroupOptionsDef1,
        OneOfAccountingGroupOptionsDef2,
        OneOfAccountingGroupOptionsDef3,
    ] = _field(metadata={"alias": "accountingGroup"})
    authentication_group: Union[
        OneOfAuthenticationGroupOptionsDef1,
        OneOfAuthenticationGroupOptionsDef2,
        OneOfAuthenticationGroupOptionsDef3,
    ] = _field(metadata={"alias": "authenticationGroup"})
    authorization_config_commands: Union[
        OneOfAuthorizationConfigCommandsOptionsDef1,
        OneOfAuthorizationConfigCommandsOptionsDef2,
        OneOfAuthorizationConfigCommandsOptionsDef3,
    ] = _field(metadata={"alias": "authorizationConfigCommands"})
    authorization_console: Union[
        OneOfAuthorizationConsoleOptionsDef1,
        OneOfAuthorizationConsoleOptionsDef2,
        OneOfAuthorizationConsoleOptionsDef3,
    ] = _field(metadata={"alias": "authorizationConsole"})
    server_auth_order: AaaOneOfServerAuthOrderOptionsDef = _field(
        metadata={"alias": "serverAuthOrder"}
    )
    # Configure the accounting rules
    accounting_rule: Optional[List[AaaAccountingRule]] = _field(
        default=None, metadata={"alias": "accountingRule"}
    )
    # Configure the Authorization Rules
    authorization_rule: Optional[List[AaaAuthorizationRule]] = _field(
        default=None, metadata={"alias": "authorizationRule"}
    )
    # Configure the Radius serverGroup
    radius: Optional[List[AaaRadius]] = _field(default=None)
    # Configure the TACACS serverGroup
    tacacs: Optional[List[AaaTacacs]] = _field(default=None)
    # Create local login account
    user: Optional[List[AaaUser]] = _field(default=None)


@dataclass
class AaaPayload:
    """
    AAA profile parcel schema for PUT request
    """

    data: SdwanSystemAaaData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanSystemAaaPayload:
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
    # AAA profile parcel schema for PUT request
    payload: Optional[AaaPayload] = _field(default=None)


@dataclass
class EditAaaProfileParcelForSystemPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemAaaOneOfServerAuthOrderOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class SystemAaaOneOfUserNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemAaaOneOfUserPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemAaaOneOfUserPrivilegeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaUserPrivilegeDef


@dataclass
class SystemAaaOneOfUserPrivilegeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaDefaultUserPrivilegeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemAaaOneOfUserPubkeyChainKeyTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaUserPubkeyChainKeyTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemAaaPubkeyChain:
    key_string: Union[
        OneOfUserPubkeyChainKeyStringOptionsDef1, OneOfUserPubkeyChainKeyStringOptionsDef2
    ] = _field(metadata={"alias": "keyString"})
    key_type: Optional[SystemAaaOneOfUserPubkeyChainKeyTypeOptionsDef] = _field(
        default=None, metadata={"alias": "keyType"}
    )


@dataclass
class SystemAaaUser:
    name: Union[SystemAaaOneOfUserNameOptionsDef1, OneOfUserNameOptionsDef2]
    password: Union[SystemAaaOneOfUserPasswordOptionsDef1, OneOfUserPasswordOptionsDef2]
    privilege: Optional[
        Union[
            SystemAaaOneOfUserPrivilegeOptionsDef1,
            OneOfUserPrivilegeOptionsDef2,
            SystemAaaOneOfUserPrivilegeOptionsDef3,
        ]
    ] = _field(default=None)
    # List of RSA public-keys per user
    pubkey_chain: Optional[List[SystemAaaPubkeyChain]] = _field(
        default=None, metadata={"alias": "pubkeyChain"}
    )


@dataclass
class SystemAaaOneOfRadiusGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemAaaOneOfRadiusServerAddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SystemAaaOneOfRadiusServerAuthPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaOneOfRadiusServerAuthPortOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaOneOfRadiusServerAcctPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaOneOfRadiusServerAcctPortOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaOneOfRadiusServerTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaOneOfRadiusServerTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaOneOfRadiusServerRetransmitOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaOneOfRadiusServerRetransmitOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaOneOfRadiusServerKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemAaaOneOfRadiusServerSecretKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemAaaOneOfRadiusServerKeyEnumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaRadiusServerKeyEnumDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemAaaOneOfRadiusServerKeyTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaRadiusServerKeyTypeDef


@dataclass
class SystemAaaOneOfRadiusServerKeyTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaDefaultRadiusServerKeyTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileSdwanSystemAaaServer:
    address: SystemAaaOneOfRadiusServerAddressOptionsDef
    key: Union[SystemAaaOneOfRadiusServerKeyOptionsDef1, OneOfRadiusServerKeyOptionsDef2]
    acct_port: Optional[
        Union[
            SystemAaaOneOfRadiusServerAcctPortOptionsDef1,
            OneOfRadiusServerAcctPortOptionsDef2,
            SystemAaaOneOfRadiusServerAcctPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "acctPort"})
    auth_port: Optional[
        Union[
            SystemAaaOneOfRadiusServerAuthPortOptionsDef1,
            OneOfRadiusServerAuthPortOptionsDef2,
            SystemAaaOneOfRadiusServerAuthPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "authPort"})
    key_enum: Optional[
        Union[SystemAaaOneOfRadiusServerKeyEnumOptionsDef1, OneOfRadiusServerKeyEnumOptionsDef2]
    ] = _field(default=None, metadata={"alias": "keyEnum"})
    key_type: Optional[
        Union[
            SystemAaaOneOfRadiusServerKeyTypeOptionsDef1,
            OneOfRadiusServerKeyTypeOptionsDef2,
            SystemAaaOneOfRadiusServerKeyTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "keyType"})
    retransmit: Optional[
        Union[
            SystemAaaOneOfRadiusServerRetransmitOptionsDef1,
            OneOfRadiusServerRetransmitOptionsDef2,
            SystemAaaOneOfRadiusServerRetransmitOptionsDef3,
        ]
    ] = _field(default=None)
    secret_key: Optional[
        Union[
            SystemAaaOneOfRadiusServerSecretKeyOptionsDef1,
            OneOfRadiusServerSecretKeyOptionsDef2,
            OneOfRadiusServerSecretKeyOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secretKey"})
    timeout: Optional[
        Union[
            SystemAaaOneOfRadiusServerTimeoutOptionsDef1,
            OneOfRadiusServerTimeoutOptionsDef2,
            SystemAaaOneOfRadiusServerTimeoutOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class SystemAaaRadius:
    group_name: SystemAaaOneOfRadiusGroupNameOptionsDef = _field(metadata={"alias": "groupName"})
    # Configure the Radius server
    server: List[FeatureProfileSdwanSystemAaaServer]
    source_interface: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})
    vpn: Optional[Union[OneOfRadiusVpnOptionsDef1, OneOfRadiusVpnOptionsDef2]] = _field(
        default=None
    )


@dataclass
class SystemAaaOneOfTacacsGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemAaaOneOfTacacsServerAddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SystemAaaOneOfTacacsServerPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaOneOfTacacsServerPortOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaOneOfTacacsServerTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaOneOfTacacsServerTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaOneOfTacacsServerKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemAaaOneOfTacacsServerSecretKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemAaaOneOfTacacsServerKeyEnumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaTacacsServerKeyEnumDef  # pytype: disable=annotation-type-mismatch


@dataclass
class V1FeatureProfileSdwanSystemAaaServer:
    address: SystemAaaOneOfTacacsServerAddressOptionsDef
    key: Union[SystemAaaOneOfTacacsServerKeyOptionsDef1, OneOfTacacsServerKeyOptionsDef2]
    key_enum: Optional[
        Union[SystemAaaOneOfTacacsServerKeyEnumOptionsDef1, OneOfTacacsServerKeyEnumOptionsDef2]
    ] = _field(default=None, metadata={"alias": "keyEnum"})
    port: Optional[
        Union[
            SystemAaaOneOfTacacsServerPortOptionsDef1,
            OneOfTacacsServerPortOptionsDef2,
            SystemAaaOneOfTacacsServerPortOptionsDef3,
        ]
    ] = _field(default=None)
    secret_key: Optional[
        Union[SystemAaaOneOfTacacsServerSecretKeyOptionsDef1, OneOfTacacsServerSecretKeyOptionsDef2]
    ] = _field(default=None, metadata={"alias": "secretKey"})
    timeout: Optional[
        Union[
            SystemAaaOneOfTacacsServerTimeoutOptionsDef1,
            OneOfTacacsServerTimeoutOptionsDef2,
            SystemAaaOneOfTacacsServerTimeoutOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class SystemAaaTacacs:
    group_name: SystemAaaOneOfTacacsGroupNameOptionsDef = _field(metadata={"alias": "groupName"})
    # Configure the TACACS server
    server: List[V1FeatureProfileSdwanSystemAaaServer]
    source_interface: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})
    vpn: Optional[Union[OneOfTacacsVpnOptionsDef1, OneOfTacacsVpnOptionsDef2]] = _field(
        default=None
    )


@dataclass
class SystemAaaOneOfAccountingRuleRuleIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemAaaOneOfAccountingRuleMethodOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaAccountingRuleMethodDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemAaaOneOfAccountingRuleLevelOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaAccountingRuleLevelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemAaaOneOfAccountingRuleGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class SystemAaaAccountingRule:
    group: SystemAaaOneOfAccountingRuleGroupOptionsDef
    method: SystemAaaOneOfAccountingRuleMethodOptionsDef
    rule_id: SystemAaaOneOfAccountingRuleRuleIdOptionsDef = _field(metadata={"alias": "ruleId"})
    level: Optional[
        Union[SystemAaaOneOfAccountingRuleLevelOptionsDef1, OneOfAccountingRuleLevelOptionsDef2]
    ] = _field(default=None)
    start_stop: Optional[
        Union[
            OneOfAccountingRuleStartStopOptionsDef1,
            OneOfAccountingRuleStartStopOptionsDef2,
            OneOfAccountingRuleStartStopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "startStop"})


@dataclass
class SystemAaaOneOfAuthorizationRuleRuleIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemAaaOneOfAuthorizationRuleMethodOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaAuthorizationRuleMethodDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemAaaOneOfAuthorizationRuleLevelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaAuthorizationRuleLevelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemAaaOneOfAuthorizationRuleGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class SystemAaaAuthorizationRule:
    group: SystemAaaOneOfAuthorizationRuleGroupOptionsDef
    level: SystemAaaOneOfAuthorizationRuleLevelOptionsDef
    method: SystemAaaOneOfAuthorizationRuleMethodOptionsDef
    rule_id: SystemAaaOneOfAuthorizationRuleRuleIdOptionsDef = _field(metadata={"alias": "ruleId"})
    if_authenticated: Optional[
        Union[
            OneOfAuthorizationRuleIfAuthenticatedOptionsDef1,
            OneOfAuthorizationRuleIfAuthenticatedOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "ifAuthenticated"})


@dataclass
class FeatureProfileSdwanSystemAaaData:
    accounting_group: Union[
        OneOfAccountingGroupOptionsDef1,
        OneOfAccountingGroupOptionsDef2,
        OneOfAccountingGroupOptionsDef3,
    ] = _field(metadata={"alias": "accountingGroup"})
    authentication_group: Union[
        OneOfAuthenticationGroupOptionsDef1,
        OneOfAuthenticationGroupOptionsDef2,
        OneOfAuthenticationGroupOptionsDef3,
    ] = _field(metadata={"alias": "authenticationGroup"})
    authorization_config_commands: Union[
        OneOfAuthorizationConfigCommandsOptionsDef1,
        OneOfAuthorizationConfigCommandsOptionsDef2,
        OneOfAuthorizationConfigCommandsOptionsDef3,
    ] = _field(metadata={"alias": "authorizationConfigCommands"})
    authorization_console: Union[
        OneOfAuthorizationConsoleOptionsDef1,
        OneOfAuthorizationConsoleOptionsDef2,
        OneOfAuthorizationConsoleOptionsDef3,
    ] = _field(metadata={"alias": "authorizationConsole"})
    server_auth_order: SystemAaaOneOfServerAuthOrderOptionsDef = _field(
        metadata={"alias": "serverAuthOrder"}
    )
    # Configure the accounting rules
    accounting_rule: Optional[List[SystemAaaAccountingRule]] = _field(
        default=None, metadata={"alias": "accountingRule"}
    )
    # Configure the Authorization Rules
    authorization_rule: Optional[List[SystemAaaAuthorizationRule]] = _field(
        default=None, metadata={"alias": "authorizationRule"}
    )
    # Configure the Radius serverGroup
    radius: Optional[List[SystemAaaRadius]] = _field(default=None)
    # Configure the TACACS serverGroup
    tacacs: Optional[List[SystemAaaTacacs]] = _field(default=None)
    # Create local login account
    user: Optional[List[SystemAaaUser]] = _field(default=None)


@dataclass
class EditAaaProfileParcelForSystemPutRequest:
    """
    AAA profile parcel schema for PUT request
    """

    data: FeatureProfileSdwanSystemAaaData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
