# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import HandleFileGenerationStatusNotificationRequest


class FileGenerationStatusBuilder:
    """
    Builds and executes requests for operations under /device/file-based/data-collection/file-generation-status
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: HandleFileGenerationStatusNotificationRequest, **kw):
        """
        Device notify when file is ready and vManage has to download them
        POST /dataservice/device/file-based/data-collection/file-generation-status

        :param payload: File generation status notification payload
        :returns: None
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/device/file-based/data-collection/file-generation-status",
            payload=payload,
            **kw,
        )
