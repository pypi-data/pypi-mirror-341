# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateEthernetProfileParcelForMobilityPostRequest,
    GetListMobilityGlobalEthernetPayload,
)


class EthernetBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility/global/{profileId}/ethernet
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, profile_id: str, payload: CreateEthernetProfileParcelForMobilityPostRequest, **kw
    ) -> str:
        """
        Create an ethernet Profile Parcel for Mobility Global Feature Profile
        POST /dataservice/v1/feature-profile/mobility/global/{profileId}/ethernet

        :param profile_id: Feature Profile ID
        :param payload: Ethernet Profile Parcel
        :returns: str
        """
        params = {
            "profileId": profile_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/ethernet",
            return_type=str,
            params=params,
            payload=payload,
            **kw,
        )

    def put(self, profile_id: str, ethernet_id: str, payload: str, **kw):
        """
        Update a Ethernet Profile Parcel for feature profile
        PUT /dataservice/v1/feature-profile/mobility/global/{profileId}/ethernet/{ethernetId}

        :param profile_id: Feature Profile ID
        :param ethernet_id: Profile Parcel ID
        :param payload: Ethernet Profile Parcel
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/ethernet/{ethernetId}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, profile_id: str, ethernet_id: str, **kw):
        """
        Delete a Ethernet Profile Parcel for feature profile
        DELETE /dataservice/v1/feature-profile/mobility/global/{profileId}/ethernet/{ethernetId}

        :param profile_id: Feature Profile ID
        :param ethernet_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/ethernet/{ethernetId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, profile_id: str, ethernet_id: str, **kw) -> str:
        """
        Get Ethernet Profile Parcels for feature profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/ethernet/{ethernetId}

        :param profile_id: Feature Profile ID
        :param ethernet_id: Profile Parcel ID
        :returns: str
        """
        ...

    @overload
    def get(self, profile_id: str, **kw) -> GetListMobilityGlobalEthernetPayload:
        """
        Get Ethernet Profile Parcels for feature profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/ethernet

        :param profile_id: Feature Profile ID
        :returns: GetListMobilityGlobalEthernetPayload
        """
        ...

    def get(
        self, profile_id: str, ethernet_id: Optional[str] = None, **kw
    ) -> Union[GetListMobilityGlobalEthernetPayload, str]:
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/ethernet/{ethernetId}
        if self._request_adapter.param_checker([(profile_id, str), (ethernet_id, str)], []):
            params = {
                "profileId": profile_id,
                "ethernetId": ethernet_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/ethernet/{ethernetId}",
                return_type=str,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/ethernet
        if self._request_adapter.param_checker([(profile_id, str)], [ethernet_id]):
            params = {
                "profileId": profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/ethernet",
                return_type=GetListMobilityGlobalEthernetPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
