# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .sessions.sessions_builder import SessionsBuilder


class SyncedBuilder:
    """
    Builds and executes requests for operations under /device/bfd/synced
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def sessions(self) -> SessionsBuilder:
        """
        The sessions property
        """
        from .sessions.sessions_builder import SessionsBuilder

        return SessionsBuilder(self._request_adapter)
