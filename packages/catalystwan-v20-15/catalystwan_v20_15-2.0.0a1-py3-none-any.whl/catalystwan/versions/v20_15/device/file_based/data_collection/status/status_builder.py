# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /device/file-based/data-collection/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, request_uuid: str, **kw) -> str:
        """
        Get Data Collection status for given Request UUID
        GET /dataservice/device/file-based/data-collection/status/{requestUUID}

        :param request_uuid: request UUID
        :returns: str
        """
        params = {
            "requestUUID": request_uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/file-based/data-collection/status/{requestUUID}",
            return_type=str,
            params=params,
            **kw,
        )
