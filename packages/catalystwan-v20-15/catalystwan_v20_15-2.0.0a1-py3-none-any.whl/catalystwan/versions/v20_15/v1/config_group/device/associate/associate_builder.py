# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateConfigGroupAssociationPostRequest,
    DeleteConfigGroupAssociationDeleteRequest,
    GetConfigGroupAssociationGetResponse,
    UpdateConfigGroupAssociationPutRequest,
)


class AssociateBuilder:
    """
    Builds and executes requests for operations under /v1/config-group/{configGroupId}/device/associate
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, config_group_id: str, **kw) -> GetConfigGroupAssociationGetResponse:
        """
        Get devices association with a config group
        GET /dataservice/v1/config-group/{configGroupId}/device/associate

        :param config_group_id: Config group id
        :returns: GetConfigGroupAssociationGetResponse
        """
        params = {
            "configGroupId": config_group_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/config-group/{configGroupId}/device/associate",
            return_type=GetConfigGroupAssociationGetResponse,
            params=params,
            **kw,
        )

    def put(self, config_group_id: str, payload: UpdateConfigGroupAssociationPutRequest, **kw):
        """
        Move the devices from one config group to another
        PUT /dataservice/v1/config-group/{configGroupId}/device/associate

        :param config_group_id: Config group id
        :param payload: Payload
        :returns: None
        """
        params = {
            "configGroupId": config_group_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/config-group/{configGroupId}/device/associate",
            params=params,
            payload=payload,
            **kw,
        )

    def post(self, config_group_id: str, payload: CreateConfigGroupAssociationPostRequest, **kw):
        """
        Create associations with device and a config group
        POST /dataservice/v1/config-group/{configGroupId}/device/associate

        :param config_group_id: Config group id
        :param payload: Payload
        :returns: None
        """
        params = {
            "configGroupId": config_group_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/config-group/{configGroupId}/device/associate",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(
        self,
        config_group_id: str,
        payload: Optional[DeleteConfigGroupAssociationDeleteRequest] = None,
        **kw,
    ):
        """
        Delete Config Group Association from devices
        DELETE /dataservice/v1/config-group/{configGroupId}/device/associate

        :param config_group_id: Config group id
        :param payload: Payload
        :returns: None
        """
        params = {
            "configGroupId": config_group_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/config-group/{configGroupId}/device/associate",
            params=params,
            payload=payload,
            **kw,
        )
