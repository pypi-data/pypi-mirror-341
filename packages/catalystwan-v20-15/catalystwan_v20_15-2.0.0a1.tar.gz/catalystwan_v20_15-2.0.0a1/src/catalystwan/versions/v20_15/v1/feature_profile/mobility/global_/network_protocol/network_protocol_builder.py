# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNetworkProtocolProfileParcelForMobilityPostRequest,
    EditNetworkProtocolProfileParcelForMobilityPutRequest,
    GetListMobilityGlobalNetworkprotocolPayload,
    GetSingleMobilityGlobalNetworkprotocolPayload,
)


class NetworkProtocolBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility/global/{profileId}/networkProtocol
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        profile_id: str,
        payload: CreateNetworkProtocolProfileParcelForMobilityPostRequest,
        **kw,
    ) -> str:
        """
        Create an NetworkProtocol Profile Parcel for Mobility Global Feature Profile
        POST /dataservice/v1/feature-profile/mobility/global/{profileId}/networkProtocol

        :param profile_id: Feature Profile ID
        :param payload: NetworkProtocol Profile Parcel
        :returns: str
        """
        params = {
            "profileId": profile_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/networkProtocol",
            return_type=str,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        profile_id: str,
        network_protocol_id: str,
        payload: EditNetworkProtocolProfileParcelForMobilityPutRequest,
        **kw,
    ):
        """
        Edit an Network Protocol Profile Parcel for Mobility Global Feature Profile
        PUT /dataservice/v1/feature-profile/mobility/global/{profileId}/networkProtocol/{networkProtocolId}

        :param profile_id: Feature Profile ID
        :param network_protocol_id: Profile Parcel ID
        :param payload: Network Protocol Profile Parcel
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "networkProtocolId": network_protocol_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/networkProtocol/{networkProtocolId}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, profile_id: str, network_protocol_id: str, **kw):
        """
        Delete a Network Protocol Profile Parcel for Mobility Global Feature Profile
        DELETE /dataservice/v1/feature-profile/mobility/global/{profileId}/networkProtocol/{networkProtocolId}

        :param profile_id: Feature Profile ID
        :param network_protocol_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "profileId": profile_id,
            "networkProtocolId": network_protocol_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/mobility/global/{profileId}/networkProtocol/{networkProtocolId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, profile_id: str, network_protocol_id: str, **kw
    ) -> GetSingleMobilityGlobalNetworkprotocolPayload:
        """
        Get an Mobility NetworkProtocol Profile Parcel for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/networkProtocol/{networkProtocolId}

        :param profile_id: Feature Profile ID
        :param network_protocol_id: Profile Parcel ID
        :returns: GetSingleMobilityGlobalNetworkprotocolPayload
        """
        ...

    @overload
    def get(self, profile_id: str, **kw) -> GetListMobilityGlobalNetworkprotocolPayload:
        """
        Get an Mobility NetworkProtocol Profile Parcel list for Mobility Global Feature Profile
        GET /dataservice/v1/feature-profile/mobility/global/{profileId}/networkProtocol

        :param profile_id: Feature Profile ID
        :returns: GetListMobilityGlobalNetworkprotocolPayload
        """
        ...

    def get(
        self, profile_id: str, network_protocol_id: Optional[str] = None, **kw
    ) -> Union[
        GetListMobilityGlobalNetworkprotocolPayload, GetSingleMobilityGlobalNetworkprotocolPayload
    ]:
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/networkProtocol/{networkProtocolId}
        if self._request_adapter.param_checker([(profile_id, str), (network_protocol_id, str)], []):
            params = {
                "profileId": profile_id,
                "networkProtocolId": network_protocol_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/networkProtocol/{networkProtocolId}",
                return_type=GetSingleMobilityGlobalNetworkprotocolPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/mobility/global/{profileId}/networkProtocol
        if self._request_adapter.param_checker([(profile_id, str)], [network_protocol_id]):
            params = {
                "profileId": profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{profileId}/networkProtocol",
                return_type=GetListMobilityGlobalNetworkprotocolPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
