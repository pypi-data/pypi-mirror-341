# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnInterfaceCellularParcelForTransportPostRequest,
    CreateWanVpnInterfaceCellularParcelForTransportPostResponse,
    EditWanVpnInterfaceCellularParcelForTransportPutRequest,
    EditWanVpnInterfaceCellularParcelForTransportPutResponse,
    GetListSdwanTransportWanVpnInterfaceCellularPayload,
    GetSingleSdwanTransportWanVpnInterfaceCellularPayload,
)

if TYPE_CHECKING:
    from .ipv6_tracker.ipv6_tracker_builder import Ipv6TrackerBuilder
    from .ipv6_trackergroup.ipv6_trackergroup_builder import Ipv6TrackergroupBuilder
    from .schema.schema_builder import SchemaBuilder
    from .tracker.tracker_builder import TrackerBuilder
    from .trackergroup.trackergroup_builder import TrackergroupBuilder


class CellularBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/wan/vpn/interface/cellular
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vpn_id: str,
        payload: CreateWanVpnInterfaceCellularParcelForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnInterfaceCellularParcelForTransportPostResponse:
        """
        Create a wanvpn Cellular interface Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular

        :param transport_id: Feature Profile ID
        :param vpn_id: VPN Profile Parcel ID
        :param payload: WanVpn Interface Cellular Profile Parcel
        :returns: CreateWanVpnInterfaceCellularParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular",
            return_type=CreateWanVpnInterfaceCellularParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        intf_id: str,
        payload: EditWanVpnInterfaceCellularParcelForTransportPutRequest,
        **kw,
    ) -> EditWanVpnInterfaceCellularParcelForTransportPutResponse:
        """
        Update a wanvpn Cellular Interface Parcel for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{intfId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param intf_id: Interface ID
        :param payload: WanVpn Cellular Interface Profile Parcel
        :returns: EditWanVpnInterfaceCellularParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "intfId": intf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{intfId}",
            return_type=EditWanVpnInterfaceCellularParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, intf_id: str, **kw):
        """
        Delete a wanvpn Cellular interface Parcel for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{intfId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param intf_id: Interface Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "intfId": intf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{intfId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, intf_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnInterfaceCellularPayload:
        """
        Get wanvpn Cellular interface Parcel by intfId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{intfId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param intf_id: Interface Parcel ID
        :returns: GetSingleSdwanTransportWanVpnInterfaceCellularPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, **kw
    ) -> GetListSdwanTransportWanVpnInterfaceCellularPayload:
        """
        Get Interface Cellular Parcels for transport Wan Vpn Parcel
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: GetListSdwanTransportWanVpnInterfaceCellularPayload
        """
        ...

    def get(
        self, transport_id: str, vpn_id: str, intf_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportWanVpnInterfaceCellularPayload,
        GetSingleSdwanTransportWanVpnInterfaceCellularPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{intfId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (intf_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "intfId": intf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{intfId}",
                return_type=GetSingleSdwanTransportWanVpnInterfaceCellularPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular
        if self._request_adapter.param_checker([(transport_id, str), (vpn_id, str)], [intf_id]):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular",
                return_type=GetListSdwanTransportWanVpnInterfaceCellularPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def ipv6_tracker(self) -> Ipv6TrackerBuilder:
        """
        The ipv6-tracker property
        """
        from .ipv6_tracker.ipv6_tracker_builder import Ipv6TrackerBuilder

        return Ipv6TrackerBuilder(self._request_adapter)

    @property
    def ipv6_trackergroup(self) -> Ipv6TrackergroupBuilder:
        """
        The ipv6-trackergroup property
        """
        from .ipv6_trackergroup.ipv6_trackergroup_builder import Ipv6TrackergroupBuilder

        return Ipv6TrackergroupBuilder(self._request_adapter)

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

    @property
    def trackergroup(self) -> TrackergroupBuilder:
        """
        The trackergroup property
        """
        from .trackergroup.trackergroup_builder import TrackergroupBuilder

        return TrackergroupBuilder(self._request_adapter)
