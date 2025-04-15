# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateConfigFeatureForMobilityPostRequest,
    CreateConfigFeatureForMobilityPostResponse,
    EditConfigFeatureForMobilityPutRequest,
    EditConfigFeatureForMobilityPutResponse,
    GetListMobilityCliConfigPayload,
    GetSingleMobilityCliConfigPayload,
)


class ConfigBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility/cli/{cliId}/config
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, cli_id: str, payload: CreateConfigFeatureForMobilityPostRequest, **kw
    ) -> CreateConfigFeatureForMobilityPostResponse:
        """
        Create a config Feature for cli feature profile
        POST /dataservice/v1/feature-profile/mobility/cli/{cliId}/config

        :param cli_id: Feature Profile ID
        :param payload: cli config Feature
        :returns: CreateConfigFeatureForMobilityPostResponse
        """
        params = {
            "cliId": cli_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/mobility/cli/{cliId}/config",
            return_type=CreateConfigFeatureForMobilityPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, cli_id: str, config_id: str, payload: EditConfigFeatureForMobilityPutRequest, **kw
    ) -> EditConfigFeatureForMobilityPutResponse:
        """
        Update a config Feature for cli feature profile
        PUT /dataservice/v1/feature-profile/mobility/cli/{cliId}/config/{configId}

        :param cli_id: Feature Profile ID
        :param config_id: Feature ID
        :param payload: cli config Feature
        :returns: EditConfigFeatureForMobilityPutResponse
        """
        params = {
            "cliId": cli_id,
            "configId": config_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/mobility/cli/{cliId}/config/{configId}",
            return_type=EditConfigFeatureForMobilityPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, cli_id: str, config_id: str, **kw):
        """
        Delete a config Feature for cli feature profile
        DELETE /dataservice/v1/feature-profile/mobility/cli/{cliId}/config/{configId}

        :param cli_id: Feature Profile ID
        :param config_id: Feature ID
        :returns: None
        """
        params = {
            "cliId": cli_id,
            "configId": config_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/mobility/cli/{cliId}/config/{configId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, cli_id: str, config_id: str, **kw) -> GetSingleMobilityCliConfigPayload:
        """
        Get config Feature by configId for cli feature profile
        GET /dataservice/v1/feature-profile/mobility/cli/{cliId}/config/{configId}

        :param cli_id: Feature Profile ID
        :param config_id: Feature ID
        :returns: GetSingleMobilityCliConfigPayload
        """
        ...

    @overload
    def get(self, cli_id: str, **kw) -> GetListMobilityCliConfigPayload:
        """
        Get config Features for cli feature profile
        GET /dataservice/v1/feature-profile/mobility/cli/{cliId}/config

        :param cli_id: Feature Profile ID
        :returns: GetListMobilityCliConfigPayload
        """
        ...

    def get(
        self, cli_id: str, config_id: Optional[str] = None, **kw
    ) -> Union[GetListMobilityCliConfigPayload, GetSingleMobilityCliConfigPayload]:
        # /dataservice/v1/feature-profile/mobility/cli/{cliId}/config/{configId}
        if self._request_adapter.param_checker([(cli_id, str), (config_id, str)], []):
            params = {
                "cliId": cli_id,
                "configId": config_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/cli/{cliId}/config/{configId}",
                return_type=GetSingleMobilityCliConfigPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/mobility/cli/{cliId}/config
        if self._request_adapter.param_checker([(cli_id, str)], [config_id]):
            params = {
                "cliId": cli_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/cli/{cliId}/config",
                return_type=GetListMobilityCliConfigPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
