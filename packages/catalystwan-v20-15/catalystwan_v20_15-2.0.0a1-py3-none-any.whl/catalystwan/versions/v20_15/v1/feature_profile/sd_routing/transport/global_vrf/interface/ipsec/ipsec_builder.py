# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportGlobalVrfInterfaceIpsecFeatureForTransportPostRequest,
    CreateSdroutingTransportGlobalVrfInterfaceIpsecFeatureForTransportPostResponse,
    EditSdroutingTransportGlobalVrfInterfaceIpsecFeatureForTransportPutRequest,
    EditSdroutingTransportGlobalVrfInterfaceIpsecFeatureForTransportPutResponse,
    GetListSdRoutingTransportGlobalVrfWanInterfaceIpsecPayload,
    GetSingleSdRoutingTransportGlobalVrfWanInterfaceIpsecPayload,
)


class IpsecBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ipsec
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vrf_id: str,
        payload: CreateSdroutingTransportGlobalVrfInterfaceIpsecFeatureForTransportPostRequest,
        **kw,
    ) -> CreateSdroutingTransportGlobalVrfInterfaceIpsecFeatureForTransportPostResponse:
        """
        Create a SD-Routing Ipsec Interface Feature for Global VRF in Transport Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ipsec

        :param transport_id: Transport Profile ID
        :param vrf_id: Transport Global VRF Feature ID
        :param payload:  Ipsec Interface Feature for Global VRF in Transport Feature Profile
        :returns: CreateSdroutingTransportGlobalVrfInterfaceIpsecFeatureForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ipsec",
            return_type=CreateSdroutingTransportGlobalVrfInterfaceIpsecFeatureForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vrf_id: str,
        ipsec_id: str,
        payload: EditSdroutingTransportGlobalVrfInterfaceIpsecFeatureForTransportPutRequest,
        **kw,
    ) -> EditSdroutingTransportGlobalVrfInterfaceIpsecFeatureForTransportPutResponse:
        """
        Edit a SD-Routing Ipsec Interface Feature for Global VRF in Transport Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ipsec/{ipsecId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Transport Global VRF Feature ID
        :param ipsec_id: Interface Ipsec Feature ID
        :param payload:  Ipsec Interface Feature for Global VRF in Transport Feature Profile
        :returns: EditSdroutingTransportGlobalVrfInterfaceIpsecFeatureForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ipsecId": ipsec_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ipsec/{ipsecId}",
            return_type=EditSdroutingTransportGlobalVrfInterfaceIpsecFeatureForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vrf_id: str, ipsec_id: str, **kw):
        """
        Delete a SD-Routing Ipsec Interface Feature for Global VRF in Transport Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ipsec/{ipsecId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Transport Global VRF Feature ID
        :param ipsec_id: Interface Ipsec Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ipsecId": ipsec_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ipsec/{ipsecId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vrf_id: str, ipsec_id: str, **kw
    ) -> GetSingleSdRoutingTransportGlobalVrfWanInterfaceIpsecPayload:
        """
        Get a SD-Routing Ipsec Interface Feature for Global VRF in Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ipsec/{ipsecId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Transport Global VRF Feature ID
        :param ipsec_id: Interface Ipsec Feature ID
        :returns: GetSingleSdRoutingTransportGlobalVrfWanInterfaceIpsecPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vrf_id: str, **kw
    ) -> GetListSdRoutingTransportGlobalVrfWanInterfaceIpsecPayload:
        """
        Get all  Ipsec Interface Features for Global VRF in Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ipsec

        :param transport_id: Transport Profile ID
        :param vrf_id: Transport Global VRF Feature ID
        :returns: GetListSdRoutingTransportGlobalVrfWanInterfaceIpsecPayload
        """
        ...

    def get(
        self, transport_id: str, vrf_id: str, ipsec_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportGlobalVrfWanInterfaceIpsecPayload,
        GetSingleSdRoutingTransportGlobalVrfWanInterfaceIpsecPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ipsec/{ipsecId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vrf_id, str), (ipsec_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
                "ipsecId": ipsec_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ipsec/{ipsecId}",
                return_type=GetSingleSdRoutingTransportGlobalVrfWanInterfaceIpsecPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ipsec
        if self._request_adapter.param_checker([(transport_id, str), (vrf_id, str)], [ipsec_id]):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/interface/ipsec",
                return_type=GetListSdRoutingTransportGlobalVrfWanInterfaceIpsecPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
