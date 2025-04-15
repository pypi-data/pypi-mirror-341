# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLanVpnAndRoutingBgpParcelAssociationForServicePostRequest,
    CreateLanVpnAndRoutingBgpParcelAssociationForServicePostResponse,
    EditLanVpnAndRoutingBgpParcelAssociationForServicePutRequest,
    EditLanVpnAndRoutingBgpParcelAssociationForServicePutResponse,
    GetLanVpnAssociatedRoutingBgpParcelsForServiceGetResponse,
    GetSingleSdwanServiceLanVpnRoutingBgpPayload,
)


class BgpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/bgp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vpn_id: str,
        payload: CreateLanVpnAndRoutingBgpParcelAssociationForServicePostRequest,
        **kw,
    ) -> CreateLanVpnAndRoutingBgpParcelAssociationForServicePostResponse:
        """
        Associate a lanvpn parcel with a routingbgp Parcel for service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/bgp

        :param service_id: Feature Profile ID
        :param vpn_id: Lan Vpn Profile Parcel ID
        :param payload: Routing Bgp Profile Parcel Id
        :returns: CreateLanVpnAndRoutingBgpParcelAssociationForServicePostResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/bgp",
            return_type=CreateLanVpnAndRoutingBgpParcelAssociationForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vpn_id: str,
        bgp_id: str,
        payload: EditLanVpnAndRoutingBgpParcelAssociationForServicePutRequest,
        **kw,
    ) -> EditLanVpnAndRoutingBgpParcelAssociationForServicePutResponse:
        """
        Update a LanVpn parcel and a RoutingBgp Parcel association for service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/bgp/{bgpId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param bgp_id: Routing Bgp ID
        :param payload: Routing Bgp Profile Parcel
        :returns: EditLanVpnAndRoutingBgpParcelAssociationForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "bgpId": bgp_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/bgp/{bgpId}",
            return_type=EditLanVpnAndRoutingBgpParcelAssociationForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, bgp_id: str, **kw):
        """
        Delete a LanVpn parcel and a RoutingBgp Parcel association for service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/bgp/{bgpId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param bgp_id: Routing Bgp Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "bgpId": bgp_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/bgp/{bgpId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vpn_id: str, bgp_id: str, **kw
    ) -> GetSingleSdwanServiceLanVpnRoutingBgpPayload:
        """
        Get LanVpn parcel associated RoutingBgp Parcel by bgpId for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/bgp/{bgpId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param bgp_id: Routing Bgp Parcel ID
        :returns: GetSingleSdwanServiceLanVpnRoutingBgpPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vpn_id: str, **kw
    ) -> List[GetLanVpnAssociatedRoutingBgpParcelsForServiceGetResponse]:
        """
        Get LanVpn associated Routing Bgp Parcels for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/bgp

        :param service_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: List[GetLanVpnAssociatedRoutingBgpParcelsForServiceGetResponse]
        """
        ...

    def get(
        self, service_id: str, vpn_id: str, bgp_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetLanVpnAssociatedRoutingBgpParcelsForServiceGetResponse],
        GetSingleSdwanServiceLanVpnRoutingBgpPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/bgp/{bgpId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (bgp_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/bgp/{bgpId}",
                return_type=GetSingleSdwanServiceLanVpnRoutingBgpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/bgp
        if self._request_adapter.param_checker([(service_id, str), (vpn_id, str)], [bgp_id]):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/bgp",
                return_type=List[GetLanVpnAssociatedRoutingBgpParcelsForServiceGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
