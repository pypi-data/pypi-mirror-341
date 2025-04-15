# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cloudx.cloudx_builder import CloudxBuilder
    from .links.links_builder import LinksBuilder
    from .mcastautodiscoveradvt.mcastautodiscoveradvt_builder import McastautodiscoveradvtBuilder
    from .mcastautodiscoverrecv.mcastautodiscoverrecv_builder import McastautodiscoverrecvBuilder
    from .mcastroutesadvt.mcastroutesadvt_builder import McastroutesadvtBuilder
    from .mcastroutesrecv.mcastroutesrecv_builder import McastroutesrecvBuilder
    from .peers.peers_builder import PeersBuilder
    from .routes.routes_builder import RoutesBuilder
    from .services.services_builder import ServicesBuilder
    from .status.status_builder import StatusBuilder
    from .summary.summary_builder import SummaryBuilder
    from .synced.synced_builder import SyncedBuilder
    from .tlocs.tlocs_builder import TlocsBuilder


class OmpBuilder:
    """
    Builds and executes requests for operations under /device/omp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def cloudx(self) -> CloudxBuilder:
        """
        The cloudx property
        """
        from .cloudx.cloudx_builder import CloudxBuilder

        return CloudxBuilder(self._request_adapter)

    @property
    def links(self) -> LinksBuilder:
        """
        The links property
        """
        from .links.links_builder import LinksBuilder

        return LinksBuilder(self._request_adapter)

    @property
    def mcastautodiscoveradvt(self) -> McastautodiscoveradvtBuilder:
        """
        The mcastautodiscoveradvt property
        """
        from .mcastautodiscoveradvt.mcastautodiscoveradvt_builder import (
            McastautodiscoveradvtBuilder,
        )

        return McastautodiscoveradvtBuilder(self._request_adapter)

    @property
    def mcastautodiscoverrecv(self) -> McastautodiscoverrecvBuilder:
        """
        The mcastautodiscoverrecv property
        """
        from .mcastautodiscoverrecv.mcastautodiscoverrecv_builder import (
            McastautodiscoverrecvBuilder,
        )

        return McastautodiscoverrecvBuilder(self._request_adapter)

    @property
    def mcastroutesadvt(self) -> McastroutesadvtBuilder:
        """
        The mcastroutesadvt property
        """
        from .mcastroutesadvt.mcastroutesadvt_builder import McastroutesadvtBuilder

        return McastroutesadvtBuilder(self._request_adapter)

    @property
    def mcastroutesrecv(self) -> McastroutesrecvBuilder:
        """
        The mcastroutesrecv property
        """
        from .mcastroutesrecv.mcastroutesrecv_builder import McastroutesrecvBuilder

        return McastroutesrecvBuilder(self._request_adapter)

    @property
    def peers(self) -> PeersBuilder:
        """
        The peers property
        """
        from .peers.peers_builder import PeersBuilder

        return PeersBuilder(self._request_adapter)

    @property
    def routes(self) -> RoutesBuilder:
        """
        The routes property
        """
        from .routes.routes_builder import RoutesBuilder

        return RoutesBuilder(self._request_adapter)

    @property
    def services(self) -> ServicesBuilder:
        """
        The services property
        """
        from .services.services_builder import ServicesBuilder

        return ServicesBuilder(self._request_adapter)

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
    def tlocs(self) -> TlocsBuilder:
        """
        The tlocs property
        """
        from .tlocs.tlocs_builder import TlocsBuilder

        return TlocsBuilder(self._request_adapter)
