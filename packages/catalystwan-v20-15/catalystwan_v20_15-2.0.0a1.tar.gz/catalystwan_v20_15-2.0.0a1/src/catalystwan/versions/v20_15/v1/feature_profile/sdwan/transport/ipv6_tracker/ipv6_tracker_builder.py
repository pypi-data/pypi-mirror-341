# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateIpv6TrackerProfileParcelForTransportPostRequest,
    CreateIpv6TrackerProfileParcelForTransportPostResponse,
    EditIpv6TrackerProfileParcelForTransportPutRequest,
    EditIpv6TrackerProfileParcelForTransportPutResponse,
    GetListSdwanTransportIpv6TrackerPayload,
    GetSingleSdwanTransportIpv6TrackerPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class Ipv6TrackerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/ipv6-tracker
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateIpv6TrackerProfileParcelForTransportPostRequest,
        **kw,
    ) -> CreateIpv6TrackerProfileParcelForTransportPostResponse:
        """
        Create a IPv6 Tracker Profile Parcel for Transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-tracker

        :param transport_id: Feature Profile ID
        :param payload: IPv6 Tracker Profile Parcel
        :returns: CreateIpv6TrackerProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-tracker",
            return_type=CreateIpv6TrackerProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        ipv6_tracker_id: str,
        payload: EditIpv6TrackerProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditIpv6TrackerProfileParcelForTransportPutResponse:
        """
        Update a IPv6 Tracker Profile Parcel for Transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-tracker/{ipv6-trackerId}

        :param transport_id: Feature Profile ID
        :param ipv6_tracker_id: Profile Parcel ID
        :param payload: IPv6 Tracker Profile Parcel
        :returns: EditIpv6TrackerProfileParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "ipv6-trackerId": ipv6_tracker_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-tracker/{ipv6-trackerId}",
            return_type=EditIpv6TrackerProfileParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, ipv6_tracker_id: str, **kw):
        """
        Delete a IPv6 Tracker Profile Parcel for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-tracker/{ipv6-trackerId}

        :param transport_id: Feature Profile ID
        :param ipv6_tracker_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "ipv6-trackerId": ipv6_tracker_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-tracker/{ipv6-trackerId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, ipv6_tracker_id: str, **kw
    ) -> GetSingleSdwanTransportIpv6TrackerPayload:
        """
        Get IPv6 Tracker Profile Parcel by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-tracker/{ipv6-trackerId}

        :param transport_id: Feature Profile ID
        :param ipv6_tracker_id: Profile Parcel ID
        :returns: GetSingleSdwanTransportIpv6TrackerPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportIpv6TrackerPayload:
        """
        Get IPv6 Tracker Profile Parcels for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-tracker

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportIpv6TrackerPayload
        """
        ...

    def get(
        self, transport_id: str, ipv6_tracker_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanTransportIpv6TrackerPayload, GetSingleSdwanTransportIpv6TrackerPayload]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-tracker/{ipv6-trackerId}
        if self._request_adapter.param_checker([(transport_id, str), (ipv6_tracker_id, str)], []):
            params = {
                "transportId": transport_id,
                "ipv6-trackerId": ipv6_tracker_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-tracker/{ipv6-trackerId}",
                return_type=GetSingleSdwanTransportIpv6TrackerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-tracker
        if self._request_adapter.param_checker([(transport_id, str)], [ipv6_tracker_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-tracker",
                return_type=GetListSdwanTransportIpv6TrackerPayload,
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
