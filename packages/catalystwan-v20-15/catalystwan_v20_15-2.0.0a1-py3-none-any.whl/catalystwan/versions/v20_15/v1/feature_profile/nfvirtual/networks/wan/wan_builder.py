# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualWanParcelPostRequest,
    CreateNfvirtualWanParcelPostResponse,
    EditNfvirtualWanParcelPutRequest,
    EditNfvirtualWanParcelPutResponse,
    GetSingleNfvirtualNetworksWanPayload,
)


class WanBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/networks/{networksId}/wan
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, networks_id: str, payload: CreateNfvirtualWanParcelPostRequest, **kw
    ) -> CreateNfvirtualWanParcelPostResponse:
        """
        Create a WAN Profile Parcel for Networks feature profile
        POST /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/wan

        :param networks_id: Feature Profile ID
        :param payload: WAN config Profile Parcel
        :returns: CreateNfvirtualWanParcelPostResponse
        """
        params = {
            "networksId": networks_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/wan",
            return_type=CreateNfvirtualWanParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(self, networks_id: str, wan_id: str, **kw) -> GetSingleNfvirtualNetworksWanPayload:
        """
        Get WAN Profile Parcels for Networks feature profile
        GET /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/wan/{wanId}

        :param networks_id: Feature Profile ID
        :param wan_id: Profile Parcel ID
        :returns: GetSingleNfvirtualNetworksWanPayload
        """
        params = {
            "networksId": networks_id,
            "wanId": wan_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/wan/{wanId}",
            return_type=GetSingleNfvirtualNetworksWanPayload,
            params=params,
            **kw,
        )

    def put(
        self, networks_id: str, wan_id: str, payload: EditNfvirtualWanParcelPutRequest, **kw
    ) -> EditNfvirtualWanParcelPutResponse:
        """
        Edit a WAN Profile Parcel for networks feature profile
        PUT /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/wan/{wanId}

        :param networks_id: Feature Profile ID
        :param wan_id: Profile Parcel ID
        :param payload: WAN Profile Parcel
        :returns: EditNfvirtualWanParcelPutResponse
        """
        params = {
            "networksId": networks_id,
            "wanId": wan_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/wan/{wanId}",
            return_type=EditNfvirtualWanParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, networks_id: str, wan_id: str, **kw):
        """
        Delete a WAN Profile Parcel for Networks feature profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/wan/{wanId}

        :param networks_id: Feature Profile ID
        :param wan_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "networksId": networks_id,
            "wanId": wan_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/wan/{wanId}",
            params=params,
            **kw,
        )
