# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AdminTechsUploadReq


class UploadBuilder:
    """
    Builds and executes requests for operations under /device/tools/admintechs/upload
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: AdminTechsUploadReq, **kw):
        """
        upload admin tech to SR
        POST /dataservice/device/tools/admintechs/upload

        :param payload: Admin tech upload request
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/tools/admintechs/upload", payload=payload, **kw
        )
