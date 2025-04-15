# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualSnmpParcelPostRequest,
    CreateNfvirtualSnmpParcelPostResponse,
    EditNfvirtualSnmpParcelPutRequest,
    EditNfvirtualSnmpParcelPutResponse,
    GetSingleNfvirtualSystemSnmpPayload,
)


class SnmpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/system/{systemId}/snmp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateNfvirtualSnmpParcelPostRequest, **kw
    ) -> CreateNfvirtualSnmpParcelPostResponse:
        """
        Create SNMP Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/snmp

        :param system_id: Feature Profile ID
        :param payload: SNMP config Profile Parcel
        :returns: CreateNfvirtualSnmpParcelPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/snmp",
            return_type=CreateNfvirtualSnmpParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(self, system_id: str, snmp_id: str, **kw) -> GetSingleNfvirtualSystemSnmpPayload:
        """
        Get SNMP Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/snmp/{snmpId}

        :param system_id: Feature Profile ID
        :param snmp_id: Profile Parcel ID
        :returns: GetSingleNfvirtualSystemSnmpPayload
        """
        params = {
            "systemId": system_id,
            "snmpId": snmp_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/snmp/{snmpId}",
            return_type=GetSingleNfvirtualSystemSnmpPayload,
            params=params,
            **kw,
        )

    def put(
        self, system_id: str, snmp_id: str, payload: EditNfvirtualSnmpParcelPutRequest, **kw
    ) -> EditNfvirtualSnmpParcelPutResponse:
        """
        Edit a  SNMP Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/snmp/{snmpId}

        :param system_id: Feature Profile ID
        :param snmp_id: Profile Parcel ID
        :param payload: SNMP Profile Parcel
        :returns: EditNfvirtualSnmpParcelPutResponse
        """
        params = {
            "systemId": system_id,
            "snmpId": snmp_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/snmp/{snmpId}",
            return_type=EditNfvirtualSnmpParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, snmp_id: str, **kw):
        """
        Delete a SNMP Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/snmp/{snmpId}

        :param system_id: Feature Profile ID
        :param snmp_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "snmpId": snmp_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/snmp/{snmpId}",
            params=params,
            **kw,
        )
