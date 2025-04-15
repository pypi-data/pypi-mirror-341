# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class AttachBootStrapBuilder:
    """
    Builds and executes requests for operations under /template/device/config/attachBootStrap
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Attach feature device template


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/template/device/config/attachBootStrap

        :param payload: Device template
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/device/config/attachBootStrap", payload=payload, **kw
        )
