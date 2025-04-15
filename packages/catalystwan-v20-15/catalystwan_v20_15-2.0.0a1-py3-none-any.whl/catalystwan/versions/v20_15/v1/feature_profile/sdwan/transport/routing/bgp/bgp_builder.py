# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateRoutingBgpProfileParcelForTransportPostRequest,
    CreateRoutingBgpProfileParcelForTransportPostResponse,
    EditRoutingBgpProfileParcelForTransportPutRequest,
    EditRoutingBgpProfileParcelForTransportPutResponse,
    GetListSdwanTransportRoutingBgpPayload,
    GetSingleSdwanTransportRoutingBgpPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class BgpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/routing/bgp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, transport_id: str, payload: CreateRoutingBgpProfileParcelForTransportPostRequest, **kw
    ) -> CreateRoutingBgpProfileParcelForTransportPostResponse:
        """
        Create a Routing Bgp Profile Parcel for Transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/bgp

        :param transport_id: Feature Profile ID
        :param payload: Routing Bgp Profile Parcel
        :returns: CreateRoutingBgpProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/bgp",
            return_type=CreateRoutingBgpProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        bgp_id: str,
        payload: EditRoutingBgpProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditRoutingBgpProfileParcelForTransportPutResponse:
        """
        Update a Routing Bgp Profile Parcel for Transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/bgp/{bgpId}

        :param transport_id: Feature Profile ID
        :param bgp_id: Profile Parcel ID
        :param payload: Routing Bgp Profile Parcel
        :returns: EditRoutingBgpProfileParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "bgpId": bgp_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/bgp/{bgpId}",
            return_type=EditRoutingBgpProfileParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, bgp_id: str, **kw):
        """
        Delete a Routing Bgp Profile Parcel for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/bgp/{bgpId}

        :param transport_id: Feature Profile ID
        :param bgp_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "bgpId": bgp_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/bgp/{bgpId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, transport_id: str, bgp_id: str, **kw) -> GetSingleSdwanTransportRoutingBgpPayload:
        """
        Get Routing Bgp Profile Parcel by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/bgp/{bgpId}

        :param transport_id: Feature Profile ID
        :param bgp_id: Profile Parcel ID
        :returns: GetSingleSdwanTransportRoutingBgpPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportRoutingBgpPayload:
        """
        Get Routing Bgp Profile Parcels for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/bgp

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportRoutingBgpPayload
        """
        ...

    def get(
        self, transport_id: str, bgp_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanTransportRoutingBgpPayload, GetSingleSdwanTransportRoutingBgpPayload]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/bgp/{bgpId}
        if self._request_adapter.param_checker([(transport_id, str), (bgp_id, str)], []):
            params = {
                "transportId": transport_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/bgp/{bgpId}",
                return_type=GetSingleSdwanTransportRoutingBgpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/bgp
        if self._request_adapter.param_checker([(transport_id, str)], [bgp_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/bgp",
                return_type=GetListSdwanTransportRoutingBgpPayload,
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
