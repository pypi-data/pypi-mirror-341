# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .domain.domain_builder import DomainBuilder
    from .ipaddress.ipaddress_builder import IpaddressBuilder
    from .webex.webex_builder import WebexBuilder


class SdavccloudconnectorBuilder:
    """
    Builds and executes requests for operations under /monitor/sdavccloudconnector
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def domain(self) -> DomainBuilder:
        """
        The domain property
        """
        from .domain.domain_builder import DomainBuilder

        return DomainBuilder(self._request_adapter)

    @property
    def ipaddress(self) -> IpaddressBuilder:
        """
        The ipaddress property
        """
        from .ipaddress.ipaddress_builder import IpaddressBuilder

        return IpaddressBuilder(self._request_adapter)

    @property
    def webex(self) -> WebexBuilder:
        """
        The webex property
        """
        from .webex.webex_builder import WebexBuilder

        return WebexBuilder(self._request_adapter)
