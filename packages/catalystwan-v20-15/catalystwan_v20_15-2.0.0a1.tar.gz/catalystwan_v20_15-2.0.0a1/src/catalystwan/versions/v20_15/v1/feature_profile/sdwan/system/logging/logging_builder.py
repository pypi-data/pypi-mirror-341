# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLoggingProfileParcelForSystemPostRequest,
    CreateLoggingProfileParcelForSystemPostResponse,
    EditLoggingProfileParcelForSystemPutRequest,
    EditLoggingProfileParcelForSystemPutResponse,
    GetListSdwanSystemLoggingPayload,
    GetSingleSdwanSystemLoggingPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class LoggingBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/system/logging
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateLoggingProfileParcelForSystemPostRequest, **kw
    ) -> CreateLoggingProfileParcelForSystemPostResponse:
        """
        Create a Logging Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/sdwan/system/{systemId}/logging

        :param system_id: Feature Profile ID
        :param payload: Logging Profile Parcel
        :returns: CreateLoggingProfileParcelForSystemPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/logging",
            return_type=CreateLoggingProfileParcelForSystemPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        system_id: str,
        logging_id: str,
        payload: EditLoggingProfileParcelForSystemPutRequest,
        **kw,
    ) -> EditLoggingProfileParcelForSystemPutResponse:
        """
        Update a Logging Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/sdwan/system/{systemId}/logging/{loggingId}

        :param system_id: Feature Profile ID
        :param logging_id: Profile Parcel ID
        :param payload: Logging Profile Parcel
        :returns: EditLoggingProfileParcelForSystemPutResponse
        """
        params = {
            "systemId": system_id,
            "loggingId": logging_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/logging/{loggingId}",
            return_type=EditLoggingProfileParcelForSystemPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, logging_id: str, **kw):
        """
        Delete a Logging Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/system/{systemId}/logging/{loggingId}

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
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/logging/{loggingId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, logging_id: str, **kw) -> GetSingleSdwanSystemLoggingPayload:
        """
        Get Logging Profile Parcel by parcelId for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/logging/{loggingId}

        :param system_id: Feature Profile ID
        :param logging_id: Profile Parcel ID
        :returns: GetSingleSdwanSystemLoggingPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdwanSystemLoggingPayload:
        """
        Get Logging Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/logging

        :param system_id: Feature Profile ID
        :returns: GetListSdwanSystemLoggingPayload
        """
        ...

    def get(
        self, system_id: str, logging_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanSystemLoggingPayload, GetSingleSdwanSystemLoggingPayload]:
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/logging/{loggingId}
        if self._request_adapter.param_checker([(system_id, str), (logging_id, str)], []):
            params = {
                "systemId": system_id,
                "loggingId": logging_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/logging/{loggingId}",
                return_type=GetSingleSdwanSystemLoggingPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/logging
        if self._request_adapter.param_checker([(system_id, str)], [logging_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/logging",
                return_type=GetListSdwanSystemLoggingPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)
