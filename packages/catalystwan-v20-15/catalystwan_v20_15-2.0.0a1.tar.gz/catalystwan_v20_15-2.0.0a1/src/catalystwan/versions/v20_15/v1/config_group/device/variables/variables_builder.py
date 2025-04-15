# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateConfigGroupDeviceVariablesPutRequest,
    FetchConfigGroupDeviceVariablesPostRequest,
    GetConfigGroupDeviceVariablesGetResponse,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class VariablesBuilder:
    """
    Builds and executes requests for operations under /v1/config-group/{configGroupId}/device/variables
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        config_group_id: str,
        device_id: Optional[str] = None,
        suggestions: Optional[bool] = None,
        **kw,
    ) -> GetConfigGroupDeviceVariablesGetResponse:
        """
        Get device variables
        GET /dataservice/v1/config-group/{configGroupId}/device/variables

        :param config_group_id: Config Group Id
        :param device_id: Comma separated device id's like d1,d2
        :param suggestions: Suggestions for possible values
        :returns: GetConfigGroupDeviceVariablesGetResponse
        """
        params = {
            "configGroupId": config_group_id,
            "device-id": device_id,
            "suggestions": suggestions,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/config-group/{configGroupId}/device/variables",
            return_type=GetConfigGroupDeviceVariablesGetResponse,
            params=params,
            **kw,
        )

    def put(
        self, config_group_id: str, payload: CreateConfigGroupDeviceVariablesPutRequest, **kw
    ) -> Any:
        """
        assign values to device variables
        PUT /dataservice/v1/config-group/{configGroupId}/device/variables

        :param config_group_id: Config Group Id
        :param payload: Payload
        :returns: Any
        """
        params = {
            "configGroupId": config_group_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/config-group/{configGroupId}/device/variables",
            params=params,
            payload=payload,
            **kw,
        )

    def post(
        self, config_group_id: str, payload: FetchConfigGroupDeviceVariablesPostRequest, **kw
    ) -> Any:
        """
        Fetch device variables
        POST /dataservice/v1/config-group/{configGroupId}/device/variables

        :param config_group_id: Config Group Id
        :param payload: Payload
        :returns: Any
        """
        params = {
            "configGroupId": config_group_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/config-group/{configGroupId}/device/variables",
            params=params,
            payload=payload,
            **kw,
        )

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)
