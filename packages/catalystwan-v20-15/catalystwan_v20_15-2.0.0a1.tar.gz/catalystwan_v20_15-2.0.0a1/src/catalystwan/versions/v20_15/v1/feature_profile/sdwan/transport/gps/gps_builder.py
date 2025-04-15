# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateGpsProfileParcelForTransportPostRequest,
    CreateGpsProfileParcelForTransportPostResponse,
    EditGpsProfileParcelForTransportPutRequest,
    EditGpsProfileParcelForTransportPutResponse,
    GetListSdwanTransportGpsPayload,
    GetSingleSdwanTransportGpsPayload,
)


class GpsBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/gps
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, transport_id: str, payload: CreateGpsProfileParcelForTransportPostRequest, **kw
    ) -> CreateGpsProfileParcelForTransportPostResponse:
        """
        Create a Gps Profile Parcel for Transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/gps

        :param transport_id: Feature Profile ID
        :param payload: Gps Profile Parcel
        :returns: CreateGpsProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/gps",
            return_type=CreateGpsProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        gps_id: str,
        payload: EditGpsProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditGpsProfileParcelForTransportPutResponse:
        """
        Update a Gps Profile Parcel for Transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/gps/{gpsId}

        :param transport_id: Feature Profile ID
        :param gps_id: Profile Parcel ID
        :param payload: Gps Profile Parcel
        :returns: EditGpsProfileParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "gpsId": gps_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/gps/{gpsId}",
            return_type=EditGpsProfileParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, gps_id: str, **kw):
        """
        Delete a Gps Profile Parcel for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/gps/{gpsId}

        :param transport_id: Feature Profile ID
        :param gps_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "gpsId": gps_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/gps/{gpsId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, transport_id: str, gps_id: str, **kw) -> GetSingleSdwanTransportGpsPayload:
        """
        Get Gps Profile Parcel by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/gps/{gpsId}

        :param transport_id: Feature Profile ID
        :param gps_id: Profile Parcel ID
        :returns: GetSingleSdwanTransportGpsPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportGpsPayload:
        """
        Get Gps Profile Parcels for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/gps

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportGpsPayload
        """
        ...

    def get(
        self, transport_id: str, gps_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanTransportGpsPayload, GetSingleSdwanTransportGpsPayload]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/gps/{gpsId}
        if self._request_adapter.param_checker([(transport_id, str), (gps_id, str)], []):
            params = {
                "transportId": transport_id,
                "gpsId": gps_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/gps/{gpsId}",
                return_type=GetSingleSdwanTransportGpsPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/gps
        if self._request_adapter.param_checker([(transport_id, str)], [gps_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/gps",
                return_type=GetListSdwanTransportGpsPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
