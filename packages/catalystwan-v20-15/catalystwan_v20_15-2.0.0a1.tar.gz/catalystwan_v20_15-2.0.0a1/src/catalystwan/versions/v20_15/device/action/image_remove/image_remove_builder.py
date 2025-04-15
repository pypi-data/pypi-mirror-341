# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ImageRemoveBuilder:
    """
    Builds and executes requests for operations under /device/action/image-remove
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Process remove software image operation
        POST /dataservice/device/action/image-remove

        :param payload: Request body - Process remove software image operation
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/action/image-remove", payload=payload, **kw
        )
