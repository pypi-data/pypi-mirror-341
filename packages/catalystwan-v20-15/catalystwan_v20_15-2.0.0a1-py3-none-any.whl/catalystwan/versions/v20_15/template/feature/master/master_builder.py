# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class MasterBuilder:
    """
    Builds and executes requests for operations under /template/feature/master
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, type_name: str, **kw) -> Any:
        """
        Generate template type definition by device type


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/template/feature/master/{type_name}

        :param type_name: Device type
        :returns: Any
        """
        params = {
            "type_name": type_name,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/feature/master/{type_name}", params=params, **kw
        )
