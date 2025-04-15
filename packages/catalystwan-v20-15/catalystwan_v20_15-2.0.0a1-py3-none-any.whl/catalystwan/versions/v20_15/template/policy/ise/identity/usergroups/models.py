# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Optional


@dataclass
class UsergroupObject:
    name: Optional[str] = _field(default=None)
    sid: Optional[str] = _field(default=None)
    type_: Optional[str] = _field(default=None, metadata={"alias": "type"})


@dataclass
class ErsActiveDirectoryGroups:
    groups: Optional[List[UsergroupObject]] = _field(default=None)


@dataclass
class UserGroupsDataObject:
    """
    Data Object for Users Groups call
    """

    ers_active_directory_groups: Optional[ErsActiveDirectoryGroups] = _field(
        default=None, metadata={"alias": "ERSActiveDirectoryGroups"}
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
class UserGroupsResponse:
    """
    User Groups Data from ISE active directory domain
    """

    # Data Object for Users Groups call
    data: Optional[UserGroupsDataObject] = _field(default=None)
    # Header for Response
    header: Optional[HeaderObject] = _field(default=None)


@dataclass
class UserGroupsBody:
    filter: Optional[str] = _field(default=None)
