# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InProgressCount


class InprogressBuilder:
    """
    Builds and executes requests for operations under /device/tools/admintechs/inprogress
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> InProgressCount:
        """
        Get device admin-tech InProgressCount
        GET /dataservice/device/tools/admintechs/inprogress

        :returns: InProgressCount
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/tools/admintechs/inprogress",
            return_type=InProgressCount,
            **kw,
        )
