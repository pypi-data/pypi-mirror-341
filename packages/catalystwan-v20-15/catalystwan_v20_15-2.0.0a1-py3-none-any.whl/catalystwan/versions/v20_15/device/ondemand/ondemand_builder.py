# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .local.local_builder import LocalBuilder
    from .remote.remote_builder import RemoteBuilder


class OndemandBuilder:
    """
    Builds and executes requests for operations under /device/ondemand
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def local(self) -> LocalBuilder:
        """
        The local property
        """
        from .local.local_builder import LocalBuilder

        return LocalBuilder(self._request_adapter)

    @property
    def remote(self) -> RemoteBuilder:
        """
        The remote property
        """
        from .remote.remote_builder import RemoteBuilder

        return RemoteBuilder(self._request_adapter)
