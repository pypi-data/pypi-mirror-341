# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateRoutingOspfProfileParcelForServicePostRequest,
    CreateRoutingOspfProfileParcelForServicePostResponse,
    EditRoutingOspfProfileParcelForServicePutRequest,
    EditRoutingOspfProfileParcelForServicePutResponse,
    GetListSdwanServiceRoutingOspfPayload,
    GetSingleSdwanServiceRoutingOspfPayload,
)


class OspfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/routing/ospf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateRoutingOspfProfileParcelForServicePostRequest, **kw
    ) -> CreateRoutingOspfProfileParcelForServicePostResponse:
        """
        Create a Routing Ospf Profile Parcel for Service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospf

        :param service_id: Feature Profile ID
        :param payload: Routing Ospf Profile Parcel
        :returns: CreateRoutingOspfProfileParcelForServicePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospf",
            return_type=CreateRoutingOspfProfileParcelForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        ospf_id: str,
        payload: EditRoutingOspfProfileParcelForServicePutRequest,
        **kw,
    ) -> EditRoutingOspfProfileParcelForServicePutResponse:
        """
        Update a Routing Ospf Profile Parcel for Service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospf/{ospfId}

        :param service_id: Feature Profile ID
        :param ospf_id: Profile Parcel ID
        :param payload: Routing Ospf Profile Parcel
        :returns: EditRoutingOspfProfileParcelForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospf/{ospfId}",
            return_type=EditRoutingOspfProfileParcelForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, ospf_id: str, **kw):
        """
        Delete a Routing Ospf Profile Parcel for Service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospf/{ospfId}

        :param service_id: Feature Profile ID
        :param ospf_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospf/{ospfId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, service_id: str, ospf_id: str, **kw) -> GetSingleSdwanServiceRoutingOspfPayload:
        """
        Get Routing Ospf Profile Parcel by parcelId for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospf/{ospfId}

        :param service_id: Feature Profile ID
        :param ospf_id: Profile Parcel ID
        :returns: GetSingleSdwanServiceRoutingOspfPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdwanServiceRoutingOspfPayload:
        """
        Get Routing Ospf Profile Parcels for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospf

        :param service_id: Feature Profile ID
        :returns: GetListSdwanServiceRoutingOspfPayload
        """
        ...

    def get(
        self, service_id: str, ospf_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanServiceRoutingOspfPayload, GetSingleSdwanServiceRoutingOspfPayload]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospf/{ospfId}
        if self._request_adapter.param_checker([(service_id, str), (ospf_id, str)], []):
            params = {
                "serviceId": service_id,
                "ospfId": ospf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospf/{ospfId}",
                return_type=GetSingleSdwanServiceRoutingOspfPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospf
        if self._request_adapter.param_checker([(service_id, str)], [ospf_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospf",
                return_type=GetListSdwanServiceRoutingOspfPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
