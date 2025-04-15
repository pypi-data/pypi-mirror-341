# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AdminTechReq


class CopyBuilder:
    """
    Builds and executes requests for operations under /device/tools/admintech/copy
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: AdminTechReq, **kw):
        """
        copy admin tech logs
        POST /dataservice/device/tools/admintech/copy

        :param payload: Admin tech copy request
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/tools/admintech/copy", payload=payload, **kw
        )
