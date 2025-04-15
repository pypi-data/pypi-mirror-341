# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnAndRoutingOspfv3Ipv6AfParcelAssociationForTransportPostRequest,
    CreateWanVpnAndRoutingOspfv3Ipv6AfParcelAssociationForTransportPostResponse,
    EditWanVpnAndRoutingOspfv3IPv6AfParcelAssociationForTransportPutRequest,
    EditWanVpnAndRoutingOspfv3IPv6AfParcelAssociationForTransportPutResponse,
    GetSingleSdwanTransportWanVpnRoutingOspfv3Ipv6Payload,
    GetWanVpnAssociatedRoutingOspfv3IPv6AfParcelsForTransportGetResponse,
)


class Ipv6Builder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospfv3/ipv6
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vpn_id: str,
        payload: CreateWanVpnAndRoutingOspfv3Ipv6AfParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnAndRoutingOspfv3Ipv6AfParcelAssociationForTransportPostResponse:
        """
        Associate a WAN VPN parcel with a routing OSPFv3 parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospfv3/ipv6

        :param transport_id: Feature Profile ID
        :param vpn_id: WAN Vpn Profile Parcel ID
        :param payload: Routing Ospfv3 IPv6Address Family Profile Parcel Id
        :returns: CreateWanVpnAndRoutingOspfv3Ipv6AfParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospfv3/ipv6",
            return_type=CreateWanVpnAndRoutingOspfv3Ipv6AfParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        ospfv3_id: str,
        payload: EditWanVpnAndRoutingOspfv3IPv6AfParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditWanVpnAndRoutingOspfv3IPv6AfParcelAssociationForTransportPutResponse:
        """
        Update a WAN VPN parcel and a routing OSPFv3 parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospfv3_id: Routing Ospfv3 IPv6 Address Family parcel ID
        :param payload: Routing Ospfv3 IPv6 Address Family Profile Parcel
        :returns: EditWanVpnAndRoutingOspfv3IPv6AfParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospfv3/ipv6/{ospfv3Id}",
            return_type=EditWanVpnAndRoutingOspfv3IPv6AfParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, ospfv3_id: str, **kw):
        """
        Delete a WAN VPN parcel and a routing OSPFv3 parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospfv3_id: Routing Ospfv3 IPv6 Address Family Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospfv3/ipv6/{ospfv3Id}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, ospfv3_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnRoutingOspfv3Ipv6Payload:
        """
        Get WAN VPN parcel associated OSPFv3 IPv6 parcel by ID for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospfv3_id: Routing Ospfv3 IPv6 Address Family Parcel ID
        :returns: GetSingleSdwanTransportWanVpnRoutingOspfv3Ipv6Payload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, **kw
    ) -> List[GetWanVpnAssociatedRoutingOspfv3IPv6AfParcelsForTransportGetResponse]:
        """
        Get WAN VPN associated routing OSPFv3 IPv6 address family parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospfv3/ipv6

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: List[GetWanVpnAssociatedRoutingOspfv3IPv6AfParcelsForTransportGetResponse]
        """
        ...

    def get(
        self, transport_id: str, vpn_id: str, ospfv3_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetWanVpnAssociatedRoutingOspfv3IPv6AfParcelsForTransportGetResponse],
        GetSingleSdwanTransportWanVpnRoutingOspfv3Ipv6Payload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospfv3/ipv6/{ospfv3Id}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (ospfv3_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "ospfv3Id": ospfv3_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospfv3/ipv6/{ospfv3Id}",
                return_type=GetSingleSdwanTransportWanVpnRoutingOspfv3Ipv6Payload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospfv3/ipv6
        if self._request_adapter.param_checker([(transport_id, str), (vpn_id, str)], [ospfv3_id]):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospfv3/ipv6",
                return_type=List[
                    GetWanVpnAssociatedRoutingOspfv3IPv6AfParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
