# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingCliConfigGroupFeaturePostRequest,
    CreateSdroutingCliConfigGroupFeaturePostResponse,
    EditSdroutingCliConfigGroupFeaturePutRequest,
    EditSdroutingCliConfigGroupFeaturePutResponse,
    GetListSdRoutingCliFullConfigPayload,
    GetSingleSdRoutingCliFullConfigPayload,
)


class FullConfigBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/cli/{cliId}/full-config
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, cli_id: str, payload: CreateSdroutingCliConfigGroupFeaturePostRequest, **kw
    ) -> CreateSdroutingCliConfigGroupFeaturePostResponse:
        """
        Create a SD-Routing CLI Configuration Group
        POST /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/full-config

        :param cli_id: Cli Profile ID
        :param payload: SD-Routing CLI Configuration Group
        :returns: CreateSdroutingCliConfigGroupFeaturePostResponse
        """
        params = {
            "cliId": cli_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/full-config",
            return_type=CreateSdroutingCliConfigGroupFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        cli_id: str,
        full_config_id: str,
        payload: EditSdroutingCliConfigGroupFeaturePutRequest,
        **kw,
    ) -> EditSdroutingCliConfigGroupFeaturePutResponse:
        """
        Edit a SD-Routing CLI Configuration Group
        PUT /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/full-config/{fullConfigId}

        :param cli_id: Cli Profile ID
        :param full_config_id: Full Config Feature ID
        :param payload: SD-Routing CLI Configuration Group
        :returns: EditSdroutingCliConfigGroupFeaturePutResponse
        """
        params = {
            "cliId": cli_id,
            "fullConfigId": full_config_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/full-config/{fullConfigId}",
            return_type=EditSdroutingCliConfigGroupFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, cli_id: str, full_config_id: str, **kw):
        """
        Delete a SD-Routing CLI Configuration Group
        DELETE /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/full-config/{fullConfigId}

        :param cli_id: Cli Profile ID
        :param full_config_id: Full Config Feature ID
        :returns: None
        """
        params = {
            "cliId": cli_id,
            "fullConfigId": full_config_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/full-config/{fullConfigId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, cli_id: str, full_config_id: str, **kw) -> GetSingleSdRoutingCliFullConfigPayload:
        """
        Get the CLI Configuration by CLI profile ID and Config Feature ID
        GET /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/full-config/{fullConfigId}

        :param cli_id: Cli Profile ID
        :param full_config_id: Full Config Feature ID
        :returns: GetSingleSdRoutingCliFullConfigPayload
        """
        ...

    @overload
    def get(self, cli_id: str, **kw) -> GetListSdRoutingCliFullConfigPayload:
        """
        Get the CLI Configuration by CLI profile ID
        GET /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/full-config

        :param cli_id: Cli Profile ID
        :returns: GetListSdRoutingCliFullConfigPayload
        """
        ...

    def get(
        self, cli_id: str, full_config_id: Optional[str] = None, **kw
    ) -> Union[GetListSdRoutingCliFullConfigPayload, GetSingleSdRoutingCliFullConfigPayload]:
        # /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/full-config/{fullConfigId}
        if self._request_adapter.param_checker([(cli_id, str), (full_config_id, str)], []):
            params = {
                "cliId": cli_id,
                "fullConfigId": full_config_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/full-config/{fullConfigId}",
                return_type=GetSingleSdRoutingCliFullConfigPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/cli/{cliId}/full-config
        if self._request_adapter.param_checker([(cli_id, str)], [full_config_id]):
            params = {
                "cliId": cli_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}/full-config",
                return_type=GetListSdRoutingCliFullConfigPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
