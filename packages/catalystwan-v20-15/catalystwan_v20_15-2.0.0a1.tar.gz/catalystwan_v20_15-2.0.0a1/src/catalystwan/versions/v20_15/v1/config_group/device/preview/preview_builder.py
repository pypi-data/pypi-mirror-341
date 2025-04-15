# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    GetConfigGroupDeviceConfigurationPreviewPostRequest,
    GetConfigGroupDeviceConfigurationPreviewPostResponse,
)


class PreviewBuilder:
    """
    Builds and executes requests for operations under /v1/config-group/{configGroupId}/device/{deviceId}/preview
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        config_group_id: str,
        device_id: str,
        payload: GetConfigGroupDeviceConfigurationPreviewPostRequest,
        **kw,
    ) -> GetConfigGroupDeviceConfigurationPreviewPostResponse:
        """
        Get a preview of the configuration for a device
        POST /dataservice/v1/config-group/{configGroupId}/device/{deviceId}/preview

        :param config_group_id: Config Group Id
        :param device_id: Device Id
        :param payload: Payload
        :returns: GetConfigGroupDeviceConfigurationPreviewPostResponse
        """
        params = {
            "configGroupId": config_group_id,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/config-group/{configGroupId}/device/{deviceId}/preview",
            return_type=GetConfigGroupDeviceConfigurationPreviewPostResponse,
            params=params,
            payload=payload,
            **kw,
        )
