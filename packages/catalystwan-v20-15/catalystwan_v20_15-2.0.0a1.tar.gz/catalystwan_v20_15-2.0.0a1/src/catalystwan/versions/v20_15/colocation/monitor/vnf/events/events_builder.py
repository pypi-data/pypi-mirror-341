# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging

from catalystwan.abc import RequestAdapterInterface


class EventsBuilder:
    """
    Builds and executes requests for operations under /colocation/monitor/vnf/events
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, vnf_name: str, **kw):
        """
        Get event detail of VNF
        GET /dataservice/colocation/monitor/vnf/events

        :param vnf_name: Vnf name
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "getVNFEventsDetail")
        params = {
            "vnfName": vnf_name,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/colocation/monitor/vnf/events", params=params, **kw
        )
