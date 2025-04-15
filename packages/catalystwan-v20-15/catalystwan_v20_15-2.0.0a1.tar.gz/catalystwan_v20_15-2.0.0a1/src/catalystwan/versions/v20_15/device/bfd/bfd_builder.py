# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .history.history_builder import HistoryBuilder
    from .links.links_builder import LinksBuilder
    from .sessions.sessions_builder import SessionsBuilder
    from .sites.sites_builder import SitesBuilder
    from .state.state_builder import StateBuilder
    from .status.status_builder import StatusBuilder
    from .summary.summary_builder import SummaryBuilder
    from .synced.synced_builder import SyncedBuilder
    from .tloc.tloc_builder import TlocBuilder


class BfdBuilder:
    """
    Builds and executes requests for operations under /device/bfd
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def history(self) -> HistoryBuilder:
        """
        The history property
        """
        from .history.history_builder import HistoryBuilder

        return HistoryBuilder(self._request_adapter)

    @property
    def links(self) -> LinksBuilder:
        """
        The links property
        """
        from .links.links_builder import LinksBuilder

        return LinksBuilder(self._request_adapter)

    @property
    def sessions(self) -> SessionsBuilder:
        """
        The sessions property
        """
        from .sessions.sessions_builder import SessionsBuilder

        return SessionsBuilder(self._request_adapter)

    @property
    def sites(self) -> SitesBuilder:
        """
        The sites property
        """
        from .sites.sites_builder import SitesBuilder

        return SitesBuilder(self._request_adapter)

    @property
    def state(self) -> StateBuilder:
        """
        The state property
        """
        from .state.state_builder import StateBuilder

        return StateBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)

    @property
    def synced(self) -> SyncedBuilder:
        """
        The synced property
        """
        from .synced.synced_builder import SyncedBuilder

        return SyncedBuilder(self._request_adapter)

    @property
    def tloc(self) -> TlocBuilder:
        """
        The tloc property
        """
        from .tloc.tloc_builder import TlocBuilder

        return TlocBuilder(self._request_adapter)
