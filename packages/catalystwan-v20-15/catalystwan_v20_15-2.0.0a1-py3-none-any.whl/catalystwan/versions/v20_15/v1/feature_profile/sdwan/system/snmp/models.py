# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

CommunityAuthorizationDef = Literal["read-only", "read-write"]

GroupSecurityLevelDef = Literal["auth-no-priv", "auth-priv", "no-auth-no-priv"]

UserAuthDef = Literal["sha"]

UserPrivDef = Literal["aes-256-cfb-128", "aes-cfb-128"]

SnmpCommunityAuthorizationDef = Literal["read-only", "read-write"]

SnmpGroupSecurityLevelDef = Literal["auth-no-priv", "auth-priv", "no-auth-no-priv"]

SnmpUserAuthDef = Literal["sha"]

SnmpUserPrivDef = Literal["aes-256-cfb-128", "aes-cfb-128"]

SystemSnmpCommunityAuthorizationDef = Literal["read-only", "read-write"]

SystemSnmpGroupSecurityLevelDef = Literal["auth-no-priv", "auth-priv", "no-auth-no-priv"]

SystemSnmpUserAuthDef = Literal["sha"]

SystemSnmpUserPrivDef = Literal["aes-256-cfb-128", "aes-cfb-128"]


@dataclass
class OneOfShutdownOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfShutdownOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfShutdownOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfContactOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfContactOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfContactOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLocationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfLocationOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLocationOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfViewNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfViewOidIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfViewOidIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfViewOidExcludeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfViewOidExcludeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfViewOidExcludeOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class Oid:
    id: Union[OneOfViewOidIdOptionsDef1, OneOfViewOidIdOptionsDef2]
    exclude: Optional[
        Union[
            OneOfViewOidExcludeOptionsDef1,
            OneOfViewOidExcludeOptionsDef2,
            OneOfViewOidExcludeOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class View:
    name: OneOfViewNameOptionsDef
    # Configure SNMP object identifier
    oid: Optional[List[Oid]] = _field(default=None)


@dataclass
class OneOfCommunityNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfCommunityNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTargetCommunityNameUserLabelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfCommunityViewOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfCommunityViewOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfCommunityAuthorizationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CommunityAuthorizationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfCommunityAuthorizationOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Community:
    name: Union[OneOfCommunityNameOptionsDef1, OneOfCommunityNameOptionsDef2]
    view: Union[OneOfCommunityViewOptionsDef1, OneOfCommunityViewOptionsDef2]
    authorization: Optional[
        Union[OneOfCommunityAuthorizationOptionsDef1, OneOfCommunityAuthorizationOptionsDef2]
    ] = _field(default=None)
    user_label: Optional[OneOfTargetCommunityNameUserLabelOptionsDef] = _field(
        default=None, metadata={"alias": "userLabel"}
    )


@dataclass
class OneOfGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfGroupSecurityLevelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GroupSecurityLevelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfGroupViewOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfGroupViewOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Group:
    name: OneOfGroupNameOptionsDef
    security_level: OneOfGroupSecurityLevelOptionsDef = _field(metadata={"alias": "securityLevel"})
    view: Union[OneOfGroupViewOptionsDef1, OneOfGroupViewOptionsDef2]


@dataclass
class OneOfUserNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUserAuthOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UserAuthDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUserAuthOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserAuthOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUserAuthPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUserAuthPasswordOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserAuthPasswordOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUserPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UserPrivDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUserPrivOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserPrivOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUserPrivPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUserPrivPasswordOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserPrivPasswordOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUserGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUserGroupOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class User:
    group: Union[OneOfUserGroupOptionsDef1, OneOfUserGroupOptionsDef2]
    name: OneOfUserNameOptionsDef
    auth: Optional[
        Union[OneOfUserAuthOptionsDef1, OneOfUserAuthOptionsDef2, OneOfUserAuthOptionsDef3]
    ] = _field(default=None)
    auth_password: Optional[
        Union[
            OneOfUserAuthPasswordOptionsDef1,
            OneOfUserAuthPasswordOptionsDef2,
            OneOfUserAuthPasswordOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "authPassword"})
    priv: Optional[
        Union[OneOfUserPrivOptionsDef1, OneOfUserPrivOptionsDef2, OneOfUserPrivOptionsDef3]
    ] = _field(default=None)
    priv_password: Optional[
        Union[
            OneOfUserPrivPasswordOptionsDef1,
            OneOfUserPrivPasswordOptionsDef2,
            OneOfUserPrivPasswordOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "privPassword"})


@dataclass
class OneOfTargetVpnIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTargetVpnIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTargetIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfTargetIpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTargetPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTargetPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTargetCommunityNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTargetCommunityNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTargetUserOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTargetUserOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTargetSourceInterfaceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTargetSourceInterfaceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Target:
    ip: Union[OneOfTargetIpOptionsDef1, OneOfTargetIpOptionsDef2]
    port: Union[OneOfTargetPortOptionsDef1, OneOfTargetPortOptionsDef2]
    vpn_id: Union[OneOfTargetVpnIdOptionsDef1, OneOfTargetVpnIdOptionsDef2] = _field(
        metadata={"alias": "vpnId"}
    )
    community_name: Optional[
        Union[OneOfTargetCommunityNameOptionsDef1, OneOfTargetCommunityNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "communityName"})
    source_interface: Optional[
        Union[OneOfTargetSourceInterfaceOptionsDef1, OneOfTargetSourceInterfaceOptionsDef2]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})
    user: Optional[Union[OneOfTargetUserOptionsDef1, OneOfTargetUserOptionsDef2]] = _field(
        default=None
    )
    user_label: Optional[OneOfTargetCommunityNameUserLabelOptionsDef] = _field(
        default=None, metadata={"alias": "userLabel"}
    )


@dataclass
class SnmpData:
    # Configure SNMP community
    community: Optional[List[Community]] = _field(default=None)
    contact: Optional[
        Union[OneOfContactOptionsDef1, OneOfContactOptionsDef2, OneOfContactOptionsDef3]
    ] = _field(default=None)
    # Configure an SNMP group
    group: Optional[List[Group]] = _field(default=None)
    location: Optional[
        Union[OneOfLocationOptionsDef1, OneOfLocationOptionsDef2, OneOfLocationOptionsDef3]
    ] = _field(default=None)
    shutdown: Optional[
        Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    ] = _field(default=None)
    # Configure SNMP server to receive SNMP traps
    target: Optional[List[Target]] = _field(default=None)
    # Configure an SNMP user
    user: Optional[List[User]] = _field(default=None)
    # Configure a view record
    view: Optional[List[View]] = _field(default=None)


@dataclass
class Payload:
    """
    SNMP profile parcel schema for POST request
    """

    data: SnmpData
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
    # SNMP profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanSystemSnmpPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSnmpProfileParcelForSystemPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemSnmpData:
    # Configure SNMP community
    community: Optional[List[Community]] = _field(default=None)
    contact: Optional[
        Union[OneOfContactOptionsDef1, OneOfContactOptionsDef2, OneOfContactOptionsDef3]
    ] = _field(default=None)
    # Configure an SNMP group
    group: Optional[List[Group]] = _field(default=None)
    location: Optional[
        Union[OneOfLocationOptionsDef1, OneOfLocationOptionsDef2, OneOfLocationOptionsDef3]
    ] = _field(default=None)
    shutdown: Optional[
        Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    ] = _field(default=None)
    # Configure SNMP server to receive SNMP traps
    target: Optional[List[Target]] = _field(default=None)
    # Configure an SNMP user
    user: Optional[List[User]] = _field(default=None)
    # Configure a view record
    view: Optional[List[View]] = _field(default=None)


@dataclass
class CreateSnmpProfileParcelForSystemPostRequest:
    """
    SNMP profile parcel schema for POST request
    """

    data: SystemSnmpData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class SnmpOneOfContactOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfLocationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfViewNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfViewOidIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOid:
    id: Union[SnmpOneOfViewOidIdOptionsDef1, OneOfViewOidIdOptionsDef2]
    exclude: Optional[
        Union[
            OneOfViewOidExcludeOptionsDef1,
            OneOfViewOidExcludeOptionsDef2,
            OneOfViewOidExcludeOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class SnmpView:
    name: SnmpOneOfViewNameOptionsDef
    # Configure SNMP object identifier
    oid: Optional[List[SnmpOid]] = _field(default=None)


@dataclass
class SnmpOneOfCommunityNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfTargetCommunityNameUserLabelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfCommunityViewOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfCommunityAuthorizationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SnmpCommunityAuthorizationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SnmpCommunity:
    name: Union[SnmpOneOfCommunityNameOptionsDef1, OneOfCommunityNameOptionsDef2]
    view: Union[SnmpOneOfCommunityViewOptionsDef1, OneOfCommunityViewOptionsDef2]
    authorization: Optional[
        Union[SnmpOneOfCommunityAuthorizationOptionsDef1, OneOfCommunityAuthorizationOptionsDef2]
    ] = _field(default=None)
    user_label: Optional[SnmpOneOfTargetCommunityNameUserLabelOptionsDef] = _field(
        default=None, metadata={"alias": "userLabel"}
    )


@dataclass
class SnmpOneOfGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfGroupSecurityLevelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SnmpGroupSecurityLevelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SnmpOneOfGroupViewOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpGroup:
    name: SnmpOneOfGroupNameOptionsDef
    security_level: SnmpOneOfGroupSecurityLevelOptionsDef = _field(
        metadata={"alias": "securityLevel"}
    )
    view: Union[SnmpOneOfGroupViewOptionsDef1, OneOfGroupViewOptionsDef2]


@dataclass
class SnmpOneOfUserNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfUserAuthOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SnmpUserAuthDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SnmpOneOfUserAuthPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfUserPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SnmpUserPrivDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SnmpOneOfUserPrivPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfUserGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpUser:
    group: Union[SnmpOneOfUserGroupOptionsDef1, OneOfUserGroupOptionsDef2]
    name: SnmpOneOfUserNameOptionsDef
    auth: Optional[
        Union[SnmpOneOfUserAuthOptionsDef1, OneOfUserAuthOptionsDef2, OneOfUserAuthOptionsDef3]
    ] = _field(default=None)
    auth_password: Optional[
        Union[
            SnmpOneOfUserAuthPasswordOptionsDef1,
            OneOfUserAuthPasswordOptionsDef2,
            OneOfUserAuthPasswordOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "authPassword"})
    priv: Optional[
        Union[SnmpOneOfUserPrivOptionsDef1, OneOfUserPrivOptionsDef2, OneOfUserPrivOptionsDef3]
    ] = _field(default=None)
    priv_password: Optional[
        Union[
            SnmpOneOfUserPrivPasswordOptionsDef1,
            OneOfUserPrivPasswordOptionsDef2,
            OneOfUserPrivPasswordOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "privPassword"})


@dataclass
class SnmpOneOfTargetVpnIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SnmpOneOfTargetIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SnmpOneOfTargetPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemSnmpOneOfTargetCommunityNameUserLabelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfTargetCommunityNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfTargetUserOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfTargetSourceInterfaceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpTarget:
    ip: Union[SnmpOneOfTargetIpOptionsDef1, OneOfTargetIpOptionsDef2]
    port: Union[SnmpOneOfTargetPortOptionsDef1, OneOfTargetPortOptionsDef2]
    vpn_id: Union[SnmpOneOfTargetVpnIdOptionsDef1, OneOfTargetVpnIdOptionsDef2] = _field(
        metadata={"alias": "vpnId"}
    )
    community_name: Optional[
        Union[SnmpOneOfTargetCommunityNameOptionsDef1, OneOfTargetCommunityNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "communityName"})
    source_interface: Optional[
        Union[SnmpOneOfTargetSourceInterfaceOptionsDef1, OneOfTargetSourceInterfaceOptionsDef2]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})
    user: Optional[Union[SnmpOneOfTargetUserOptionsDef1, OneOfTargetUserOptionsDef2]] = _field(
        default=None
    )
    user_label: Optional[SystemSnmpOneOfTargetCommunityNameUserLabelOptionsDef] = _field(
        default=None, metadata={"alias": "userLabel"}
    )


@dataclass
class SdwanSystemSnmpData:
    # Configure SNMP community
    community: Optional[List[SnmpCommunity]] = _field(default=None)
    contact: Optional[
        Union[SnmpOneOfContactOptionsDef1, OneOfContactOptionsDef2, OneOfContactOptionsDef3]
    ] = _field(default=None)
    # Configure an SNMP group
    group: Optional[List[SnmpGroup]] = _field(default=None)
    location: Optional[
        Union[SnmpOneOfLocationOptionsDef1, OneOfLocationOptionsDef2, OneOfLocationOptionsDef3]
    ] = _field(default=None)
    shutdown: Optional[
        Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    ] = _field(default=None)
    # Configure SNMP server to receive SNMP traps
    target: Optional[List[SnmpTarget]] = _field(default=None)
    # Configure an SNMP user
    user: Optional[List[SnmpUser]] = _field(default=None)
    # Configure a view record
    view: Optional[List[SnmpView]] = _field(default=None)


@dataclass
class SnmpPayload:
    """
    SNMP profile parcel schema for PUT request
    """

    data: SdwanSystemSnmpData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanSystemSnmpPayload:
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
    # SNMP profile parcel schema for PUT request
    payload: Optional[SnmpPayload] = _field(default=None)


@dataclass
class EditSnmpProfileParcelForSystemPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemSnmpOneOfContactOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfLocationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfViewNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfViewOidIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOid:
    id: Union[SystemSnmpOneOfViewOidIdOptionsDef1, OneOfViewOidIdOptionsDef2]
    exclude: Optional[
        Union[
            OneOfViewOidExcludeOptionsDef1,
            OneOfViewOidExcludeOptionsDef2,
            OneOfViewOidExcludeOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class SystemSnmpView:
    name: SystemSnmpOneOfViewNameOptionsDef
    # Configure SNMP object identifier
    oid: Optional[List[SystemSnmpOid]] = _field(default=None)


@dataclass
class SystemSnmpOneOfCommunityNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanSystemSnmpOneOfTargetCommunityNameUserLabelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfCommunityViewOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfCommunityAuthorizationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemSnmpCommunityAuthorizationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemSnmpCommunity:
    name: Union[SystemSnmpOneOfCommunityNameOptionsDef1, OneOfCommunityNameOptionsDef2]
    view: Union[SystemSnmpOneOfCommunityViewOptionsDef1, OneOfCommunityViewOptionsDef2]
    authorization: Optional[
        Union[
            SystemSnmpOneOfCommunityAuthorizationOptionsDef1, OneOfCommunityAuthorizationOptionsDef2
        ]
    ] = _field(default=None)
    user_label: Optional[SdwanSystemSnmpOneOfTargetCommunityNameUserLabelOptionsDef] = _field(
        default=None, metadata={"alias": "userLabel"}
    )


@dataclass
class SystemSnmpOneOfGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfGroupSecurityLevelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemSnmpGroupSecurityLevelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemSnmpOneOfGroupViewOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpGroup:
    name: SystemSnmpOneOfGroupNameOptionsDef
    security_level: SystemSnmpOneOfGroupSecurityLevelOptionsDef = _field(
        metadata={"alias": "securityLevel"}
    )
    view: Union[SystemSnmpOneOfGroupViewOptionsDef1, OneOfGroupViewOptionsDef2]


@dataclass
class SystemSnmpOneOfUserNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfUserAuthOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemSnmpUserAuthDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemSnmpOneOfUserAuthPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfUserPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemSnmpUserPrivDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemSnmpOneOfUserPrivPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfUserGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpUser:
    group: Union[SystemSnmpOneOfUserGroupOptionsDef1, OneOfUserGroupOptionsDef2]
    name: SystemSnmpOneOfUserNameOptionsDef
    auth: Optional[
        Union[
            SystemSnmpOneOfUserAuthOptionsDef1, OneOfUserAuthOptionsDef2, OneOfUserAuthOptionsDef3
        ]
    ] = _field(default=None)
    auth_password: Optional[
        Union[
            SystemSnmpOneOfUserAuthPasswordOptionsDef1,
            OneOfUserAuthPasswordOptionsDef2,
            OneOfUserAuthPasswordOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "authPassword"})
    priv: Optional[
        Union[
            SystemSnmpOneOfUserPrivOptionsDef1, OneOfUserPrivOptionsDef2, OneOfUserPrivOptionsDef3
        ]
    ] = _field(default=None)
    priv_password: Optional[
        Union[
            SystemSnmpOneOfUserPrivPasswordOptionsDef1,
            OneOfUserPrivPasswordOptionsDef2,
            OneOfUserPrivPasswordOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "privPassword"})


@dataclass
class SystemSnmpOneOfTargetVpnIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemSnmpOneOfTargetIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SystemSnmpOneOfTargetPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdwanSystemSnmpOneOfTargetCommunityNameUserLabelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfTargetCommunityNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfTargetUserOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfTargetSourceInterfaceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpTarget:
    ip: Union[SystemSnmpOneOfTargetIpOptionsDef1, OneOfTargetIpOptionsDef2]
    port: Union[SystemSnmpOneOfTargetPortOptionsDef1, OneOfTargetPortOptionsDef2]
    vpn_id: Union[SystemSnmpOneOfTargetVpnIdOptionsDef1, OneOfTargetVpnIdOptionsDef2] = _field(
        metadata={"alias": "vpnId"}
    )
    community_name: Optional[
        Union[SystemSnmpOneOfTargetCommunityNameOptionsDef1, OneOfTargetCommunityNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "communityName"})
    source_interface: Optional[
        Union[
            SystemSnmpOneOfTargetSourceInterfaceOptionsDef1, OneOfTargetSourceInterfaceOptionsDef2
        ]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})
    user: Optional[Union[SystemSnmpOneOfTargetUserOptionsDef1, OneOfTargetUserOptionsDef2]] = (
        _field(default=None)
    )
    user_label: Optional[
        FeatureProfileSdwanSystemSnmpOneOfTargetCommunityNameUserLabelOptionsDef
    ] = _field(default=None, metadata={"alias": "userLabel"})


@dataclass
class FeatureProfileSdwanSystemSnmpData:
    # Configure SNMP community
    community: Optional[List[SystemSnmpCommunity]] = _field(default=None)
    contact: Optional[
        Union[SystemSnmpOneOfContactOptionsDef1, OneOfContactOptionsDef2, OneOfContactOptionsDef3]
    ] = _field(default=None)
    # Configure an SNMP group
    group: Optional[List[SystemSnmpGroup]] = _field(default=None)
    location: Optional[
        Union[
            SystemSnmpOneOfLocationOptionsDef1, OneOfLocationOptionsDef2, OneOfLocationOptionsDef3
        ]
    ] = _field(default=None)
    shutdown: Optional[
        Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    ] = _field(default=None)
    # Configure SNMP server to receive SNMP traps
    target: Optional[List[SystemSnmpTarget]] = _field(default=None)
    # Configure an SNMP user
    user: Optional[List[SystemSnmpUser]] = _field(default=None)
    # Configure a view record
    view: Optional[List[SystemSnmpView]] = _field(default=None)


@dataclass
class EditSnmpProfileParcelForSystemPutRequest:
    """
    SNMP profile parcel schema for PUT request
    """

    data: FeatureProfileSdwanSystemSnmpData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
