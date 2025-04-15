# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingSnmpFeaturePostRequest,
    CreateSdroutingSnmpFeaturePostResponse,
    EditSdroutingSnmpFeaturePutRequest,
    EditSdroutingSnmpFeaturePutResponse,
    GetListSdRoutingSystemSnmpSdRoutingPayload,
    GetSingleSdRoutingSystemSnmpSdRoutingPayload,
)


class SnmpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/system/{systemId}/snmp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateSdroutingSnmpFeaturePostRequest, **kw
    ) -> CreateSdroutingSnmpFeaturePostResponse:
        """
        Create a SD-Routing SNMP Feature for System Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/system/{systemId}/snmp

        :param system_id: System Profile ID
        :param payload: SD-Routing SNMP Feature for System Feature Profile
        :returns: CreateSdroutingSnmpFeaturePostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/snmp",
            return_type=CreateSdroutingSnmpFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, snmp_id: str, payload: EditSdroutingSnmpFeaturePutRequest, **kw
    ) -> EditSdroutingSnmpFeaturePutResponse:
        """
        Edit a SD-Routing SNMP Feature for System Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/system/{systemId}/snmp/{snmpId}

        :param system_id: System Profile ID
        :param snmp_id: SNMP Feature ID
        :param payload: SD-Routing SNMP Feature for System Feature Profile
        :returns: EditSdroutingSnmpFeaturePutResponse
        """
        params = {
            "systemId": system_id,
            "snmpId": snmp_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/snmp/{snmpId}",
            return_type=EditSdroutingSnmpFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, snmp_id: str, **kw):
        """
        Delete a SD-Routing SNMP Feature for System Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/system/{systemId}/snmp/{snmpId}

        :param system_id: System Profile ID
        :param snmp_id: SNMP Feature ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "snmpId": snmp_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/snmp/{snmpId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, system_id: str, snmp_id: str, **kw
    ) -> GetSingleSdRoutingSystemSnmpSdRoutingPayload:
        """
        Get a SD-Routing SNMP Feature for System Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/snmp/{snmpId}

        :param system_id: System Profile ID
        :param snmp_id: SNMP Feature ID
        :returns: GetSingleSdRoutingSystemSnmpSdRoutingPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdRoutingSystemSnmpSdRoutingPayload:
        """
        Get all SD-Routing SNMP Features for System Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/system/{systemId}/snmp

        :param system_id: System Profile ID
        :returns: GetListSdRoutingSystemSnmpSdRoutingPayload
        """
        ...

    def get(
        self, system_id: str, snmp_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingSystemSnmpSdRoutingPayload, GetSingleSdRoutingSystemSnmpSdRoutingPayload
    ]:
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/snmp/{snmpId}
        if self._request_adapter.param_checker([(system_id, str), (snmp_id, str)], []):
            params = {
                "systemId": system_id,
                "snmpId": snmp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/snmp/{snmpId}",
                return_type=GetSingleSdRoutingSystemSnmpSdRoutingPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/system/{systemId}/snmp
        if self._request_adapter.param_checker([(system_id, str)], [snmp_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/system/{systemId}/snmp",
                return_type=GetListSdRoutingSystemSnmpSdRoutingPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
