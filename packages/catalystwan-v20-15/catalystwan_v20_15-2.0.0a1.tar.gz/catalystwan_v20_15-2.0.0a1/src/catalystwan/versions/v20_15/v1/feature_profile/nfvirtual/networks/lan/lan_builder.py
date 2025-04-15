# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualLanParcelPostRequest,
    CreateNfvirtualLanParcelPostResponse,
    EditNfvirtualLanParcelPutRequest,
    EditNfvirtualLanParcelPutResponse,
    GetSingleNfvirtualNetworksLanPayload,
)


class LanBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/networks/{networksId}/lan
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, networks_id: str, payload: CreateNfvirtualLanParcelPostRequest, **kw
    ) -> CreateNfvirtualLanParcelPostResponse:
        """
        Create LAN Profile Parcel for Networks feature profile
        POST /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/lan

        :param networks_id: Feature Profile ID
        :param payload: LAN config Profile Parcel
        :returns: CreateNfvirtualLanParcelPostResponse
        """
        params = {
            "networksId": networks_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/lan",
            return_type=CreateNfvirtualLanParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(self, networks_id: str, lan_id: str, **kw) -> GetSingleNfvirtualNetworksLanPayload:
        """
        Get LAN Profile Parcels for Networks feature profile
        GET /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/lan/{lanId}

        :param networks_id: Feature Profile ID
        :param lan_id: Profile Parcel ID
        :returns: GetSingleNfvirtualNetworksLanPayload
        """
        params = {
            "networksId": networks_id,
            "lanId": lan_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/lan/{lanId}",
            return_type=GetSingleNfvirtualNetworksLanPayload,
            params=params,
            **kw,
        )

    def put(
        self, networks_id: str, lan_id: str, payload: EditNfvirtualLanParcelPutRequest, **kw
    ) -> EditNfvirtualLanParcelPutResponse:
        """
        Edit a  LAN Profile Parcel for networks feature profile
        PUT /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/lan/{lanId}

        :param networks_id: Feature Profile ID
        :param lan_id: Profile Parcel ID
        :param payload: LAN Profile Parcel
        :returns: EditNfvirtualLanParcelPutResponse
        """
        params = {
            "networksId": networks_id,
            "lanId": lan_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/lan/{lanId}",
            return_type=EditNfvirtualLanParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, networks_id: str, lan_id: str, **kw):
        """
        Delete a LAN Profile Parcel for Networks feature profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/lan/{lanId}

        :param networks_id: Feature Profile ID
        :param lan_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "networksId": networks_id,
            "lanId": lan_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/lan/{lanId}",
            params=params,
            **kw,
        )
