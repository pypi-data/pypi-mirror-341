# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

UserRoleDef = Literal["administrators", "auditors", "operators"]

AuthOrderAuthenticationDef = Literal["local", "tacacs"]

TacacsKeyEnumDef = Literal["0", "7"]

DefaultOptionTypeDef = Literal["default"]

Value = Literal["0"]

RadiusKeyEnumDef = Literal["0", "7"]

AaaUserRoleDef = Literal["administrators", "auditors", "operators"]

AaaAuthOrderAuthenticationDef = Literal["local", "tacacs"]

AaaTacacsKeyEnumDef = Literal["0", "7"]

AaaRadiusKeyEnumDef = Literal["0", "7"]

SystemAaaUserRoleDef = Literal["administrators", "auditors", "operators"]

SystemAaaAuthOrderAuthenticationDef = Literal["local", "tacacs"]

SystemAaaTacacsKeyEnumDef = Literal["0", "7"]

SystemAaaRadiusKeyEnumDef = Literal["0", "7"]


@dataclass
class CreateNfvirtualAaaParcelPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


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
class OneOfUserRoleOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UserRoleDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUserRoleOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class User:
    name: Union[OneOfUserNameOptionsDef1, OneOfUserNameOptionsDef2]
    nfvis_password: Union[OneOfUserPasswordOptionsDef1, OneOfUserPasswordOptionsDef2] = _field(
        metadata={"alias": "nfvisPassword"}
    )
    role: Union[OneOfUserRoleOptionsDef1, OneOfUserRoleOptionsDef2]


@dataclass
class OneOfAuthOrderAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AuthOrderAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAuthOrderAuthenticationOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class AuthOrder:
    authentication: Union[
        OneOfAuthOrderAuthenticationOptionsDef1, OneOfAuthOrderAuthenticationOptionsDef2
    ]


@dataclass
class OneOfTacacsHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfTacacsHostOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTacacsKeyEnumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TacacsKeyEnumDef


