# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnAndRoutingOspfParcelAssociationForTransportPostRequest,
    CreateWanVpnAndRoutingOspfParcelAssociationForTransportPostResponse,
    EditWanVpnAndRoutingOspfParcelAssociationForTransportPutRequest,
    EditWanVpnAndRoutingOspfParcelAssociationForTransportPutResponse,
    GetSingleSdwanTransportWanVpnRoutingOspfPayload,
    GetWanVpnAssociatedRoutingOspfParcelsForTransportGetResponse,
)


class OspfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vpn_id: str,
        payload: CreateWanVpnAndRoutingOspfParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnAndRoutingOspfParcelAssociationForTransportPostResponse:
        """
        Associate a wan/vpn parcel with a routing/ospf Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospf

        :param transport_id: Feature Profile ID
        :param vpn_id: Lan Vpn Profile Parcel ID
        :param payload: Routing Ospf Profile Parcel Id
        :returns: CreateWanVpnAndRoutingOspfParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospf",
            return_type=CreateWanVpnAndRoutingOspfParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        ospf_id: str,
        payload: EditWanVpnAndRoutingOspfParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditWanVpnAndRoutingOspfParcelAssociationForTransportPutResponse:
        """
        Update a WanVpn parcel and a RoutingOspf Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospf/{ospfId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospf_id: Routing Ospf ID
        :param payload: Routing Ospf Profile Parcel
        :returns: EditWanVpnAndRoutingOspfParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospf/{ospfId}",
            return_type=EditWanVpnAndRoutingOspfParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, ospf_id: str, **kw):
        """
        Delete a WanVpn parcel and a RoutingOspf Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospf/{ospfId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospf_id: Routing Ospf Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospf/{ospfId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, ospf_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnRoutingOspfPayload:
        """
        Get WanVpn parcel associated RoutingOspf Parcel by ospfId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospf/{ospfId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ospf_id: Routing Ospf Parcel ID
        :returns: GetSingleSdwanTransportWanVpnRoutingOspfPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, **kw
    ) -> List[GetWanVpnAssociatedRoutingOspfParcelsForTransportGetResponse]:
        """
        Get WanVpn associated Routing Ospf Parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospf

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: List[GetWanVpnAssociatedRoutingOspfParcelsForTransportGetResponse]
        """
        ...

    def get(
        self, transport_id: str, vpn_id: str, ospf_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetWanVpnAssociatedRoutingOspfParcelsForTransportGetResponse],
        GetSingleSdwanTransportWanVpnRoutingOspfPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospf/{ospfId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (ospf_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "ospfId": ospf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospf/{ospfId}",
                return_type=GetSingleSdwanTransportWanVpnRoutingOspfPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospf
        if self._request_adapter.param_checker([(transport_id, str), (vpn_id, str)], [ospf_id]):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/routing/ospf",
                return_type=List[GetWanVpnAssociatedRoutingOspfParcelsForTransportGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
