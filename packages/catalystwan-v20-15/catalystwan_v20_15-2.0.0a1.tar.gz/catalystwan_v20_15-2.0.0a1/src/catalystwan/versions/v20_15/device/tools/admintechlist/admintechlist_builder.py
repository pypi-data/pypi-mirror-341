# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AdminTechListReq, AdminTechListRes


class AdmintechlistBuilder:
    """
    Builds and executes requests for operations under /device/tools/admintechlist
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: AdminTechListReq, **kw) -> List[AdminTechListRes]:
        """
        List admin tech logs
        POST /dataservice/device/tools/admintechlist

        :param payload: Admin tech listing request
        :returns: List[AdminTechListRes]
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/device/tools/admintechlist",
            return_type=List[AdminTechListRes],
            payload=payload,
            **kw,
        )
