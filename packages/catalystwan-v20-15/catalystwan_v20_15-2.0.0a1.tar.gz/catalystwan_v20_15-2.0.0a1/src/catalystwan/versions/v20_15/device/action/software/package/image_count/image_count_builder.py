# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface


class ImageCountBuilder:
    """
    Builds and executes requests for operations under /device/action/software/package/imageCount
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, image_type: Optional[List[str]] = None, **kw):
        """
        Number of software image presented in vManage repository
        GET /dataservice/device/action/software/package/imageCount

        :param image_type: imageType
        :returns: None
        """
        params = {
            "imageType": image_type,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/action/software/package/imageCount", params=params, **kw
        )
