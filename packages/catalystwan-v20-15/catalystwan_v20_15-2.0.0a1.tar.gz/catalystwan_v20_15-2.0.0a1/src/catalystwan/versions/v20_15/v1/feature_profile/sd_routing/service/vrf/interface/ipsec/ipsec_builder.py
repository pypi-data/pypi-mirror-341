# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingServiceVrfInterfaceIpsecFeatureForServicePostRequest,
    CreateSdroutingServiceVrfInterfaceIpsecFeatureForServicePostResponse,
    EditSdroutingServiceVrfInterfaceIpsecFeatureForServicePutRequest,
    EditSdroutingServiceVrfInterfaceIpsecFeatureForServicePutResponse,
    GetListSdRoutingServiceVrfLanInterfaceIpsecPayload,
    GetSingleSdRoutingServiceVrfLanInterfaceIpsecPayload,
)


class IpsecBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ipsec
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vrf_id: str,
        payload: CreateSdroutingServiceVrfInterfaceIpsecFeatureForServicePostRequest,
        **kw,
    ) -> CreateSdroutingServiceVrfInterfaceIpsecFeatureForServicePostResponse:
        """
        Create a SD-Routing Ipsec Interface Feature for Service VRF in Service Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ipsec

        :param service_id: Service Profile ID
        :param vrf_id: Service VRF Feature ID
        :param payload:  Ipsec Interface Feature for Service VRF in Service Feature Profile
        :returns: CreateSdroutingServiceVrfInterfaceIpsecFeatureForServicePostResponse
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ipsec",
            return_type=CreateSdroutingServiceVrfInterfaceIpsecFeatureForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vrf_id: str,
        ipsec_id: str,
        payload: EditSdroutingServiceVrfInterfaceIpsecFeatureForServicePutRequest,
        **kw,
    ) -> EditSdroutingServiceVrfInterfaceIpsecFeatureForServicePutResponse:
        """
        Edit a SD-Routing Ipsec Interface Feature for Service VRF in Service Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ipsec/{ipsecId}

        :param service_id: Service Profile ID
        :param vrf_id: Service VRF Feature ID
        :param ipsec_id: Interface Ipsec Feature ID
        :param payload:  Ipsec Interface Feature for Service VRF in Service Feature Profile
        :returns: EditSdroutingServiceVrfInterfaceIpsecFeatureForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
            "ipsecId": ipsec_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ipsec/{ipsecId}",
            return_type=EditSdroutingServiceVrfInterfaceIpsecFeatureForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vrf_id: str, ipsec_id: str, **kw):
        """
        Delete a SD-Routing Ipsec Interface Feature for Service VRF in Service Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ipsec/{ipsecId}

        :param service_id: Service Profile ID
        :param vrf_id: Service VRF Feature ID
        :param ipsec_id: Interface Ipsec Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
            "ipsecId": ipsec_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ipsec/{ipsecId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vrf_id: str, ipsec_id: str, **kw
    ) -> GetSingleSdRoutingServiceVrfLanInterfaceIpsecPayload:
        """
        Get a SD-Routing Ipsec Interface Feature for Service VRF in Service Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ipsec/{ipsecId}

        :param service_id: Service Profile ID
        :param vrf_id: Service VRF Feature ID
        :param ipsec_id: Interface Ipsec Feature ID
        :returns: GetSingleSdRoutingServiceVrfLanInterfaceIpsecPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vrf_id: str, **kw
    ) -> GetListSdRoutingServiceVrfLanInterfaceIpsecPayload:
        """
        Get all  Ipsec Interface Features for Service VRF in Service Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ipsec

        :param service_id: Service Profile ID
        :param vrf_id: Service VRF feature ID
        :returns: GetListSdRoutingServiceVrfLanInterfaceIpsecPayload
        """
        ...

    def get(
        self, service_id: str, vrf_id: str, ipsec_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingServiceVrfLanInterfaceIpsecPayload,
        GetSingleSdRoutingServiceVrfLanInterfaceIpsecPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ipsec/{ipsecId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vrf_id, str), (ipsec_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
                "ipsecId": ipsec_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ipsec/{ipsecId}",
                return_type=GetSingleSdRoutingServiceVrfLanInterfaceIpsecPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ipsec
        if self._request_adapter.param_checker([(service_id, str), (vrf_id, str)], [ipsec_id]):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ipsec",
                return_type=GetListSdRoutingServiceVrfLanInterfaceIpsecPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
