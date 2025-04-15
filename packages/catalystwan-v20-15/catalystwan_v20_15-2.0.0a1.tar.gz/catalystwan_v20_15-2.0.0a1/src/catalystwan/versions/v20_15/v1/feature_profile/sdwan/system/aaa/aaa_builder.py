# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateAaaProfileParcelForSystemPostRequest,
    CreateAaaProfileParcelForSystemPostResponse,
    EditAaaProfileParcelForSystemPutRequest,
    EditAaaProfileParcelForSystemPutResponse,
    GetListSdwanSystemAaaPayload,
    GetSingleSdwanSystemAaaPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class AaaBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/system/aaa
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateAaaProfileParcelForSystemPostRequest, **kw
    ) -> CreateAaaProfileParcelForSystemPostResponse:
        """
        Create a Aaa Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/sdwan/system/{systemId}/aaa

        :param system_id: Feature Profile ID
        :param payload: Aaa Profile Parcel
        :returns: CreateAaaProfileParcelForSystemPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/aaa",
            return_type=CreateAaaProfileParcelForSystemPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, system_id: str, aaa_id: str, payload: EditAaaProfileParcelForSystemPutRequest, **kw
    ) -> EditAaaProfileParcelForSystemPutResponse:
        """
        Update a Aaa Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/sdwan/system/{systemId}/aaa/{aaaId}

        :param system_id: Feature Profile ID
        :param aaa_id: Profile Parcel ID
        :param payload: Aaa Profile Parcel
        :returns: EditAaaProfileParcelForSystemPutResponse
        """
        params = {
            "systemId": system_id,
            "aaaId": aaa_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/aaa/{aaaId}",
            return_type=EditAaaProfileParcelForSystemPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, aaa_id: str, **kw):
        """
        Delete a Aaa Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/system/{systemId}/aaa/{aaaId}

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
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/aaa/{aaaId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, aaa_id: str, **kw) -> GetSingleSdwanSystemAaaPayload:
        """
        Get Aaa Profile Parcel by parcelId for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/aaa/{aaaId}

        :param system_id: Feature Profile ID
        :param aaa_id: Profile Parcel ID
        :returns: GetSingleSdwanSystemAaaPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdwanSystemAaaPayload:
        """
        Get Aaa Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/aaa

        :param system_id: Feature Profile ID
        :returns: GetListSdwanSystemAaaPayload
        """
        ...

    def get(
        self, system_id: str, aaa_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanSystemAaaPayload, GetSingleSdwanSystemAaaPayload]:
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/aaa/{aaaId}
        if self._request_adapter.param_checker([(system_id, str), (aaa_id, str)], []):
            params = {
                "systemId": system_id,
                "aaaId": aaa_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/aaa/{aaaId}",
                return_type=GetSingleSdwanSystemAaaPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/aaa
        if self._request_adapter.param_checker([(system_id, str)], [aaa_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/aaa",
                return_type=GetListSdwanSystemAaaPayload,
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
