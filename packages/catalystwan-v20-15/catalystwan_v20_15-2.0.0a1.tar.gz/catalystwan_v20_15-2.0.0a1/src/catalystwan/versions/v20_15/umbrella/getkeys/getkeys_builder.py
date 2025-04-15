# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .management.management_builder import ManagementBuilder
    from .networkdevices.networkdevices_builder import NetworkdevicesBuilder
    from .reporting.reporting_builder import ReportingBuilder


class GetkeysBuilder:
    """
    Builds and executes requests for operations under /umbrella/getkeys
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        Get keys from Umbrella
        GET /dataservice/umbrella/getkeys

        :returns: None
        """
        return self._request_adapter.request("GET", "/dataservice/umbrella/getkeys", **kw)

    @property
    def management(self) -> ManagementBuilder:
        """
        The management property
        """
        from .management.management_builder import ManagementBuilder

        return ManagementBuilder(self._request_adapter)

    @property
    def networkdevices(self) -> NetworkdevicesBuilder:
        """
        The networkdevices property
        """
        from .networkdevices.networkdevices_builder import NetworkdevicesBuilder

        return NetworkdevicesBuilder(self._request_adapter)

    @property
    def reporting(self) -> ReportingBuilder:
        """
        The reporting property
        """
        from .reporting.reporting_builder import ReportingBuilder

        return ReportingBuilder(self._request_adapter)
