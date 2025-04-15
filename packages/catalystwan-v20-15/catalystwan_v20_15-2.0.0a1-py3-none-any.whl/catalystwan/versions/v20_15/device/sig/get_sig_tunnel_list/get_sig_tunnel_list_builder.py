# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class GetSigTunnelListBuilder:
    """
    Builds and executes requests for operations under /device/sig/getSigTunnelList
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        page_size: Optional[str] = None,
        offset: Optional[str] = None,
        last_n_hours: Optional[str] = None,
        site_id: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        get Sig TunnelList
        GET /dataservice/device/sig/getSigTunnelList

        :param page_size: Page Size
        :param offset: Page offset
        :param last_n_hours: last n hours
        :param site_id: Optional site ID  to filter devices
        :returns: Any
        """
        params = {
            "pageSize": page_size,
            "offset": offset,
            "lastNHours": last_n_hours,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/sig/getSigTunnelList", params=params, **kw
        )
