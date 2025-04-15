# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateBfdProfileParcelForSystemPostRequest,
    CreateBfdProfileParcelForSystemPostResponse,
    EditBfdProfileParcelForSystemPutRequest,
    EditBfdProfileParcelForSystemPutResponse,
    GetListSdwanSystemBfdPayload,
    GetSingleSdwanSystemBfdPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class BfdBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/system/bfd
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateBfdProfileParcelForSystemPostRequest, **kw
    ) -> CreateBfdProfileParcelForSystemPostResponse:
        """
        Create a Bfd Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/sdwan/system/{systemId}/bfd

        :param system_id: Feature Profile ID
        :param payload: Bfd Profile Parcel
        :returns: CreateBfdProfileParcelForSystemPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/bfd",
            return_type=CreateBfdProfileParcelForSystemPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, bfd_id: str, payload: EditBfdProfileParcelForSystemPutRequest, **kw
    ) -> EditBfdProfileParcelForSystemPutResponse:
        """
        Update a Bfd Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/sdwan/system/{systemId}/bfd/{bfdId}

        :param system_id: Feature Profile ID
        :param bfd_id: Profile Parcel ID
        :param payload: Bfd Profile Parcel
        :returns: EditBfdProfileParcelForSystemPutResponse
        """
        params = {
            "systemId": system_id,
            "bfdId": bfd_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/bfd/{bfdId}",
            return_type=EditBfdProfileParcelForSystemPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, bfd_id: str, **kw):
        """
        Delete a Bfd Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/system/{systemId}/bfd/{bfdId}

        :param system_id: Feature Profile ID
        :param bfd_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "bfdId": bfd_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/bfd/{bfdId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, bfd_id: str, **kw) -> GetSingleSdwanSystemBfdPayload:
        """
        Get Bfd Profile Parcel by parcelId for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/bfd/{bfdId}

        :param system_id: Feature Profile ID
        :param bfd_id: Profile Parcel ID
        :returns: GetSingleSdwanSystemBfdPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdwanSystemBfdPayload:
        """
        Get Bfd Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/bfd

        :param system_id: Feature Profile ID
        :returns: GetListSdwanSystemBfdPayload
        """
        ...

    def get(
        self, system_id: str, bfd_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanSystemBfdPayload, GetSingleSdwanSystemBfdPayload]:
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/bfd/{bfdId}
        if self._request_adapter.param_checker([(system_id, str), (bfd_id, str)], []):
            params = {
                "systemId": system_id,
                "bfdId": bfd_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/bfd/{bfdId}",
                return_type=GetSingleSdwanSystemBfdPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/bfd
        if self._request_adapter.param_checker([(system_id, str)], [bfd_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/bfd",
                return_type=GetListSdwanSystemBfdPayload,
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
