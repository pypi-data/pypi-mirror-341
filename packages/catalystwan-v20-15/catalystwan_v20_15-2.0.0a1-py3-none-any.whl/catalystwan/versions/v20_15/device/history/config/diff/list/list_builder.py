# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ListBuilder:
    """
    Builds and executes requests for operations under /device/history/config/diff/list
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, config_id1: str, config_id2: str, **kw) -> Any:
        """
        Get diff of two configs
        GET /dataservice/device/history/config/diff/list

        :param config_id1: Config Id one
        :param config_id2: Config Id two
        :returns: Any
        """
        params = {
            "config_id1": config_id1,
            "config_id2": config_id2,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/history/config/diff/list", params=params, **kw
        )
