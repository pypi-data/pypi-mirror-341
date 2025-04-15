# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualAaaParcelPostRequest,
    CreateNfvirtualAaaParcelPostResponse,
    EditNfvirtualAaaParcelPutRequest,
    EditNfvirtualAaaParcelPutResponse,
    GetSingleNfvirtualSystemAaaPayload,
)


class AaaBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/system/{systemId}/aaa
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateNfvirtualAaaParcelPostRequest, **kw
    ) -> CreateNfvirtualAaaParcelPostResponse:
        """
        Create AAA Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/aaa

        :param system_id: Feature Profile ID
        :param payload: AAA config Profile Parcel
        :returns: CreateNfvirtualAaaParcelPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/aaa",
            return_type=CreateNfvirtualAaaParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(self, system_id: str, aaa_id: str, **kw) -> GetSingleNfvirtualSystemAaaPayload:
        """
        Get AAA Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/aaa/{aaaId}

        :param system_id: Feature Profile ID
        :param aaa_id: Profile Parcel ID
        :returns: GetSingleNfvirtualSystemAaaPayload
        """
        params = {
            "systemId": system_id,
            "aaaId": aaa_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/aaa/{aaaId}",
            return_type=GetSingleNfvirtualSystemAaaPayload,
            params=params,
            **kw,
        )

    def put(
        self, system_id: str, aaa_id: str, payload: EditNfvirtualAaaParcelPutRequest, **kw
    ) -> EditNfvirtualAaaParcelPutResponse:
        """
        Edit a  AAA Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/aaa/{aaaId}

        :param system_id: Feature Profile ID
        :param aaa_id: Profile Parcel ID
        :param payload: AAA Profile Parcel
        :returns: EditNfvirtualAaaParcelPutResponse
        """
        params = {
            "systemId": system_id,
            "aaaId": aaa_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/aaa/{aaaId}",
            return_type=EditNfvirtualAaaParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, aaa_id: str, **kw):
        """
        Delete a AAA Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/aaa/{aaaId}

        :param system_id: Feature Profile ID
        :param aaa_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "aaaId": aaa_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/aaa/{aaaId}",
            params=params,
            **kw,
        )
