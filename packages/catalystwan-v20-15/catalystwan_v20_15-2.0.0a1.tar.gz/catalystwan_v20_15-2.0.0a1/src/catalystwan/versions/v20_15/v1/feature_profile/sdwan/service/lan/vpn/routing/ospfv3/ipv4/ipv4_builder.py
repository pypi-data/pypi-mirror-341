# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLanVpnAndRoutingOspfv3IPv4ParcelAssociationForServicePostRequest,
    CreateLanVpnAndRoutingOspfv3IPv4ParcelAssociationForServicePostResponse,
    EditLanVpnAndRoutingOspfv3IPv4ParcelAssociationForServicePutRequest,
    EditLanVpnAndRoutingOspfv3IPv4ParcelAssociationForServicePutResponse,
    GetLanVpnAssociatedRoutingOspfv3IPv4ParcelsForServiceGetResponse,
    GetSingleSdwanServiceLanVpnRoutingOspfv3Ipv4Payload,
)


class Ipv4Builder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv4
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vpn_id: str,
        payload: CreateLanVpnAndRoutingOspfv3IPv4ParcelAssociationForServicePostRequest,
        **kw,
    ) -> CreateLanVpnAndRoutingOspfv3IPv4ParcelAssociationForServicePostResponse:
        """
        Associate a LAN VPN parcel with a IPv4 address family OSPFv3 Parcel for service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv4

        :param service_id: Feature Profile ID
        :param vpn_id: Lan Vpn Profile Parcel ID
        :param payload: IPv4 address family OSPFv3 Profile Parcel Id
        :returns: CreateLanVpnAndRoutingOspfv3IPv4ParcelAssociationForServicePostResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv4",
            return_type=CreateLanVpnAndRoutingOspfv3IPv4ParcelAssociationForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vpn_id: str,
        ospfv3_id: str,
        payload: EditLanVpnAndRoutingOspfv3IPv4ParcelAssociationForServicePutRequest,
        **kw,
    ) -> EditLanVpnAndRoutingOspfv3IPv4ParcelAssociationForServicePutResponse:
        """
        Update a LAN VPN parcel and a routing OSPFv3 IPv4 Parcel association for service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospfv3_id: IPv4 address family OSPFv3 ID
        :param payload: IPv4 address family OSPFv3 Profile Parcel
        :returns: EditLanVpnAndRoutingOspfv3IPv4ParcelAssociationForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv4/{ospfv3Id}",
            return_type=EditLanVpnAndRoutingOspfv3IPv4ParcelAssociationForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, ospfv3_id: str, **kw):
        """
        Delete a LAN VPN parcel and a IPv4 OSPFv3 parcel association for service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospfv3_id: IPv4 Address Family OSPFv3 IPv4 Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv4/{ospfv3Id}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vpn_id: str, ospfv3_id: str, **kw
    ) -> GetSingleSdwanServiceLanVpnRoutingOspfv3Ipv4Payload:
        """
        Get LanVpn parcel associated IPv4 address family OSPFv3 IPv4 Parcel by ospfv3Id for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospfv3_id: IPv4 Address Family OSPFv3 Parcel ID
        :returns: GetSingleSdwanServiceLanVpnRoutingOspfv3Ipv4Payload
        """
        ...

    @overload
    def get(
        self, service_id: str, vpn_id: str, **kw
    ) -> List[GetLanVpnAssociatedRoutingOspfv3IPv4ParcelsForServiceGetResponse]:
        """
        Get LanVpn associated IPv4 address family OSPFv3 Parcels for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv4

        :param service_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: List[GetLanVpnAssociatedRoutingOspfv3IPv4ParcelsForServiceGetResponse]
        """
        ...

    def get(
        self, service_id: str, vpn_id: str, ospfv3_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetLanVpnAssociatedRoutingOspfv3IPv4ParcelsForServiceGetResponse],
        GetSingleSdwanServiceLanVpnRoutingOspfv3Ipv4Payload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv4/{ospfv3Id}
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (ospfv3_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "ospfv3Id": ospfv3_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv4/{ospfv3Id}",
                return_type=GetSingleSdwanServiceLanVpnRoutingOspfv3Ipv4Payload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv4
        if self._request_adapter.param_checker([(service_id, str), (vpn_id, str)], [ospfv3_id]):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/ospfv3/ipv4",
                return_type=List[GetLanVpnAssociatedRoutingOspfv3IPv4ParcelsForServiceGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
