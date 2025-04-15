# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class LinksBuilder:
    """
    Builds and executes requests for operations under /group/map/devices/links
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, group_id: Optional[str] = None, **kw) -> List[Any]:
        """
        Retrieve devices in group for map
        GET /dataservice/group/map/devices/links

        :param group_id: groupId
        :returns: List[Any]
        """
        params = {
            "groupId": group_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/group/map/devices/links",
            return_type=List[Any],
            params=params,
            **kw,
        )
