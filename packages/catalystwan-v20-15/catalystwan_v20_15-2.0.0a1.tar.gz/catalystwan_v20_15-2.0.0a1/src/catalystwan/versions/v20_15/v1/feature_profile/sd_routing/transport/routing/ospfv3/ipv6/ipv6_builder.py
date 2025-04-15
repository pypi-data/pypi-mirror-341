# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportRoutingOspfv3Ipv6FeaturePostRequest,
    CreateSdroutingTransportRoutingOspfv3Ipv6FeaturePostResponse,
    EditSdroutingTransportRoutingOspfv3Ipv6FeaturePutRequest,
    EditSdroutingTransportRoutingOspfv3Ipv6FeaturePutResponse,
    GetListSdRoutingTransportRoutingOspfv3Ipv6Payload,
    GetSingleSdRoutingTransportRoutingOspfv3Ipv6Payload,
)


class Ipv6Builder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv6
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateSdroutingTransportRoutingOspfv3Ipv6FeaturePostRequest,
        **kw,
    ) -> CreateSdroutingTransportRoutingOspfv3Ipv6FeaturePostResponse:
        """
        Create a SD-Routing WAN OSPFv3 IPv6 Feature for Transport Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv6

        :param transport_id: Transport Profile ID
        :param payload: SD-Routing WAN OSPFv3 IPv6 Feature for Transport Feature Profile
        :returns: CreateSdroutingTransportRoutingOspfv3Ipv6FeaturePostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv6",
            return_type=CreateSdroutingTransportRoutingOspfv3Ipv6FeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        ospfv3_id: str,
        payload: EditSdroutingTransportRoutingOspfv3Ipv6FeaturePutRequest,
        **kw,
    ) -> EditSdroutingTransportRoutingOspfv3Ipv6FeaturePutResponse:
        """
        Edit a SD-Routing WAN OSPFv3 IPv6 Feature for Transport Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param transport_id: Transport Profile ID
        :param ospfv3_id: OSPFv3 IPv6 Feature ID
        :param payload: SD-Routing WAN OSPFv3 IPv6 Feature for Transport Feature Profile
        :returns: EditSdroutingTransportRoutingOspfv3Ipv6FeaturePutResponse
        """
        params = {
            "transportId": transport_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv6/{ospfv3Id}",
            return_type=EditSdroutingTransportRoutingOspfv3Ipv6FeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, ospfv3_id: str, **kw):
        """
        Delete a SD-Routing WAN OSPFv3 IPv6 Feature for Transport Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param transport_id: Transport Profile ID
        :param ospfv3_id: OSPFv3 IPv6 Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv6/{ospfv3Id}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, ospfv3_id: str, **kw
    ) -> GetSingleSdRoutingTransportRoutingOspfv3Ipv6Payload:
        """
        Get a SD-Routing WAN OSPFv3 IPv6 Feature for Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param transport_id: Transport Profile ID
        :param ospfv3_id: OSPFv3 IPv6 Feature ID
        :returns: GetSingleSdRoutingTransportRoutingOspfv3Ipv6Payload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdRoutingTransportRoutingOspfv3Ipv6Payload:
        """
        Get all SD-Routing WAN OSPFv3 IPv6 Features for Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv6

        :param transport_id: Transport Profile ID
        :returns: GetListSdRoutingTransportRoutingOspfv3Ipv6Payload
        """
        ...

    def get(
        self, transport_id: str, ospfv3_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportRoutingOspfv3Ipv6Payload,
        GetSingleSdRoutingTransportRoutingOspfv3Ipv6Payload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv6/{ospfv3Id}
        if self._request_adapter.param_checker([(transport_id, str), (ospfv3_id, str)], []):
            params = {
                "transportId": transport_id,
                "ospfv3Id": ospfv3_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv6/{ospfv3Id}",
                return_type=GetSingleSdRoutingTransportRoutingOspfv3Ipv6Payload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv6
        if self._request_adapter.param_checker([(transport_id, str)], [ospfv3_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospfv3/ipv6",
                return_type=GetListSdRoutingTransportRoutingOspfv3Ipv6Payload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
