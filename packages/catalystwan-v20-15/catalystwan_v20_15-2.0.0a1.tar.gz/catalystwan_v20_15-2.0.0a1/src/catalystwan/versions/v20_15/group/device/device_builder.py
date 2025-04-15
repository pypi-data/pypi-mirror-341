# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class DeviceBuilder:
    """
    Builds and executes requests for operations under /group/device
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, site_id: Optional[str] = None, **kw) -> List[Any]:
        """
        Retrieve device groups
        GET /dataservice/group/device

        :param site_id: siteId
        :returns: List[Any]
        """
        params = {
            "siteId": site_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/group/device", return_type=List[Any], params=params, **kw
        )
