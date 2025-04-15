# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportRoutingOspfv3Ipv4FeaturePostRequest,
    CreateSdroutingTransportRoutingOspfv3Ipv4FeaturePostResponse,
    EditSdroutingTransportRoutingOspfv3Ipv4FeaturePutRequest,
    EditSdroutingTransportRoutingOspfv3Ipv4FeaturePutResponse,
    GetListSdRoutingTransportRoutingOspfv3Ipv4Payload,
    GetSingleSdRoutingTransportRoutingOspfv3Ipv4Payload,
)


class Ipv4Builder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv4
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateSdroutingTransportRoutingOspfv3Ipv4FeaturePostRequest,
        **kw,
    ) -> CreateSdroutingTransportRoutingOspfv3Ipv4FeaturePostResponse:
        """
        Create a SD-Routing WAN OSPFv3 IPv4 Feature in Transport Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv4

        :param transport_id: Transport Profile ID
        :param payload: SD-Routing WAN OSPFv3 IPv4 Feature in Transport Feature Profile
        :returns: CreateSdroutingTransportRoutingOspfv3Ipv4FeaturePostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv4",
            return_type=CreateSdroutingTransportRoutingOspfv3Ipv4FeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        ospfv3_id: str,
        payload: EditSdroutingTransportRoutingOspfv3Ipv4FeaturePutRequest,
        **kw,
    ) -> EditSdroutingTransportRoutingOspfv3Ipv4FeaturePutResponse:
        """
        Edit a SD-Routing WAN OSPFv3 IPv4 Feature in Transport Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param transport_id: Transport Profile ID
        :param ospfv3_id: IPv4 OSPFv3 Feature ID
        :param payload: SD-Routing WAN OSPFv3 IPv4 Feature in Transport Feature Profile
        :returns: EditSdroutingTransportRoutingOspfv3Ipv4FeaturePutResponse
        """
        params = {
            "transportId": transport_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv4/{ospfv3Id}",
            return_type=EditSdroutingTransportRoutingOspfv3Ipv4FeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, ospfv3_id: str, **kw):
        """
        Delete a SD-Routing WAN OSPFv3 IPv4 Feature in Transport Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param transport_id: Transport Profile ID
        :param ospfv3_id: IPv4 OSPFv3 Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv4/{ospfv3Id}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, ospfv3_id: str, **kw
    ) -> GetSingleSdRoutingTransportRoutingOspfv3Ipv4Payload:
        """
        Get a SD-Routing WAN OSPFv3 IPv4 Feature in Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param transport_id: Transport Profile ID
        :param ospfv3_id: IPv4 OSPFv3 Feature ID
        :returns: GetSingleSdRoutingTransportRoutingOspfv3Ipv4Payload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdRoutingTransportRoutingOspfv3Ipv4Payload:
        """
        Get all SD-Routing WAN OSPFv3 IPv4 Features in Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv4

        :param transport_id: Transport Profile ID
        :returns: GetListSdRoutingTransportRoutingOspfv3Ipv4Payload
        """
        ...

    def get(
        self, transport_id: str, ospfv3_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportRoutingOspfv3Ipv4Payload,
        GetSingleSdRoutingTransportRoutingOspfv3Ipv4Payload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv4/{ospfv3Id}
        if self._request_adapter.param_checker([(transport_id, str), (ospfv3_id, str)], []):
            params = {
                "transportId": transport_id,
                "ospfv3Id": ospfv3_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv4/{ospfv3Id}",
                return_type=GetSingleSdRoutingTransportRoutingOspfv3Ipv4Payload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv4
        if self._request_adapter.param_checker([(transport_id, str)], [ospfv3_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv4",
                return_type=GetListSdRoutingTransportRoutingOspfv3Ipv4Payload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
