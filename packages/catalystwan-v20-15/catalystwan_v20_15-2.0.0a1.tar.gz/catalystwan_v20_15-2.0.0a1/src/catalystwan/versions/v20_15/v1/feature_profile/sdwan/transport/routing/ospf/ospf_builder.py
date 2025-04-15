# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateRoutingOspfProfileParcelForTransportPostRequest,
    CreateRoutingOspfProfileParcelForTransportPostResponse,
    EditRoutingOspfProfileParcelForTransportPutRequest,
    EditRoutingOspfProfileParcelForTransportPutResponse,
    GetListSdwanTransportRoutingOspfPayload,
    GetSingleSdwanTransportRoutingOspfPayload,
)


class OspfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/routing/ospf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateRoutingOspfProfileParcelForTransportPostRequest,
        **kw,
    ) -> CreateRoutingOspfProfileParcelForTransportPostResponse:
        """
        Create a Routing Ospf Profile Parcel for Transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospf

        :param transport_id: Feature Profile ID
        :param payload: Routing Ospf Profile Parcel
        :returns: CreateRoutingOspfProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospf",
            return_type=CreateRoutingOspfProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        ospf_id: str,
        payload: EditRoutingOspfProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditRoutingOspfProfileParcelForTransportPutResponse:
        """
        Update a Routing Ospf Profile Parcel for Transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospf/{ospfId}

        :param transport_id: Feature Profile ID
        :param ospf_id: Profile Parcel ID
        :param payload: Routing Ospf Profile Parcel
        :returns: EditRoutingOspfProfileParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospf/{ospfId}",
            return_type=EditRoutingOspfProfileParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, ospf_id: str, **kw):
        """
        Delete a Routing Ospf Profile Parcel for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospf/{ospfId}

        :param transport_id: Feature Profile ID
        :param ospf_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospf/{ospfId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, ospf_id: str, **kw
    ) -> GetSingleSdwanTransportRoutingOspfPayload:
        """
        Get Routing Ospf Profile Parcel by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospf/{ospfId}

        :param transport_id: Feature Profile ID
        :param ospf_id: Profile Parcel ID
        :returns: GetSingleSdwanTransportRoutingOspfPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportRoutingOspfPayload:
        """
        Get Routing Ospf Profile Parcels for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospf

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportRoutingOspfPayload
        """
        ...

    def get(
        self, transport_id: str, ospf_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanTransportRoutingOspfPayload, GetSingleSdwanTransportRoutingOspfPayload]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospf/{ospfId}
        if self._request_adapter.param_checker([(transport_id, str), (ospf_id, str)], []):
            params = {
                "transportId": transport_id,
                "ospfId": ospf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospf/{ospfId}",
                return_type=GetSingleSdwanTransportRoutingOspfPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospf
        if self._request_adapter.param_checker([(transport_id, str)], [ospf_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospf",
                return_type=GetListSdwanTransportRoutingOspfPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
