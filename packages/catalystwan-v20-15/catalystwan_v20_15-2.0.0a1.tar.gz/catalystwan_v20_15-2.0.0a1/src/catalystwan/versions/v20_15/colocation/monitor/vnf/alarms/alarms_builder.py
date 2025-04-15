# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .count.count_builder import CountBuilder


class AlarmsBuilder:
    """
    Builds and executes requests for operations under /colocation/monitor/vnf/alarms
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, user_group: str, **kw):
        """
        Get event detail of VNF
        GET /dataservice/colocation/monitor/vnf/alarms

        :param user_group: User group
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "getVNFEventsCountDetail")
        params = {
            "user_group": user_group,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/colocation/monitor/vnf/alarms", params=params, **kw
        )

    @property
    def count(self) -> CountBuilder:
        """
        The count property
        """
        from .count.count_builder import CountBuilder

        return CountBuilder(self._request_adapter)
