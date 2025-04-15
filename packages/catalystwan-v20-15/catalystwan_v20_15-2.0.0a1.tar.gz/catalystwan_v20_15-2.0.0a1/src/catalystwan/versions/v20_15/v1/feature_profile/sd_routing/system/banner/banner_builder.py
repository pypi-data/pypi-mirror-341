# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingBannerFeaturePostRequest,
    CreateSdroutingBannerFeaturePostResponse,
    EditSdroutingBannerFeaturePutRequest,
    EditSdroutingBannerFeaturePutResponse,
    GetListSdRoutingSystemBannerPayload,
    GetSingleSdRoutingSystemBannerPayload,
)


class BannerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/system/{systemId}/banner
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateSdroutingBannerFeaturePostRequest, **kw
    ) -> CreateSdroutingBannerFeaturePostResponse:
        """
        Create a SD-Routing Banner Feature for System Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/system/{systemId}/banner

        :param system_id: System Profile ID
        :param payload: SD-Routing Banner Feature for System Feature Profile
        :returns: CreateSdroutingBannerFeaturePostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/banner",
            return_type=CreateSdroutingBannerFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, banner_id: str, payload: EditSdroutingBannerFeaturePutRequest, **kw
    ) -> EditSdroutingBannerFeaturePutResponse:
        """
        Edit a SD-Routing Banner Feature for System Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/system/{systemId}/banner/{bannerId}

        :param system_id: System Profile ID
        :param banner_id: Banner Feature ID
        :param payload: SD-Routing Banner Feature for System Feature Profile
        :returns: EditSdroutingBannerFeaturePutResponse
        """
        params = {
            "systemId": system_id,
            "bannerId": banner_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/banner/{bannerId}",
            return_type=EditSdroutingBannerFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, banner_id: str, **kw):
        """
        Delete a SD-Routing Banner Feature for System Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/system/{systemId}/banner/{bannerId}

        :param system_id: System Profile ID
        :param banner_id: Banner Feature ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "bannerId": banner_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/banner/{bannerId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, banner_id: str, **kw) -> GetSingleSdRoutingSystemBannerPayload:
        """
        Get a SD-Routing Banner Feature for System Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/banner/{bannerId}

        :param system_id: System Profile ID
        :param banner_id: Banner Feature ID
        :returns: GetSingleSdRoutingSystemBannerPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdRoutingSystemBannerPayload:
        """
        Get all SD-Routing Banner Features for System Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/banner

        :param system_id: System Profile ID
        :returns: GetListSdRoutingSystemBannerPayload
        """
        ...

    def get(
        self, system_id: str, banner_id: Optional[str] = None, **kw
    ) -> Union[GetListSdRoutingSystemBannerPayload, GetSingleSdRoutingSystemBannerPayload]:
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/banner/{bannerId}
        if self._request_adapter.param_checker([(system_id, str), (banner_id, str)], []):
            params = {
                "systemId": system_id,
                "bannerId": banner_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/banner/{bannerId}",
                return_type=GetSingleSdRoutingSystemBannerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/banner
        if self._request_adapter.param_checker([(system_id, str)], [banner_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/banner",
                return_type=GetListSdRoutingSystemBannerPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
