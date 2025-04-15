# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .import_.import_builder import ImportBuilder
    from .remoteimport.remoteimport_builder import RemoteimportBuilder


class RestoreBuilder:
    """
    Builds and executes requests for operations under /restore
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def import_(self) -> ImportBuilder:
        """
        The import property
        """
        from .import_.import_builder import ImportBuilder

        return ImportBuilder(self._request_adapter)

    @property
    def remoteimport(self) -> RemoteimportBuilder:
        """
        The remoteimport property
        """
        from .remoteimport.remoteimport_builder import RemoteimportBuilder

        return RemoteimportBuilder(self._request_adapter)
