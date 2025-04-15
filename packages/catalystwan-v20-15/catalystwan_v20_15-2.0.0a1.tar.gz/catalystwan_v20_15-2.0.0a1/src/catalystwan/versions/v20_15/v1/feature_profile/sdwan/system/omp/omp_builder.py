# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateOmpProfileParcelForSystemPostRequest,
    CreateOmpProfileParcelForSystemPostResponse,
    EditOmpProfileParcelForSystemPutRequest,
    EditOmpProfileParcelForSystemPutResponse,
    GetListSdwanSystemOmpPayload,
    GetSingleSdwanSystemOmpPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class OmpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/system/omp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateOmpProfileParcelForSystemPostRequest, **kw
    ) -> CreateOmpProfileParcelForSystemPostResponse:
        """
        Create a Omp Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/sdwan/system/{systemId}/omp

        :param system_id: Feature Profile ID
        :param payload: Omp Profile Parcel
        :returns: CreateOmpProfileParcelForSystemPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/omp",
            return_type=CreateOmpProfileParcelForSystemPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, omp_id: str, payload: EditOmpProfileParcelForSystemPutRequest, **kw
    ) -> EditOmpProfileParcelForSystemPutResponse:
        """
        Update a Omp Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/sdwan/system/{systemId}/omp/{ompId}

        :param system_id: Feature Profile ID
        :param omp_id: Profile Parcel ID
        :param payload: Omp Profile Parcel
        :returns: EditOmpProfileParcelForSystemPutResponse
        """
        params = {
            "systemId": system_id,
            "ompId": omp_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/omp/{ompId}",
            return_type=EditOmpProfileParcelForSystemPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, omp_id: str, **kw):
        """
        Delete a Omp Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/system/{systemId}/omp/{ompId}

        :param system_id: Feature Profile ID
        :param omp_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "ompId": omp_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/omp/{ompId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, omp_id: str, **kw) -> GetSingleSdwanSystemOmpPayload:
        """
        Get Omp Profile Parcel by parcelId for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/omp/{ompId}

        :param system_id: Feature Profile ID
        :param omp_id: Profile Parcel ID
        :returns: GetSingleSdwanSystemOmpPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdwanSystemOmpPayload:
        """
        Get Omp Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/omp

        :param system_id: Feature Profile ID
        :returns: GetListSdwanSystemOmpPayload
        """
        ...

    def get(
        self, system_id: str, omp_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanSystemOmpPayload, GetSingleSdwanSystemOmpPayload]:
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/omp/{ompId}
        if self._request_adapter.param_checker([(system_id, str), (omp_id, str)], []):
            params = {
                "systemId": system_id,
                "ompId": omp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/omp/{ompId}",
                return_type=GetSingleSdwanSystemOmpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/omp
        if self._request_adapter.param_checker([(system_id, str)], [omp_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/omp",
                return_type=GetListSdwanSystemOmpPayload,
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
