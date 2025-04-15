# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .delete_all_lists.delete_all_lists_builder import DeleteAllListsBuilder
    from .referenced.referenced_builder import ReferencedBuilder
    from .sgt.sgt_builder import SgtBuilder
    from .usergroups.usergroups_builder import UsergroupsBuilder
    from .users.users_builder import UsersBuilder


class IdentityBuilder:
    """
    Builds and executes requests for operations under /template/policy/ise/identity
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def delete_all_lists(self) -> DeleteAllListsBuilder:
        """
        The deleteAllLists property
        """
        from .delete_all_lists.delete_all_lists_builder import DeleteAllListsBuilder

        return DeleteAllListsBuilder(self._request_adapter)

    @property
    def referenced(self) -> ReferencedBuilder:
        """
        The referenced property
        """
        from .referenced.referenced_builder import ReferencedBuilder

        return ReferencedBuilder(self._request_adapter)

    @property
    def sgt(self) -> SgtBuilder:
        """
        The sgt property
        """
        from .sgt.sgt_builder import SgtBuilder

        return SgtBuilder(self._request_adapter)

    @property
    def usergroups(self) -> UsergroupsBuilder:
        """
        The usergroups property
        """
        from .usergroups.usergroups_builder import UsergroupsBuilder

        return UsergroupsBuilder(self._request_adapter)

    @property
    def users(self) -> UsersBuilder:
        """
        The users property
        """
        from .users.users_builder import UsersBuilder

        return UsersBuilder(self._request_adapter)
