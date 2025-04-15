# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class LxcinstallBuilder:
    """
    Builds and executes requests for operations under /device/action/lxcinstall
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Process an installation operation
        POST /dataservice/device/action/lxcinstall

        :param payload: Installation request payload
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/action/lxcinstall", payload=payload, **kw
        )
