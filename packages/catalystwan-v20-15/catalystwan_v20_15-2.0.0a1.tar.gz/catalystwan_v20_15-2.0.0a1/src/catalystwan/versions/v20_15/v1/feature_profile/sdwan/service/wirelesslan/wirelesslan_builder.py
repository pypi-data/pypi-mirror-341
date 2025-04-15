# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWirelesslanProfileParcelForServicePostRequest,
    CreateWirelesslanProfileParcelForServicePostResponse,
    EditWirelesslanProfileParcelForServicePutRequest,
    EditWirelesslanProfileParcelForServicePutResponse,
    GetListSdwanServiceWirelesslanPayload,
    GetSingleSdwanServiceWirelesslanPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class WirelesslanBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/wirelesslan
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateWirelesslanProfileParcelForServicePostRequest, **kw
    ) -> CreateWirelesslanProfileParcelForServicePostResponse:
        """
        Create a Wirelesslan Profile Parcel for Service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/wirelesslan

        :param service_id: Feature Profile ID
        :param payload: Wirelesslan Profile Parcel
        :returns: CreateWirelesslanProfileParcelForServicePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/wirelesslan",
            return_type=CreateWirelesslanProfileParcelForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        wirelesslan_id: str,
        payload: EditWirelesslanProfileParcelForServicePutRequest,
        **kw,
    ) -> EditWirelesslanProfileParcelForServicePutResponse:
        """
        Update a Wirelesslan Profile Parcel for Service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/wirelesslan/{wirelesslanId}

        :param service_id: Feature Profile ID
        :param wirelesslan_id: Profile Parcel ID
        :param payload: Wirelesslan Profile Parcel
        :returns: EditWirelesslanProfileParcelForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "wirelesslanId": wirelesslan_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/wirelesslan/{wirelesslanId}",
            return_type=EditWirelesslanProfileParcelForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, wirelesslan_id: str, **kw):
        """
        Delete a Wirelesslan Profile Parcel for Service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/wirelesslan/{wirelesslanId}

        :param service_id: Feature Profile ID
        :param wirelesslan_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "wirelesslanId": wirelesslan_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/wirelesslan/{wirelesslanId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, wirelesslan_id: str, **kw
    ) -> GetSingleSdwanServiceWirelesslanPayload:
        """
        Get Wirelesslan Profile Parcel by parcelId for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/wirelesslan/{wirelesslanId}

        :param service_id: Feature Profile ID
        :param wirelesslan_id: Profile Parcel ID
        :returns: GetSingleSdwanServiceWirelesslanPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdwanServiceWirelesslanPayload:
        """
        Get Wirelesslan Profile Parcels for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/wirelesslan

        :param service_id: Feature Profile ID
        :returns: GetListSdwanServiceWirelesslanPayload
        """
        ...

    def get(
        self, service_id: str, wirelesslan_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanServiceWirelesslanPayload, GetSingleSdwanServiceWirelesslanPayload]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/wirelesslan/{wirelesslanId}
        if self._request_adapter.param_checker([(service_id, str), (wirelesslan_id, str)], []):
            params = {
                "serviceId": service_id,
                "wirelesslanId": wirelesslan_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/wirelesslan/{wirelesslanId}",
                return_type=GetSingleSdwanServiceWirelesslanPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/wirelesslan
        if self._request_adapter.param_checker([(service_id, str)], [wirelesslan_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/wirelesslan",
                return_type=GetListSdwanServiceWirelesslanPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)
