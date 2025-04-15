# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class CancelBuilder:
    """
    Builds and executes requests for operations under /device/action/status/cancel
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, process_id: str, **kw):
        """
        Bulk cancel task status
        POST /dataservice/device/action/status/cancel/{processId}

        :param process_id: Process Id
        :returns: None
        """
        params = {
            "processId": process_id,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/device/action/status/cancel/{processId}", params=params, **kw
        )
