# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .peers.peers_builder import PeersBuilder


class SyncedBuilder:
    """
    Builds and executes requests for operations under /device/omp/synced
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def peers(self) -> PeersBuilder:
        """
        The peers property
        """
        from .peers.peers_builder import PeersBuilder

        return PeersBuilder(self._request_adapter)
