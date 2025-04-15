# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportGlobalVrfInterfaceEthernetParcelForTransportPostRequest,
    CreateSdroutingTransportGlobalVrfInterfaceEthernetParcelForTransportPostResponse,
    EditSdroutingTransportGlobalVrfInterfaceEthernetParcelForTransportPutRequest,
    EditSdroutingTransportGlobalVrfInterfaceEthernetParcelForTransportPutResponse,
    GetListSdRoutingTransportGlobalVrfWanInterfaceEthernetPayload,
    GetSingleSdRoutingTransportGlobalVrfWanInterfaceEthernetPayload,
)


class EthernetBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ethernet
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vrf_id: str,
        payload: CreateSdroutingTransportGlobalVrfInterfaceEthernetParcelForTransportPostRequest,
        **kw,
    ) -> CreateSdroutingTransportGlobalVrfInterfaceEthernetParcelForTransportPostResponse:
        """
        Create a SD-Routing Ethernet interface feature for global VRF in Transport Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ethernet

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :param payload: SD-Routing Ethernet interface feature for global VRF
        :returns: CreateSdroutingTransportGlobalVrfInterfaceEthernetParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ethernet",
            return_type=CreateSdroutingTransportGlobalVrfInterfaceEthernetParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vrf_id: str,
        ethernet_id: str,
        payload: EditSdroutingTransportGlobalVrfInterfaceEthernetParcelForTransportPutRequest,
        **kw,
    ) -> EditSdroutingTransportGlobalVrfInterfaceEthernetParcelForTransportPutResponse:
        """
        Edit a SD-Routing Ethernet interface feature for global VRF in Transport Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ethernet/{ethernetId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :param ethernet_id: Interface Feature ID
        :param payload: SD-Routing Ethernet interface feature for global VRF
        :returns: EditSdroutingTransportGlobalVrfInterfaceEthernetParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ethernet/{ethernetId}",
            return_type=EditSdroutingTransportGlobalVrfInterfaceEthernetParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vrf_id: str, ethernet_id: str, **kw):
        """
        Delete a SD-Routing Ethernet interface feature for global VRF in Transport Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ethernet/{ethernetId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :param ethernet_id: Interface Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ethernet/{ethernetId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vrf_id: str, ethernet_id: str, **kw
    ) -> GetSingleSdRoutingTransportGlobalVrfWanInterfaceEthernetPayload:
        """
        Get a SD-Routing Ethernet interface feature for global VRF by ethernetId in Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ethernet/{ethernetId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :param ethernet_id: Interface Feature ID
        :returns: GetSingleSdRoutingTransportGlobalVrfWanInterfaceEthernetPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vrf_id: str, **kw
    ) -> GetListSdRoutingTransportGlobalVrfWanInterfaceEthernetPayload:
        """
        Get all  Ethernet interface features for global VRF in Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ethernet

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :returns: GetListSdRoutingTransportGlobalVrfWanInterfaceEthernetPayload
        """
        ...

    def get(
        self, transport_id: str, vrf_id: str, ethernet_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportGlobalVrfWanInterfaceEthernetPayload,
        GetSingleSdRoutingTransportGlobalVrfWanInterfaceEthernetPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ethernet/{ethernetId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vrf_id, str), (ethernet_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
                "ethernetId": ethernet_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ethernet/{ethernetId}",
                return_type=GetSingleSdRoutingTransportGlobalVrfWanInterfaceEthernetPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ethernet
        if self._request_adapter.param_checker([(transport_id, str), (vrf_id, str)], [ethernet_id]):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ethernet",
                return_type=GetListSdRoutingTransportGlobalVrfWanInterfaceEthernetPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
