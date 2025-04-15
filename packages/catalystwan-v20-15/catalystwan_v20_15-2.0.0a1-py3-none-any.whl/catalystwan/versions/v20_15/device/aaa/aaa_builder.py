# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .servers.servers_builder import ServersBuilder
    from .users.users_builder import UsersBuilder


class AaaBuilder:
    """
    Builds and executes requests for operations under /device/aaa
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def servers(self) -> ServersBuilder:
        """
        The servers property
        """
        from .servers.servers_builder import ServersBuilder

        return ServersBuilder(self._request_adapter)

    @property
    def users(self) -> UsersBuilder:
        """
        The users property
        """
        from .users.users_builder import UsersBuilder

        return UsersBuilder(self._request_adapter)
