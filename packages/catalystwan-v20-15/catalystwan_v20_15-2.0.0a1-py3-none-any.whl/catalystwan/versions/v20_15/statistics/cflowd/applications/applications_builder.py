# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .summary.summary_builder import SummaryBuilder


class ApplicationsBuilder:
    """
    Builds and executes requests for operations under /statistics/cflowd/applications
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        vpn: Optional[str] = None,
        device_id: Optional[str] = None,
        limit: Optional[int] = None,
        query: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Generate cflowd flows list in a grid table
        GET /dataservice/statistics/cflowd/applications

        :param vpn: VPN Id
        :param device_id: Device IP
        :param limit: Limit
        :param query: Query
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "createFlowsGrid")
        params = {
            "vpn": vpn,
            "deviceId": device_id,
            "limit": limit,
            "query": query,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/statistics/cflowd/applications", params=params, **kw
        )

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)
