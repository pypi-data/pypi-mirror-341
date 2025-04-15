# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .rootcertchain.rootcertchain_builder import RootcertchainBuilder


class SyncBuilder:
    """
    Builds and executes requests for operations under /system/device/sync
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def rootcertchain(self) -> RootcertchainBuilder:
        """
        The rootcertchain property
        """
        from .rootcertchain.rootcertchain_builder import RootcertchainBuilder

        return RootcertchainBuilder(self._request_adapter)
