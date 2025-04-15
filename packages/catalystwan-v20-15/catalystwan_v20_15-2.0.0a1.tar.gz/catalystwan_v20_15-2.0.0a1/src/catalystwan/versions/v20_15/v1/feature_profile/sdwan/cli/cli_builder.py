# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdwanFeatureProfilePostRequest,
    CreateSdwanFeatureProfilePostResponse,
    EditSdwanFeatureProfilePutRequest,
    EditSdwanFeatureProfilePutResponse,
    GetSdwanFeatureProfilesByFamilyAndType1GetResponse,
    GetSingleSdwanCliPayload,
)

if TYPE_CHECKING:
    from .config.config_builder import ConfigBuilder
    from .features.features_builder import FeaturesBuilder


class CliBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/cli
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateSdwanFeatureProfilePostRequest, **kw
    ) -> CreateSdwanFeatureProfilePostResponse:
        """
        Create a SDWAN  Feature Profile with profile type
        POST /dataservice/v1/feature-profile/sdwan/cli

        :param payload: SDWAN Feature profile
        :returns: CreateSdwanFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/cli",
            return_type=CreateSdwanFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, cli_id: str, payload: EditSdwanFeatureProfilePutRequest, **kw
    ) -> EditSdwanFeatureProfilePutResponse:
        """
        Edit a SDWAN Feature Profile
        PUT /dataservice/v1/feature-profile/sdwan/cli/{cliId}

        :param cli_id: Feature Profile Id
        :param payload: SDWAN Feature profile
        :returns: EditSdwanFeatureProfilePutResponse
        """
        params = {
            "cliId": cli_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/cli/{cliId}",
            return_type=EditSdwanFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, cli_id: str, **kw):
        """
        Delete Feature Profile
        DELETE /dataservice/v1/feature-profile/sdwan/cli/{cliId}

        :param cli_id: Cli id
        :returns: None
        """
        params = {
            "cliId": cli_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/v1/feature-profile/sdwan/cli/{cliId}", params=params, **kw
        )

    @overload
    def get(self, *, cli_id: str, **kw) -> GetSingleSdwanCliPayload:
        """
        Get a SDWAN Feature Profile with Cli profile type
        GET /dataservice/v1/feature-profile/sdwan/cli/{cliId}

        :param cli_id: Feature Profile Id
        :returns: GetSingleSdwanCliPayload
        """
        ...

    @overload
    def get(
        self, *, offset: Optional[int] = None, limit: Optional[int] = 0, **kw
    ) -> List[GetSdwanFeatureProfilesByFamilyAndType1GetResponse]:
        """
        Get all SDWAN Feature Profiles with giving Family and profile type
        GET /dataservice/v1/feature-profile/sdwan/cli

        :param offset: Pagination offset
        :param limit: Pagination limit
        :returns: List[GetSdwanFeatureProfilesByFamilyAndType1GetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        cli_id: Optional[str] = None,
        **kw,
    ) -> Union[List[GetSdwanFeatureProfilesByFamilyAndType1GetResponse], GetSingleSdwanCliPayload]:
        # /dataservice/v1/feature-profile/sdwan/cli/{cliId}
        if self._request_adapter.param_checker([(cli_id, str)], [offset, limit]):
            params = {
                "cliId": cli_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/cli/{cliId}",
                return_type=GetSingleSdwanCliPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/cli
        if self._request_adapter.param_checker([], [cli_id]):
            params = {
                "offset": offset,
                "limit": limit,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/cli",
                return_type=List[GetSdwanFeatureProfilesByFamilyAndType1GetResponse],
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
