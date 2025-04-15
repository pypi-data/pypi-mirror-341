# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ProcessGetFirmwareRemoteImageReq


class DevicesBuilder:
    """
    Builds and executes requests for operations under /device/action/firmware-upgrade/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> ProcessGetFirmwareRemoteImageReq:
        """
        firmware supported devices
        GET /dataservice/device/action/firmware-upgrade/devices

        :returns: ProcessGetFirmwareRemoteImageReq
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/action/firmware-upgrade/devices",
            return_type=ProcessGetFirmwareRemoteImageReq,
            **kw,
        )
