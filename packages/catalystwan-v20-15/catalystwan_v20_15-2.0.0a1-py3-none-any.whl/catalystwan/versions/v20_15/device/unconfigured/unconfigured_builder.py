# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Device


class UnconfiguredBuilder:
    """
    Builds and executes requests for operations under /device/unconfigured
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Device]:
        """
        Get wan edge devices not configured by vManage (that is, those in CLI mode)
        GET /dataservice/device/unconfigured

        :returns: List[Device]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/device/unconfigured", return_type=List[Device], **kw
        )
