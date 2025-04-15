# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class CountBuilder:
    """
    Builds and executes requests for operations under /device/control/count
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, is_cached: Optional[bool] = False, site_id: Optional[str] = None, **kw) -> Any:
        """
        Get number of vedges and vsmart device in different control states
        GET /dataservice/device/control/count

        :param is_cached: Device State cached
        :param site_id: Optional site ID  to filter devices
        :returns: Any
        """
        params = {
            "isCached": is_cached,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/control/count", params=params, **kw
        )
