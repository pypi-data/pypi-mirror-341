# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetMobilityCliFeatureProfileGetResponse, GetSingleMobilityCliPayload

if TYPE_CHECKING:
    from .config.config_builder import ConfigBuilder


class CliBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility/cli
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, *, cli_id: str, **kw) -> GetSingleMobilityCliPayload:
        """
        Get a Mobility Feature Profile with Cli profile type
        GET /dataservice/v1/feature-profile/mobility/cli/{cliId}

        :param cli_id: Feature Profile Id
        :returns: GetSingleMobilityCliPayload
        """
        ...

    @overload
    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = 0,
        reference_count: Optional[bool] = False,
        **kw,
    ) -> List[GetMobilityCliFeatureProfileGetResponse]:
        """
        Get Mobility Cli Feature Profiles
        GET /dataservice/v1/feature-profile/mobility/cli

        :param offset: Pagination offset
        :param limit: Pagination limit
        :param reference_count: get associated group details
        :returns: List[GetMobilityCliFeatureProfileGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        reference_count: Optional[bool] = None,
        cli_id: Optional[str] = None,
        **kw,
    ) -> Union[List[GetMobilityCliFeatureProfileGetResponse], GetSingleMobilityCliPayload]:
        # /dataservice/v1/feature-profile/mobility/cli/{cliId}
        if self._request_adapter.param_checker([(cli_id, str)], [offset, limit, reference_count]):
            params = {
                "cliId": cli_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/cli/{cliId}",
                return_type=GetSingleMobilityCliPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/mobility/cli
        if self._request_adapter.param_checker([], [cli_id]):
            params = {
                "offset": offset,
                "limit": limit,
                "referenceCount": reference_count,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/cli",
                return_type=List[GetMobilityCliFeatureProfileGetResponse],
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
