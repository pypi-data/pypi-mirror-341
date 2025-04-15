# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class KeyvalueBuilder:
    """
    Builds and executes requests for operations under /device/keyvalue
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, site_id: Optional[str] = None, **kw) -> Any:
        """
        Get vEdge inventory as key value (key as systemIp value as hostName)
        GET /dataservice/device/keyvalue

        :param site_id: Optional site ID  to filter devices
        :returns: Any
        """
        params = {
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/keyvalue", params=params, **kw
        )
