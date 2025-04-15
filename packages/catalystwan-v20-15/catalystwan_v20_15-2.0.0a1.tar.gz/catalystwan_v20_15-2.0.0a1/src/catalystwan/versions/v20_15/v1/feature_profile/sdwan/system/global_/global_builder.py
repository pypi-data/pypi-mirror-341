# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateGlobalProfileParcelForSystemPostRequest,
    CreateGlobalProfileParcelForSystemPostResponse,
    EditGlobalProfileParcelForSystemPutRequest,
    EditGlobalProfileParcelForSystemPutResponse,
    GetListSdwanSystemGlobalPayload,
    GetSingleSdwanSystemGlobalPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class GlobalBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/system/global
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, system_id: str, payload: CreateGlobalProfileParcelForSystemPostRequest, **kw
    ) -> CreateGlobalProfileParcelForSystemPostResponse:
        """
        Create a Global Profile Parcel for System feature profile
        POST /dataservice/v1/feature-profile/sdwan/system/{systemId}/global

        :param system_id: Feature Profile ID
        :param payload: Global Profile Parcel
        :returns: CreateGlobalProfileParcelForSystemPostResponse
        """
        params = {
            "systemId": system_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/global",
            return_type=CreateGlobalProfileParcelForSystemPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        system_id: str,
        global_id: str,
        payload: EditGlobalProfileParcelForSystemPutRequest,
        **kw,
    ) -> EditGlobalProfileParcelForSystemPutResponse:
        """
        Update a Global Profile Parcel for System feature profile
        PUT /dataservice/v1/feature-profile/sdwan/system/{systemId}/global/{globalId}

        :param system_id: Feature Profile ID
        :param global_id: Profile Parcel ID
        :param payload: Global Profile Parcel
        :returns: EditGlobalProfileParcelForSystemPutResponse
        """
        params = {
            "systemId": system_id,
            "globalId": global_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/global/{globalId}",
            return_type=EditGlobalProfileParcelForSystemPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, system_id: str, global_id: str, **kw):
        """
        Delete a Global Profile Parcel for System feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/system/{systemId}/global/{globalId}

        :param system_id: Feature Profile ID
        :param global_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "systemId": system_id,
            "globalId": global_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/system/{systemId}/global/{globalId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, system_id: str, global_id: str, **kw) -> GetSingleSdwanSystemGlobalPayload:
        """
        Get Global Profile Parcel by parcelId for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/global/{globalId}

        :param system_id: Feature Profile ID
        :param global_id: Profile Parcel ID
        :returns: GetSingleSdwanSystemGlobalPayload
        """
        ...

    @overload
    def get(self, system_id: str, **kw) -> GetListSdwanSystemGlobalPayload:
        """
        Get Global Profile Parcels for System feature profile
        GET /dataservice/v1/feature-profile/sdwan/system/{systemId}/global

        :param system_id: Feature Profile ID
        :returns: GetListSdwanSystemGlobalPayload
        """
        ...

    def get(
        self, system_id: str, global_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanSystemGlobalPayload, GetSingleSdwanSystemGlobalPayload]:
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/global/{globalId}
        if self._request_adapter.param_checker([(system_id, str), (global_id, str)], []):
            params = {
                "systemId": system_id,
                "globalId": global_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/global/{globalId}",
                return_type=GetSingleSdwanSystemGlobalPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/system/{systemId}/global
        if self._request_adapter.param_checker([(system_id, str)], [global_id]):
            params = {
                "systemId": system_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/system/{systemId}/global",
                return_type=GetListSdwanSystemGlobalPayload,
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
