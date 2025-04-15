# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingLoggingFeaturePostRequest,
    CreateSdroutingLoggingFeaturePostResponse,
    EditSdroutingLoggingFeaturePutRequest,
    EditSdroutingLoggingFeaturePutResponse,
    GetListSdRoutingSystemLoggingSdRoutingPayload,
    GetSingleSdRoutingSystemLoggingSdRoutingPayload,
)


class LoggingBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/system/{systemId}/logging
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateSdroutingLoggingFeaturePostRequest, **kw
    ) -> CreateSdroutingLoggingFeaturePostResponse:
        """
        Create a SD-Routing Logging Feature for System Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/system/{systemId}/logging

        :param system_id: System Profile ID
        :param payload: SD-Routing Logging Feature for System Feature Profile
        :returns: CreateSdroutingLoggingFeaturePostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/logging",
            return_type=CreateSdroutingLoggingFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, logging_id: str, payload: EditSdroutingLoggingFeaturePutRequest, **kw
    ) -> EditSdroutingLoggingFeaturePutResponse:
        """
        Edit a SD-Routing Logging Feature for System Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/system/{systemId}/logging/{loggingId}

        :param system_id: System Profile ID
        :param logging_id: Logging Feature ID
        :param payload: SD-Routing Logging Feature for System Feature Profile
        :returns: EditSdroutingLoggingFeaturePutResponse
        """
        params = {
            "systemId": system_id,
            "loggingId": logging_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/logging/{loggingId}",
            return_type=EditSdroutingLoggingFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, logging_id: str, **kw):
        """
        Delete a SD-Routing Logging Feature for System Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/system/{systemId}/logging/{loggingId}

        :param system_id: System Profile ID
        :param logging_id: Logging Feature ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "loggingId": logging_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/logging/{loggingId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, system_id: str, logging_id: str, **kw
    ) -> GetSingleSdRoutingSystemLoggingSdRoutingPayload:
        """
        Get a SD-Routing Logging Feature for System Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/logging/{loggingId}

        :param system_id: System Profile ID
        :param logging_id: Logging Feature ID
        :returns: GetSingleSdRoutingSystemLoggingSdRoutingPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdRoutingSystemLoggingSdRoutingPayload:
        """
        Get all SD-Routing Logging Features for System Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/logging

        :param system_id: System Profile ID
        :returns: GetListSdRoutingSystemLoggingSdRoutingPayload
        """
        ...

    def get(
        self, system_id: str, logging_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingSystemLoggingSdRoutingPayload,
        GetSingleSdRoutingSystemLoggingSdRoutingPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/logging/{loggingId}
        if self._request_adapter.param_checker([(system_id, str), (logging_id, str)], []):
            params = {
                "systemId": system_id,
                "loggingId": logging_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/logging/{loggingId}",
                return_type=GetSingleSdRoutingSystemLoggingSdRoutingPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/logging
        if self._request_adapter.param_checker([(system_id, str)], [logging_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/logging",
                return_type=GetListSdRoutingSystemLoggingSdRoutingPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
