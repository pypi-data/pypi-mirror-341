# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .headends.headends_builder import HeadendsBuilder
    from .sessions.sessions_builder import SessionsBuilder


class SdraBuilder:
    """
    Builds and executes requests for operations under /statistics/sdra
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def headends(self) -> HeadendsBuilder:
        """
        The headends property
        """
        from .headends.headends_builder import HeadendsBuilder

        return HeadendsBuilder(self._request_adapter)

    @property
    def sessions(self) -> SessionsBuilder:
        """
        The sessions property
        """
        from .sessions.sessions_builder import SessionsBuilder

        return SessionsBuilder(self._request_adapter)
