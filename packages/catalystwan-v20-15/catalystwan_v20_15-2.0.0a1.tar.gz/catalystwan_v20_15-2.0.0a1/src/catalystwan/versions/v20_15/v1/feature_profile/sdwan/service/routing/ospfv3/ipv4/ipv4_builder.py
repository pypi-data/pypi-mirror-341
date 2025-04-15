# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateRoutingOspfv3Ipv4AfProfileParcelForServicePostRequest,
    CreateRoutingOspfv3Ipv4AfProfileParcelForServicePostResponse,
    EditRoutingOspfv3IPv4AfProfileParcelForServicePutRequest,
    EditRoutingOspfv3IPv4AfProfileParcelForServicePutResponse,
    GetListSdwanServiceRoutingOspfv3Ipv4Payload,
    GetSingleSdwanServiceRoutingOspfv3Ipv4Payload,
)


class Ipv4Builder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv4
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        payload: CreateRoutingOspfv3Ipv4AfProfileParcelForServicePostRequest,
        **kw,
    ) -> CreateRoutingOspfv3Ipv4AfProfileParcelForServicePostResponse:
        """
        Create a Routing OSPFv3 IPv4 Address Family Profile Parcel for Service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv4

        :param service_id: Feature Profile ID
        :param payload: Routing OSPFv3 IPv4 Address Family Profile Parcel
        :returns: CreateRoutingOspfv3Ipv4AfProfileParcelForServicePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv4",
            return_type=CreateRoutingOspfv3Ipv4AfProfileParcelForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        ospfv3_id: str,
        payload: EditRoutingOspfv3IPv4AfProfileParcelForServicePutRequest,
        **kw,
    ) -> EditRoutingOspfv3IPv4AfProfileParcelForServicePutResponse:
        """
        Update a Routing OSPFv3 IPv4 Address Family Profile Parcel for Service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param service_id: Feature Profile ID
        :param ospfv3_id: Profile Parcel ID
        :param payload: Routing OSPFv3 IPv4 Address Family Profile Parcel
        :returns: EditRoutingOspfv3IPv4AfProfileParcelForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv4/{ospfv3Id}",
            return_type=EditRoutingOspfv3IPv4AfProfileParcelForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, ospfv3_id: str, **kw):
        """
        Delete a Routing OSPFv3 IPv4 Address Family Profile Parcel for Service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param service_id: Feature Profile ID
        :param ospfv3_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv4/{ospfv3Id}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, ospfv3_id: str, **kw
    ) -> GetSingleSdwanServiceRoutingOspfv3Ipv4Payload:
        """
        Get Routing OSPFv3 IPv4 Address Family Profile Parcel by parcelId for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param service_id: Feature Profile ID
        :param ospfv3_id: Profile Parcel ID
        :returns: GetSingleSdwanServiceRoutingOspfv3Ipv4Payload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdwanServiceRoutingOspfv3Ipv4Payload:
        """
        Get Routing OSPFv3 IPv4 Address Family Profile Parcels for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv4

        :param service_id: Feature Profile ID
        :returns: GetListSdwanServiceRoutingOspfv3Ipv4Payload
        """
        ...

    def get(
        self, service_id: str, ospfv3_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanServiceRoutingOspfv3Ipv4Payload, GetSingleSdwanServiceRoutingOspfv3Ipv4Payload
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv4/{ospfv3Id}
        if self._request_adapter.param_checker([(service_id, str), (ospfv3_id, str)], []):
            params = {
                "serviceId": service_id,
                "ospfv3Id": ospfv3_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv4/{ospfv3Id}",
                return_type=GetSingleSdwanServiceRoutingOspfv3Ipv4Payload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv4
        if self._request_adapter.param_checker([(service_id, str)], [ospfv3_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv4",
                return_type=GetListSdwanServiceRoutingOspfv3Ipv4Payload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