@dataclass
class OneOfTacacsKeyEnumOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTacacsKeyEnumOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTacacsSharedSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTacacsSharedSecretOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTacacsAdminPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTacacsAdminPrivOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTacacsAdminPrivOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTacacsOperPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTacacsOperPrivOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTacacsOperPrivOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Tacacs:
    host: Union[OneOfTacacsHostOptionsDef1, OneOfTacacsHostOptionsDef2]
    admin_priv: Optional[
        Union[
            OneOfTacacsAdminPrivOptionsDef1,
            OneOfTacacsAdminPrivOptionsDef2,
            OneOfTacacsAdminPrivOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "admin-priv"})
    key: Optional[
        Union[
            OneOfTacacsKeyEnumOptionsDef1,
            OneOfTacacsKeyEnumOptionsDef2,
            OneOfTacacsKeyEnumOptionsDef3,
        ]
    ] = _field(default=None)
    oper_priv: Optional[
        Union[
            OneOfTacacsOperPrivOptionsDef1,
            OneOfTacacsOperPrivOptionsDef2,
            OneOfTacacsOperPrivOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "oper-priv"})
    shared_secret: Optional[
        Union[OneOfTacacsSharedSecretOptionsDef1, OneOfTacacsSharedSecretOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shared-secret"})


@dataclass
class OneOfRadiusHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfRadiusHostOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusKeyEnumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RadiusKeyEnumDef


@dataclass
class OneOfRadiusKeyEnumOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusKeyEnumOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRadiusSharedSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRadiusSharedSecretOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusAdminPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusAdminPrivOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusAdminPrivOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusOperPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusOperPrivOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusOperPrivOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Radius:
    host: Union[OneOfRadiusHostOptionsDef1, OneOfRadiusHostOptionsDef2]
    admin_priv: Optional[
        Union[
            OneOfRadiusAdminPrivOptionsDef1,
            OneOfRadiusAdminPrivOptionsDef2,
            OneOfRadiusAdminPrivOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "admin-priv"})
    key: Optional[
        Union[
            OneOfRadiusKeyEnumOptionsDef1,
            OneOfRadiusKeyEnumOptionsDef2,
            OneOfRadiusKeyEnumOptionsDef3,
        ]
    ] = _field(default=None)
    oper_priv: Optional[
        Union[
            OneOfRadiusOperPrivOptionsDef1,
            OneOfRadiusOperPrivOptionsDef2,
            OneOfRadiusOperPrivOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "oper-priv"})
    shared_secret: Optional[
        Union[OneOfRadiusSharedSecretOptionsDef1, OneOfRadiusSharedSecretOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shared-secret"})


@dataclass
class Data:
    # Set order to try different authentication methods
    auth_order: Optional[List[AuthOrder]] = _field(default=None, metadata={"alias": "auth-order"})
    # Configure the RADIUS server
    radius: Optional[List[Radius]] = _field(default=None)
    # Configure the TACACS server
    tacacs: Optional[List[Tacacs]] = _field(default=None)
    # Create local login account
    user: Optional[List[User]] = _field(default=None)


@dataclass
class CreateNfvirtualAaaParcelPostRequest:
    """
    AAA profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


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
class AaaOneOfUserRoleOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaUserRoleDef  # pytype: disable=annotation-type-mismatch


@dataclass
class AaaUser:
    name: Union[AaaOneOfUserNameOptionsDef1, OneOfUserNameOptionsDef2]
    nfvis_password: Union[AaaOneOfUserPasswordOptionsDef1, OneOfUserPasswordOptionsDef2] = _field(
        metadata={"alias": "nfvisPassword"}
    )
    role: Union[AaaOneOfUserRoleOptionsDef1, OneOfUserRoleOptionsDef2]


@dataclass
class AaaOneOfAuthOrderAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaAuthOrderAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class AaaAuthOrder:
    authentication: Union[
        AaaOneOfAuthOrderAuthenticationOptionsDef1, OneOfAuthOrderAuthenticationOptionsDef2
    ]


@dataclass
class AaaOneOfTacacsHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class AaaOneOfTacacsKeyEnumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaTacacsKeyEnumDef


@dataclass
class AaaOneOfTacacsSharedSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AaaOneOfTacacsAdminPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaOneOfTacacsOperPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaTacacs:
    host: Union[AaaOneOfTacacsHostOptionsDef1, OneOfTacacsHostOptionsDef2]
    admin_priv: Optional[
        Union[
            AaaOneOfTacacsAdminPrivOptionsDef1,
            OneOfTacacsAdminPrivOptionsDef2,
            OneOfTacacsAdminPrivOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "admin-priv"})
    key: Optional[
        Union[
            AaaOneOfTacacsKeyEnumOptionsDef1,
            OneOfTacacsKeyEnumOptionsDef2,
            OneOfTacacsKeyEnumOptionsDef3,
        ]
    ] = _field(default=None)
    oper_priv: Optional[
        Union[
            AaaOneOfTacacsOperPrivOptionsDef1,
            OneOfTacacsOperPrivOptionsDef2,
            OneOfTacacsOperPrivOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "oper-priv"})
    shared_secret: Optional[
        Union[AaaOneOfTacacsSharedSecretOptionsDef1, OneOfTacacsSharedSecretOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shared-secret"})


@dataclass
class AaaOneOfRadiusHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class AaaOneOfRadiusKeyEnumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AaaRadiusKeyEnumDef


@dataclass
class AaaOneOfRadiusSharedSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AaaOneOfRadiusAdminPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaOneOfRadiusOperPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaRadius:
    host: Union[AaaOneOfRadiusHostOptionsDef1, OneOfRadiusHostOptionsDef2]
    admin_priv: Optional[
        Union[
            AaaOneOfRadiusAdminPrivOptionsDef1,
            OneOfRadiusAdminPrivOptionsDef2,
            OneOfRadiusAdminPrivOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "admin-priv"})
    key: Optional[
        Union[
            AaaOneOfRadiusKeyEnumOptionsDef1,
            OneOfRadiusKeyEnumOptionsDef2,
            OneOfRadiusKeyEnumOptionsDef3,
        ]
    ] = _field(default=None)
    oper_priv: Optional[
        Union[
            AaaOneOfRadiusOperPrivOptionsDef1,
            OneOfRadiusOperPrivOptionsDef2,
            OneOfRadiusOperPrivOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "oper-priv"})
    shared_secret: Optional[
        Union[AaaOneOfRadiusSharedSecretOptionsDef1, OneOfRadiusSharedSecretOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shared-secret"})


@dataclass
class AaaData:
    # Set order to try different authentication methods
    auth_order: Optional[List[AaaAuthOrder]] = _field(
        default=None, metadata={"alias": "auth-order"}
    )
    # Configure the RADIUS server
    radius: Optional[List[AaaRadius]] = _field(default=None)
    # Configure the TACACS server
    tacacs: Optional[List[AaaTacacs]] = _field(default=None)
    # Create local login account
    user: Optional[List[AaaUser]] = _field(default=None)


@dataclass
class Payload:
    """
    AAA profile parcel schema for PUT request
    """

    data: AaaData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleNfvirtualSystemAaaPayload:
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
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditNfvirtualAaaParcelPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


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
class SystemAaaOneOfUserRoleOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaUserRoleDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemAaaUser:
    name: Union[SystemAaaOneOfUserNameOptionsDef1, OneOfUserNameOptionsDef2]
    nfvis_password: Union[SystemAaaOneOfUserPasswordOptionsDef1, OneOfUserPasswordOptionsDef2] = (
        _field(metadata={"alias": "nfvisPassword"})
    )
    role: Union[SystemAaaOneOfUserRoleOptionsDef1, OneOfUserRoleOptionsDef2]


@dataclass
class SystemAaaOneOfAuthOrderAuthenticationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaAuthOrderAuthenticationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemAaaAuthOrder:
    authentication: Union[
        SystemAaaOneOfAuthOrderAuthenticationOptionsDef1, OneOfAuthOrderAuthenticationOptionsDef2
    ]


@dataclass
class SystemAaaOneOfTacacsHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SystemAaaOneOfTacacsKeyEnumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaTacacsKeyEnumDef


@dataclass
class SystemAaaOneOfTacacsSharedSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemAaaOneOfTacacsAdminPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaOneOfTacacsOperPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaTacacs:
    host: Union[SystemAaaOneOfTacacsHostOptionsDef1, OneOfTacacsHostOptionsDef2]
    admin_priv: Optional[
        Union[
            SystemAaaOneOfTacacsAdminPrivOptionsDef1,
            OneOfTacacsAdminPrivOptionsDef2,
            OneOfTacacsAdminPrivOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "admin-priv"})
    key: Optional[
        Union[
            SystemAaaOneOfTacacsKeyEnumOptionsDef1,
            OneOfTacacsKeyEnumOptionsDef2,
            OneOfTacacsKeyEnumOptionsDef3,
        ]
    ] = _field(default=None)
    oper_priv: Optional[
        Union[
            SystemAaaOneOfTacacsOperPrivOptionsDef1,
            OneOfTacacsOperPrivOptionsDef2,
            OneOfTacacsOperPrivOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "oper-priv"})
    shared_secret: Optional[
        Union[SystemAaaOneOfTacacsSharedSecretOptionsDef1, OneOfTacacsSharedSecretOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shared-secret"})


@dataclass
class SystemAaaOneOfRadiusHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SystemAaaOneOfRadiusKeyEnumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemAaaRadiusKeyEnumDef


@dataclass
class SystemAaaOneOfRadiusSharedSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemAaaOneOfRadiusAdminPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaOneOfRadiusOperPrivOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemAaaRadius:
    host: Union[SystemAaaOneOfRadiusHostOptionsDef1, OneOfRadiusHostOptionsDef2]
    admin_priv: Optional[
        Union[
            SystemAaaOneOfRadiusAdminPrivOptionsDef1,
            OneOfRadiusAdminPrivOptionsDef2,
            OneOfRadiusAdminPrivOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "admin-priv"})
    key: Optional[
        Union[
            SystemAaaOneOfRadiusKeyEnumOptionsDef1,
            OneOfRadiusKeyEnumOptionsDef2,
            OneOfRadiusKeyEnumOptionsDef3,
        ]
    ] = _field(default=None)
    oper_priv: Optional[
        Union[
            SystemAaaOneOfRadiusOperPrivOptionsDef1,
            OneOfRadiusOperPrivOptionsDef2,
            OneOfRadiusOperPrivOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "oper-priv"})
    shared_secret: Optional[
        Union[SystemAaaOneOfRadiusSharedSecretOptionsDef1, OneOfRadiusSharedSecretOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shared-secret"})


@dataclass
class SystemAaaData:
    # Set order to try different authentication methods
    auth_order: Optional[List[SystemAaaAuthOrder]] = _field(
        default=None, metadata={"alias": "auth-order"}
    )
    # Configure the RADIUS server
    radius: Optional[List[SystemAaaRadius]] = _field(default=None)
    # Configure the TACACS server
    tacacs: Optional[List[SystemAaaTacacs]] = _field(default=None)
    # Create local login account
    user: Optional[List[SystemAaaUser]] = _field(default=None)


@dataclass
class EditNfvirtualAaaParcelPutRequest:
    """
    AAA profile parcel schema for PUT request
    """

    data: SystemAaaData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
