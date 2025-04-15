# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ProcessFirmwareRemoteImageReq, ProcessGetFirmwareRemoteImageReq


class RemoteBuilder:
    """
    Builds and executes requests for operations under /device/action/firmware-upgrade/remote
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> ProcessGetFirmwareRemoteImageReq:
        """
        firmware remote image package
        GET /dataservice/device/action/firmware-upgrade/remote

        :returns: ProcessGetFirmwareRemoteImageReq
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/action/firmware-upgrade/remote",
            return_type=ProcessGetFirmwareRemoteImageReq,
            **kw,
        )

    def post(self, payload: Any, **kw) -> ProcessFirmwareRemoteImageReq:
        """
        firmware remote image package
        POST /dataservice/device/action/firmware-upgrade/remote

        :param payload: Request body
        :returns: ProcessFirmwareRemoteImageReq
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/device/action/firmware-upgrade/remote",
            return_type=ProcessFirmwareRemoteImageReq,
            payload=payload,
            **kw,
        )

    def put(self, version_id: str, payload: Any, **kw) -> ProcessGetFirmwareRemoteImageReq:
        """
        Download software package file
        PUT /dataservice/device/action/firmware-upgrade/remote/{versionId}

        :param version_id: Version id
        :param payload: Request body
        :returns: ProcessGetFirmwareRemoteImageReq
        """
        params = {
            "versionId": version_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/device/action/firmware-upgrade/remote/{versionId}",
            return_type=ProcessGetFirmwareRemoteImageReq,
            params=params,
            payload=payload,
            **kw,
        )
