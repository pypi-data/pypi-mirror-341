# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class DetailBuilder:
    """
    Builds and executes requests for operations under /device/tlocutil/detail
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, util: Optional[str] = None, site_id: Optional[str] = None, **kw) -> Any:
        """
        Get detailed TLOC list
        GET /dataservice/device/tlocutil/detail

        :param util: Tloc util
        :param site_id: Optional site ID  to filter devices
        :returns: Any
        """
        params = {
            "util": util,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/tlocutil/detail", params=params, **kw
        )
