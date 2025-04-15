# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateAppqoeProfileParcelForServicePostRequest,
    CreateAppqoeProfileParcelForServicePostResponse,
    EditAppqoeProfileParcelForServicePutRequest,
    EditAppqoeProfileParcelForServicePutResponse,
    GetListSdwanServiceAppqoePayload,
    GetSingleSdwanServiceAppqoePayload,
)


class AppqoeBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/appqoe
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateAppqoeProfileParcelForServicePostRequest, **kw
    ) -> CreateAppqoeProfileParcelForServicePostResponse:
        """
        Create a Appqoe Profile Parcel for Service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/appqoe

        :param service_id: Feature Profile ID
        :param payload: Appqoe Profile Parcel
        :returns: CreateAppqoeProfileParcelForServicePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/appqoe",
            return_type=CreateAppqoeProfileParcelForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        appqoe_id: str,
        payload: EditAppqoeProfileParcelForServicePutRequest,
        **kw,
    ) -> EditAppqoeProfileParcelForServicePutResponse:
        """
        Update a Appqoe Profile Parcel for Service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/appqoe/{appqoeId}

        :param service_id: Feature Profile ID
        :param appqoe_id: Profile Parcel ID
        :param payload: Appqoe Profile Parcel
        :returns: EditAppqoeProfileParcelForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "appqoeId": appqoe_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/appqoe/{appqoeId}",
            return_type=EditAppqoeProfileParcelForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, appqoe_id: str, **kw):
        """
        Delete a Appqoe Profile Parcel for Service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/appqoe/{appqoeId}

        :param service_id: Feature Profile ID
        :param appqoe_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "appqoeId": appqoe_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/appqoe/{appqoeId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, service_id: str, appqoe_id: str, **kw) -> GetSingleSdwanServiceAppqoePayload:
        """
        Get Appqoe Profile Parcel by parcelId for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/appqoe/{appqoeId}

        :param service_id: Feature Profile ID
        :param appqoe_id: Profile Parcel ID
        :returns: GetSingleSdwanServiceAppqoePayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdwanServiceAppqoePayload:
        """
        Get Appqoe Profile Parcels for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/appqoe

        :param service_id: Feature Profile ID
        :returns: GetListSdwanServiceAppqoePayload
        """
        ...

    def get(
        self, service_id: str, appqoe_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanServiceAppqoePayload, GetSingleSdwanServiceAppqoePayload]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/appqoe/{appqoeId}
        if self._request_adapter.param_checker([(service_id, str), (appqoe_id, str)], []):
            params = {
                "serviceId": service_id,
                "appqoeId": appqoe_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/appqoe/{appqoeId}",
                return_type=GetSingleSdwanServiceAppqoePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/appqoe
        if self._request_adapter.param_checker([(service_id, str)], [appqoe_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/appqoe",
                return_type=GetListSdwanServiceAppqoePayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
