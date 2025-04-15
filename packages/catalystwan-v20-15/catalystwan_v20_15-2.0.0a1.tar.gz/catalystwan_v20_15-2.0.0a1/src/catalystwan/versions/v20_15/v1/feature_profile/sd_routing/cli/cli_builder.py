# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingCliFeatureProfilePostRequest,
    CreateSdroutingCliFeatureProfilePostResponse,
    EditSdroutingCliFeatureProfilePutRequest,
    EditSdroutingCliFeatureProfilePutResponse,
    GetSdroutingCliFeatureProfilesGetResponse,
    GetSingleSdRoutingCliPayload,
)

if TYPE_CHECKING:
    from .config.config_builder import ConfigBuilder
    from .features.features_builder import FeaturesBuilder
    from .full_config.full_config_builder import FullConfigBuilder
    from .ios_config.ios_config_builder import IosConfigBuilder


class CliBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/cli
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateSdroutingCliFeatureProfilePostRequest, **kw
    ) -> CreateSdroutingCliFeatureProfilePostResponse:
        """
        Create a SD-Routing CLI Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/cli

        :param payload: SD-Routing CLI Feature Profile
        :returns: CreateSdroutingCliFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/cli",
            return_type=CreateSdroutingCliFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, cli_id: str, payload: EditSdroutingCliFeatureProfilePutRequest, **kw
    ) -> EditSdroutingCliFeatureProfilePutResponse:
        """
        Edit a SD-Routing CLI Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/cli/{cliId}

        :param cli_id: Cli Profile Id
        :param payload: SD-Routing CLI Feature Profile
        :returns: EditSdroutingCliFeatureProfilePutResponse
        """
        params = {
            "cliId": cli_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}",
            return_type=EditSdroutingCliFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, cli_id: str, **kw):
        """
        Delete a SD-Routing CLI Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/cli/{cliId}

        :param cli_id: Cli Profile Id
        :returns: None
        """
        params = {
            "cliId": cli_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}", params=params, **kw
        )

    @overload
    def get(self, *, cli_id: str, **kw) -> GetSingleSdRoutingCliPayload:
        """
        Get a SD-Routing CLI Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/cli/{cliId}

        :param cli_id: Cli Profile Id
        :returns: GetSingleSdRoutingCliPayload
        """
        ...

    @overload
    def get(
        self, *, offset: Optional[int] = None, limit: Optional[int] = 0, **kw
    ) -> List[GetSdroutingCliFeatureProfilesGetResponse]:
        """
        Get all SD-Routing CLI Feature Profiles
        GET /dataservice/v1/feature-profile/sd-routing/cli

        :param offset: Pagination offset
        :param limit: Pagination limit
        :returns: List[GetSdroutingCliFeatureProfilesGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        cli_id: Optional[str] = None,
        **kw,
    ) -> Union[List[GetSdroutingCliFeatureProfilesGetResponse], GetSingleSdRoutingCliPayload]:
        # /dataservice/v1/feature-profile/sd-routing/cli/{cliId}
        if self._request_adapter.param_checker([(cli_id, str)], [offset, limit]):
            params = {
                "cliId": cli_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/cli/{cliId}",
                return_type=GetSingleSdRoutingCliPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/cli
        if self._request_adapter.param_checker([], [cli_id]):
            params = {
                "offset": offset,
                "limit": limit,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/cli",
                return_type=List[GetSdroutingCliFeatureProfilesGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def config(self) -> ConfigBuilder:
        """
        The config property
        """
        from .config.config_builder import ConfigBuilder

        return ConfigBuilder(self._request_adapter)

    @property
    def features(self) -> FeaturesBuilder:
        """
        The features property
        """
        from .features.features_builder import FeaturesBuilder

        return FeaturesBuilder(self._request_adapter)

    @property
    def full_config(self) -> FullConfigBuilder:
        """
        The full-config property
        """
        from .full_config.full_config_builder import FullConfigBuilder

        return FullConfigBuilder(self._request_adapter)

    @property
    def ios_config(self) -> IosConfigBuilder:
        """
        The ios-config property
        """
        from .ios_config.ios_config_builder import IosConfigBuilder

        return IosConfigBuilder(self._request_adapter)
