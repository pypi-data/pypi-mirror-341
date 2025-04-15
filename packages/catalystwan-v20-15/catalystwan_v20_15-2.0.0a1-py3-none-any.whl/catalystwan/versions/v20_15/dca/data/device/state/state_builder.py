# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class StateBuilder:
    """
    Builds and executes requests for operations under /dca/data/device/state
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, state_data_type: str, payload: Any, **kw) -> Any:
        """
        Get device state data
        POST /dataservice/dca/data/device/state/{state_data_type}

        :param state_data_type: Device state data
        :param payload: Query string
        :returns: Any
        """
        params = {
            "state_data_type": state_data_type,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/dca/data/device/state/{state_data_type}",
            params=params,
            payload=payload,
            **kw,
        )
