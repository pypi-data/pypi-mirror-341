# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingAaaFeaturePostRequest,
    CreateSdroutingAaaFeaturePostResponse,
    EditSdroutingAaaFeaturePutRequest,
    EditSdroutingAaaFeaturePutResponse,
    GetListSdRoutingSystemAaaSdRoutingPayload,
    GetSingleSdRoutingSystemAaaSdRoutingPayload,
)


class AaaBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/system/{systemId}/aaa
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateSdroutingAaaFeaturePostRequest, **kw
    ) -> CreateSdroutingAaaFeaturePostResponse:
        """
        Create a SD-Routing AAA Feature for System Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/system/{systemId}/aaa

        :param system_id: System Profile ID
        :param payload: SD-Routing AAA Feature for System Feature Profile
        :returns: CreateSdroutingAaaFeaturePostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/aaa",
            return_type=CreateSdroutingAaaFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, aaa_id: str, payload: EditSdroutingAaaFeaturePutRequest, **kw
    ) -> EditSdroutingAaaFeaturePutResponse:
        """
        Edit a SD-Routing AAA Feature for System Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/system/{systemId}/aaa/{aaaId}

        :param system_id: System Profile ID
        :param aaa_id: AAA Feature ID
        :param payload: SD-Routing AAA Feature for System Feature Profile
        :returns: EditSdroutingAaaFeaturePutResponse
        """
        params = {
            "systemId": system_id,
            "aaaId": aaa_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/aaa/{aaaId}",
            return_type=EditSdroutingAaaFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, aaa_id: str, **kw):
        """
        Delete a SD-Routing AAA Feature for System Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/system/{systemId}/aaa/{aaaId}

        :param system_id: System Profile ID
        :param aaa_id: AAA Feature ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "aaaId": aaa_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/aaa/{aaaId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, aaa_id: str, **kw) -> GetSingleSdRoutingSystemAaaSdRoutingPayload:
        """
        Get a SD-Routing AAA Feature for System Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/aaa/{aaaId}

        :param system_id: System Profile ID
        :param aaa_id: AAA Feature ID
        :returns: GetSingleSdRoutingSystemAaaSdRoutingPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdRoutingSystemAaaSdRoutingPayload:
        """
        Get all SD-Routing AAA Features for System Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/aaa

        :param system_id: System Profile ID
        :returns: GetListSdRoutingSystemAaaSdRoutingPayload
        """
        ...

    def get(
        self, system_id: str, aaa_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingSystemAaaSdRoutingPayload, GetSingleSdRoutingSystemAaaSdRoutingPayload
    ]:
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/aaa/{aaaId}
        if self._request_adapter.param_checker([(system_id, str), (aaa_id, str)], []):
            params = {
                "systemId": system_id,
                "aaaId": aaa_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/aaa/{aaaId}",
                return_type=GetSingleSdRoutingSystemAaaSdRoutingPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/aaa
        if self._request_adapter.param_checker([(system_id, str)], [aaa_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/aaa",
                return_type=GetListSdRoutingSystemAaaSdRoutingPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
