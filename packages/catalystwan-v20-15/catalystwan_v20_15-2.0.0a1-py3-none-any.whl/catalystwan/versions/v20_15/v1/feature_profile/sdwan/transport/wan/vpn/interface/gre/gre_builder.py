# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnInterfaceGreParcelForTransportPostRequest,
    CreateWanVpnInterfaceGreParcelForTransportPostResponse,
    EditWanVpnInterfaceGreParcelForTransportPutRequest,
    EditWanVpnInterfaceGreParcelForTransportPutResponse,
    GetListSdwanTransportWanVpnInterfaceGrePayload,
    GetSingleSdwanTransportWanVpnInterfaceGrePayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder
    from .tracker.tracker_builder import TrackerBuilder


class GreBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/wan/vpn/interface/gre
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vpn_id: str,
        payload: CreateWanVpnInterfaceGreParcelForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnInterfaceGreParcelForTransportPostResponse:
        """
        Create a WanVpn InterfaceGre parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param payload: Wan Vpn Interface Gre Profile Parcel
        :returns: CreateWanVpnInterfaceGreParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre",
            return_type=CreateWanVpnInterfaceGreParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        gre_id: str,
        payload: EditWanVpnInterfaceGreParcelForTransportPutRequest,
        **kw,
    ) -> EditWanVpnInterfaceGreParcelForTransportPutResponse:
        """
        Update a WanVpn InterfaceGre Parcel for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param gre_id: Interface ID
        :param payload: Wan Vpn Interface Gre Profile Parcel
        :returns: EditWanVpnInterfaceGreParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "greId": gre_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}",
            return_type=EditWanVpnInterfaceGreParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, gre_id: str, **kw):
        """
        Delete a  WanVpn InterfaceGre Parcel for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param gre_id: Interface Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "greId": gre_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, gre_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnInterfaceGrePayload:
        """
        Get WanVpn InterfaceGre Parcel by greId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param gre_id: Interface Parcel ID
        :returns: GetSingleSdwanTransportWanVpnInterfaceGrePayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, **kw
    ) -> GetListSdwanTransportWanVpnInterfaceGrePayload:
        """
        Get InterfaceGre Parcels for transport WanVpn Parcel
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: GetListSdwanTransportWanVpnInterfaceGrePayload
        """
        ...

    def get(
        self, transport_id: str, vpn_id: str, gre_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportWanVpnInterfaceGrePayload,
        GetSingleSdwanTransportWanVpnInterfaceGrePayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (gre_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "greId": gre_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre/{greId}",
                return_type=GetSingleSdwanTransportWanVpnInterfaceGrePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre
        if self._request_adapter.param_checker([(transport_id, str), (vpn_id, str)], [gre_id]):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/gre",
                return_type=GetListSdwanTransportWanVpnInterfaceGrePayload,
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

    @property
    def tracker(self) -> TrackerBuilder:
        """
        The tracker property
        """
        from .tracker.tracker_builder import TrackerBuilder

        return TrackerBuilder(self._request_adapter)
