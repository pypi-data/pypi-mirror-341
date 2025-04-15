# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateMrfProfileParcelForSystemPostRequest,
    CreateMrfProfileParcelForSystemPostResponse,
    EditMrfProfileParcelForSystemPutRequest,
    EditMrfProfileParcelForSystemPutResponse,
    GetListSdwanSystemMrfPayload,
    GetSingleSdwanSystemMrfPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class MrfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/system/mrf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateMrfProfileParcelForSystemPostRequest, **kw
    ) -> CreateMrfProfileParcelForSystemPostResponse:
        """
        Create a Mrf Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/sdwan/system/{systemId}/mrf

        :param system_id: Feature Profile ID
        :param payload: Mrf Profile Parcel
        :returns: CreateMrfProfileParcelForSystemPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/mrf",
            return_type=CreateMrfProfileParcelForSystemPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, mrf_id: str, payload: EditMrfProfileParcelForSystemPutRequest, **kw
    ) -> EditMrfProfileParcelForSystemPutResponse:
        """
        Update a Mrf Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/sdwan/system/{systemId}/mrf/{mrfId}

        :param system_id: Feature Profile ID
        :param mrf_id: Profile Parcel ID
        :param payload: Mrf Profile Parcel
        :returns: EditMrfProfileParcelForSystemPutResponse
        """
        params = {
            "systemId": system_id,
            "mrfId": mrf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/mrf/{mrfId}",
            return_type=EditMrfProfileParcelForSystemPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, mrf_id: str, **kw):
        """
        Delete a Mrf Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/system/{systemId}/mrf/{mrfId}

        :param system_id: Feature Profile ID
        :param mrf_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "mrfId": mrf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/mrf/{mrfId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, mrf_id: str, **kw) -> GetSingleSdwanSystemMrfPayload:
        """
        Get Mrf Profile Parcel by parcelId for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/mrf/{mrfId}

        :param system_id: Feature Profile ID
        :param mrf_id: Profile Parcel ID
        :returns: GetSingleSdwanSystemMrfPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdwanSystemMrfPayload:
        """
        Get Mrf Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/mrf

        :param system_id: Feature Profile ID
        :returns: GetListSdwanSystemMrfPayload
        """
        ...

    def get(
        self, system_id: str, mrf_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanSystemMrfPayload, GetSingleSdwanSystemMrfPayload]:
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/mrf/{mrfId}
        if self._request_adapter.param_checker([(system_id, str), (mrf_id, str)], []):
            params = {
                "systemId": system_id,
                "mrfId": mrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/mrf/{mrfId}",
                return_type=GetSingleSdwanSystemMrfPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/mrf
        if self._request_adapter.param_checker([(system_id, str)], [mrf_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/mrf",
                return_type=GetListSdwanSystemMrfPayload,
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
