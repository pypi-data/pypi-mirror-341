# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface


class InterfacecolorBuilder:
    """
    Builds and executes requests for operations under /multicloud/interfacecolor
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[str]:
        """
        Get WAN interface colors
        GET /dataservice/multicloud/interfacecolor

        :returns: List[str]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/interfacecolor", return_type=List[str], **kw
        )
