# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import MessagingResp


class VmanageBuilder:
    """
    Builds and executes requests for operations under /messaging/device/vmanage
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[MessagingResp]:
        """
        Create device vManage connection list
        GET /dataservice/messaging/device/vmanage

        :returns: List[MessagingResp]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/messaging/device/vmanage", return_type=List[MessagingResp], **kw
        )
