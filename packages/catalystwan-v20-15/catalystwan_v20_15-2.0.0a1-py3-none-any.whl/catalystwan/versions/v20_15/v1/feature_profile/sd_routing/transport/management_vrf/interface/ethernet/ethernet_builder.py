# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingManagementVrfInterfaceEthernetParcelForTransportProfilePostRequest,
    CreateSdroutingManagementVrfInterfaceEthernetParcelForTransportProfilePostResponse,
    EditSdroutingManagementVrfInterfaceEthernetParcelForTransportProfilePutRequest,
    EditSdroutingManagementVrfInterfaceEthernetParcelForTransportProfilePutResponse,
    GetListSdRoutingTransportManagementVrfInterfaceEthernetPayload,
    GetSingleSdRoutingTransportManagementVrfInterfaceEthernetPayload,
)


class EthernetBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}/interface/ethernet
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vrf_id: str,
        payload: CreateSdroutingManagementVrfInterfaceEthernetParcelForTransportProfilePostRequest,
        **kw,
    ) -> CreateSdroutingManagementVrfInterfaceEthernetParcelForTransportProfilePostResponse:
        """
        Create a SD-Routing Management Ethernet interface feature for management VRF in Transport Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}/interface/ethernet

        :param transport_id: Transport Profile ID
        :param vrf_id: Management VRF Feature ID
        :param payload: SD-Routing Management Ethernet interface feature schema for management VRF
        :returns: CreateSdroutingManagementVrfInterfaceEthernetParcelForTransportProfilePostResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}/interface/ethernet",
            return_type=CreateSdroutingManagementVrfInterfaceEthernetParcelForTransportProfilePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vrf_id: str,
        ethernet_id: str,
        payload: EditSdroutingManagementVrfInterfaceEthernetParcelForTransportProfilePutRequest,
        **kw,
    ) -> EditSdroutingManagementVrfInterfaceEthernetParcelForTransportProfilePutResponse:
        """
        Edit a SD-Routing Management Ethernet interface feature for management VRF in Transport Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}/interface/ethernet/{ethernetId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Management VRF Feature ID
        :param ethernet_id: Management Interface Feature ID
        :param payload: SD-Routing Management Ethernet interface feature schema for management VRF
        :returns: EditSdroutingManagementVrfInterfaceEthernetParcelForTransportProfilePutResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}/interface/ethernet/{ethernetId}",
            return_type=EditSdroutingManagementVrfInterfaceEthernetParcelForTransportProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vrf_id: str, ethernet_id: str, **kw):
        """
        Delete a SD-Routing Management Ethernet interface feature for management VRF in Transport Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}/interface/ethernet/{ethernetId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Management VRF Feature ID
        :param ethernet_id: Management Interface Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}/interface/ethernet/{ethernetId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vrf_id: str, ethernet_id: str, **kw
    ) -> GetSingleSdRoutingTransportManagementVrfInterfaceEthernetPayload:
        """
        Get a SD-Routing Management Ethernet interface feature for management VRF by ethernetId in Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}/interface/ethernet/{ethernetId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Management VRF Feature ID
        :param ethernet_id: Management Interface Feature ID
        :returns: GetSingleSdRoutingTransportManagementVrfInterfaceEthernetPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vrf_id: str, **kw
    ) -> GetListSdRoutingTransportManagementVrfInterfaceEthernetPayload:
        """
        Get all  Management Ethernet interface features for management VRF in Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}/interface/ethernet

        :param transport_id: Transport Profile ID
        :param vrf_id: Management VRF Feature ID
        :returns: GetListSdRoutingTransportManagementVrfInterfaceEthernetPayload
        """
        ...

    def get(
        self, transport_id: str, vrf_id: str, ethernet_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportManagementVrfInterfaceEthernetPayload,
        GetSingleSdRoutingTransportManagementVrfInterfaceEthernetPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}/interface/ethernet/{ethernetId}
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
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}/interface/ethernet/{ethernetId}",
                return_type=GetSingleSdRoutingTransportManagementVrfInterfaceEthernetPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}/interface/ethernet
        if self._request_adapter.param_checker([(transport_id, str), (vrf_id, str)], [ethernet_id]):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}/interface/ethernet",
                return_type=GetListSdRoutingTransportManagementVrfInterfaceEthernetPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
