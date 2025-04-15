# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Optional


@dataclass
class UserObject:
    """
    Object containing the users name
    """

    ad_user_sam_account_name: Optional[str] = _field(
        default=None, metadata={"alias": "adUserSamAccountName"}
    )


@dataclass
class ErsActiveDirectoryUsers:
    users: Optional[List[UserObject]] = _field(default=None)


@dataclass
class UsersDataObject:
    """
    Data Object for Users get call
    """

    ers_active_directory_users: Optional[ErsActiveDirectoryUsers] = _field(
        default=None, metadata={"alias": "ERSActiveDirectoryUsers"}
    )


@dataclass
class HeaderObject:
    """
    Header for Response
    """

    columns: Optional[Any] = _field(default=None)
    fields: Optional[Any] = _field(default=None)
    generated_on: Optional[int] = _field(default=None, metadata={"alias": "generatedOn"})
    view_keys: Optional[Any] = _field(default=None, metadata={"alias": "viewKeys"})


@dataclass
class UsersResponse:
    """
    Users returned from ISE active directory domain
    """

    # Data Object for Users get call
    data: Optional[UsersDataObject] = _field(default=None)
    # Header for Response
    header: Optional[HeaderObject] = _field(default=None)


@dataclass
class UsersBody:
    """
    Users body with regex filter for which users to retrieve from ISE
    """

    filter: Optional[str] = _field(default=None)
