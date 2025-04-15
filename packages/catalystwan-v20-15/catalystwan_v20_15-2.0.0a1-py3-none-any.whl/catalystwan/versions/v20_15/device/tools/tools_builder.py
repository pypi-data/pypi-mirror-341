# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .admintech.admintech_builder import AdmintechBuilder
    from .admintechlist.admintechlist_builder import AdmintechlistBuilder
    from .admintechs.admintechs_builder import AdmintechsBuilder
    from .factoryreset.factoryreset_builder import FactoryresetBuilder
    from .netstat.netstat_builder import NetstatBuilder
    from .nping.nping_builder import NpingBuilder
    from .nslookup.nslookup_builder import NslookupBuilder
    from .ping.ping_builder import PingBuilder
    from .porthopcolor.porthopcolor_builder import PorthopcolorBuilder
    from .realtimeinfo.realtimeinfo_builder import RealtimeinfoBuilder
    from .reset.reset_builder import ResetBuilder
    from .resetuser.resetuser_builder import ResetuserBuilder
    from .servicepath.servicepath_builder import ServicepathBuilder
    from .ss.ss_builder import SsBuilder
    from .system_netfilter.system_netfilter_builder import SystemNetfilterBuilder
    from .traceroute.traceroute_builder import TracerouteBuilder
    from .tunnelpath.tunnelpath_builder import TunnelpathBuilder


class ToolsBuilder:
    """
    Builds and executes requests for operations under /device/tools
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def admintech(self) -> AdmintechBuilder:
        """
        The admintech property
        """
        from .admintech.admintech_builder import AdmintechBuilder

        return AdmintechBuilder(self._request_adapter)

    @property
    def admintechlist(self) -> AdmintechlistBuilder:
        """
        The admintechlist property
        """
        from .admintechlist.admintechlist_builder import AdmintechlistBuilder

        return AdmintechlistBuilder(self._request_adapter)

    @property
    def admintechs(self) -> AdmintechsBuilder:
        """
        The admintechs property
        """
        from .admintechs.admintechs_builder import AdmintechsBuilder

        return AdmintechsBuilder(self._request_adapter)

    @property
    def factoryreset(self) -> FactoryresetBuilder:
        """
        The factoryreset property
        """
        from .factoryreset.factoryreset_builder import FactoryresetBuilder

        return FactoryresetBuilder(self._request_adapter)

    @property
    def netstat(self) -> NetstatBuilder:
        """
        The netstat property
        """
        from .netstat.netstat_builder import NetstatBuilder

        return NetstatBuilder(self._request_adapter)

    @property
    def nping(self) -> NpingBuilder:
        """
        The nping property
        """
        from .nping.nping_builder import NpingBuilder

        return NpingBuilder(self._request_adapter)

    @property
    def nslookup(self) -> NslookupBuilder:
        """
        The nslookup property
        """
        from .nslookup.nslookup_builder import NslookupBuilder

        return NslookupBuilder(self._request_adapter)

    @property
    def ping(self) -> PingBuilder:
        """
        The ping property
        """
        from .ping.ping_builder import PingBuilder

        return PingBuilder(self._request_adapter)

    @property
    def porthopcolor(self) -> PorthopcolorBuilder:
        """
        The porthopcolor property
        """
        from .porthopcolor.porthopcolor_builder import PorthopcolorBuilder

        return PorthopcolorBuilder(self._request_adapter)

    @property
    def realtimeinfo(self) -> RealtimeinfoBuilder:
        """
        The realtimeinfo property
        """
        from .realtimeinfo.realtimeinfo_builder import RealtimeinfoBuilder

        return RealtimeinfoBuilder(self._request_adapter)

    @property
    def reset(self) -> ResetBuilder:
        """
        The reset property
        """
        from .reset.reset_builder import ResetBuilder

        return ResetBuilder(self._request_adapter)

    @property
    def resetuser(self) -> ResetuserBuilder:
        """
        The resetuser property
        """
        from .resetuser.resetuser_builder import ResetuserBuilder

        return ResetuserBuilder(self._request_adapter)

    @property
    def servicepath(self) -> ServicepathBuilder:
        """
        The servicepath property
        """
        from .servicepath.servicepath_builder import ServicepathBuilder

        return ServicepathBuilder(self._request_adapter)

    @property
    def ss(self) -> SsBuilder:
        """
        The ss property
        """
        from .ss.ss_builder import SsBuilder

        return SsBuilder(self._request_adapter)

    @property
    def system_netfilter(self) -> SystemNetfilterBuilder:
        """
        The system-netfilter property
        """
        from .system_netfilter.system_netfilter_builder import SystemNetfilterBuilder

        return SystemNetfilterBuilder(self._request_adapter)

    @property
    def traceroute(self) -> TracerouteBuilder:
        """
        The traceroute property
        """
        from .traceroute.traceroute_builder import TracerouteBuilder

        return TracerouteBuilder(self._request_adapter)

    @property
    def tunnelpath(self) -> TunnelpathBuilder:
        """
        The tunnelpath property
        """
        from .tunnelpath.tunnelpath_builder import TunnelpathBuilder

        return TunnelpathBuilder(self._request_adapter)
