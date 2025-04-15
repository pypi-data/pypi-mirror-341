# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeployConfigGroupPostRequest, DeployConfigGroupPostResponse


class DeployBuilder:
    """
    Builds and executes requests for operations under /v1/config-group/{configGroupId}/device/deploy
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, config_group_id: str, payload: DeployConfigGroupPostRequest, **kw
    ) -> DeployConfigGroupPostResponse:
        """
        deploy config group to devices


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/v1/config-group/{configGroupId}/device/deploy

        :param config_group_id: Config Group Id
        :param payload: Payload
        :returns: DeployConfigGroupPostResponse
        """
        params = {
            "configGroupId": config_group_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/config-group/{configGroupId}/device/deploy",
            return_type=DeployConfigGroupPostResponse,
            params=params,
            payload=payload,
            **kw,
        )
