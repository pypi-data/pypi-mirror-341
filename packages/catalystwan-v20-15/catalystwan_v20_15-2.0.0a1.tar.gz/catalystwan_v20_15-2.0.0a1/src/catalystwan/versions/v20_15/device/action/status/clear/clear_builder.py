# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface


class ClearBuilder:
    """
    Builds and executes requests for operations under /device/action/status/clear
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(self, process_id: Optional[str] = None, **kw):
        """
        Delete status of action
        DELETE /dataservice/device/action/status/clear

        :param process_id: Process Id
        :returns: None
        """
        params = {
            "processId": process_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/device/action/status/clear", params=params, **kw
        )
