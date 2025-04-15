# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class FileBuilder:
    """
    Builds and executes requests for operations under /template/device/config/process/input/file
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> str:
        """
        Process input comma separated file


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/template/device/config/process/input/file

        :param payload: Device template
        :returns: str
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/template/device/config/process/input/file",
            return_type=str,
            payload=payload,
            **kw,
        )
