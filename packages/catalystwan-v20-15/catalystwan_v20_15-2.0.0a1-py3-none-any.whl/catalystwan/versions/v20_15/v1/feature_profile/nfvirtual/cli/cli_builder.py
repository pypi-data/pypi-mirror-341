# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualCliFeatureProfilePostRequest,
    CreateNfvirtualCliFeatureProfilePostResponse,
    EditNfvirtualCliFeatureProfilePutRequest,
    EditNfvirtualCliFeatureProfilePutResponse,
    GetAllNfvirtualCliFeatureProfilesGetResponse,
    GetSingleNfvirtualCliPayload,
)

if TYPE_CHECKING:
    from .config.config_builder import ConfigBuilder


class CliBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/cli
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateNfvirtualCliFeatureProfilePostRequest, **kw
    ) -> CreateNfvirtualCliFeatureProfilePostResponse:
        """
        Create a Nfvirtual CLI Feature Profile
        POST /dataservice/v1/feature-profile/nfvirtual/cli

        :param payload: Nfvirtual Feature profile for CLI
        :returns: CreateNfvirtualCliFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/cli",
            return_type=CreateNfvirtualCliFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, cli_id: str, payload: EditNfvirtualCliFeatureProfilePutRequest, **kw
    ) -> EditNfvirtualCliFeatureProfilePutResponse:
        """
        Edit a Nfvirtual CLI Feature Profile
        PUT /dataservice/v1/feature-profile/nfvirtual/cli/{cliId}

        :param cli_id: Feature Profile Id
        :param payload: Nfvirtual Feature profile fo CLI
        :returns: EditNfvirtualCliFeatureProfilePutResponse
        """
        params = {
            "cliId": cli_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/cli/{cliId}",
            return_type=EditNfvirtualCliFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, cli_id: str, **kw):
        """
        Delete nfvirtual CLI Feature Profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/cli/{cliId}

        :param cli_id: Cli id
        :returns: None
        """
        params = {
            "cliId": cli_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/v1/feature-profile/nfvirtual/cli/{cliId}", params=params, **kw
        )

    @overload
    def get(self, *, cli_id: str, **kw) -> GetSingleNfvirtualCliPayload:
        """
        Get nfvirtual CLI Feature Profile with cliId
        GET /dataservice/v1/feature-profile/nfvirtual/cli/{cliId}

        :param cli_id: Feature Profile Id
        :returns: GetSingleNfvirtualCliPayload
        """
        ...

    @overload
    def get(
        self, *, offset: Optional[int] = None, limit: Optional[int] = 0, **kw
    ) -> List[GetAllNfvirtualCliFeatureProfilesGetResponse]:
        """
        Get all Nfvirtual CLI Feature Profiles
        GET /dataservice/v1/feature-profile/nfvirtual/cli

        :param offset: Pagination offset
        :param limit: Pagination limit
        :returns: List[GetAllNfvirtualCliFeatureProfilesGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        cli_id: Optional[str] = None,
        **kw,
    ) -> Union[List[GetAllNfvirtualCliFeatureProfilesGetResponse], GetSingleNfvirtualCliPayload]:
        # /dataservice/v1/feature-profile/nfvirtual/cli/{cliId}
        if self._request_adapter.param_checker([(cli_id, str)], [offset, limit]):
            params = {
                "cliId": cli_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/nfvirtual/cli/{cliId}",
                return_type=GetSingleNfvirtualCliPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/nfvirtual/cli
        if self._request_adapter.param_checker([], [cli_id]):
            params = {
                "offset": offset,
                "limit": limit,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/nfvirtual/cli",
                return_type=List[GetAllNfvirtualCliFeatureProfilesGetResponse],
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
