# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualLoggingParcelPostRequest,
    CreateNfvirtualLoggingParcelPostResponse,
    EditNfvirtualLoggingParcelPutRequest,
    EditNfvirtualLoggingParcelPutResponse,
    GetSingleNfvirtualSystemLoggingPayload,
)


class LoggingBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/system/{systemId}/logging
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateNfvirtualLoggingParcelPostRequest, **kw
    ) -> CreateNfvirtualLoggingParcelPostResponse:
        """
        Create Logging Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/logging

        :param system_id: Feature Profile ID
        :param payload: Logging config Profile Parcel
        :returns: CreateNfvirtualLoggingParcelPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/logging",
            return_type=CreateNfvirtualLoggingParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(self, system_id: str, logging_id: str, **kw) -> GetSingleNfvirtualSystemLoggingPayload:
        """
        Get Logging Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/logging/{loggingId}

        :param system_id: Feature Profile ID
        :param logging_id: Profile Parcel ID
        :returns: GetSingleNfvirtualSystemLoggingPayload
        """
        params = {
            "systemId": system_id,
            "loggingId": logging_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/logging/{loggingId}",
            return_type=GetSingleNfvirtualSystemLoggingPayload,
            params=params,
            **kw,
        )

    def put(
        self, system_id: str, logging_id: str, payload: EditNfvirtualLoggingParcelPutRequest, **kw
    ) -> EditNfvirtualLoggingParcelPutResponse:
        """
        Edit a  Logging Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/logging/{loggingId}

        :param system_id: Feature Profile ID
        :param logging_id: Profile Parcel ID
        :param payload: Logging Profile Parcel
        :returns: EditNfvirtualLoggingParcelPutResponse
        """
        params = {
            "systemId": system_id,
            "loggingId": logging_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/logging/{loggingId}",
            return_type=EditNfvirtualLoggingParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, logging_id: str, **kw):
        """
        Delete a Logging Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/system/{systemId}/logging/{loggingId}

        :param system_id: Feature Profile ID
        :param logging_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "loggingId": logging_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/system/{systemId}/logging/{loggingId}",
            params=params,
            **kw,
        )
