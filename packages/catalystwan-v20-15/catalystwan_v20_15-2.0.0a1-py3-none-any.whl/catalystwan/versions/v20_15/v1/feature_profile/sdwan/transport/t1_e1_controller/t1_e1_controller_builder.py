# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateT1E1ControllerProfileParcelForTransportPostRequest,
    CreateT1E1ControllerProfileParcelForTransportPostResponse,
    EditT1E1ControllerProfileParcelForTransportPutRequest,
    EditT1E1ControllerProfileParcelForTransportPutResponse,
    GetListSdwanTransportT1E1ControllerPayload,
    GetSingleSdwanTransportT1E1ControllerPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class T1E1ControllerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/t1-e1-controller
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateT1E1ControllerProfileParcelForTransportPostRequest,
        **kw,
    ) -> CreateT1E1ControllerProfileParcelForTransportPostResponse:
        """
        Create a T1e1controller Profile Parcel for Transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/t1-e1-controller

        :param transport_id: Feature Profile ID
        :param payload: T1e1controller Profile Parcel
        :returns: CreateT1E1ControllerProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/t1-e1-controller",
            return_type=CreateT1E1ControllerProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        t1e1controller_id: str,
        payload: EditT1E1ControllerProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditT1E1ControllerProfileParcelForTransportPutResponse:
        """
        Update a T1e1controller Profile Parcel for Transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/t1-e1-controller/{t1e1controllerId}

        :param transport_id: Feature Profile ID
        :param t1e1controller_id: Profile Parcel ID
        :param payload: T1e1controller Profile Parcel
        :returns: EditT1E1ControllerProfileParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "t1e1controllerId": t1e1controller_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/t1-e1-controller/{t1e1controllerId}",
            return_type=EditT1E1ControllerProfileParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, t1e1controller_id: str, **kw):
        """
        Delete a T1e1controller Profile Parcel for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/t1-e1-controller/{t1e1controllerId}

        :param transport_id: Feature Profile ID
        :param t1e1controller_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "t1e1controllerId": t1e1controller_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/t1-e1-controller/{t1e1controllerId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, t1e1controller_id: str, **kw
    ) -> GetSingleSdwanTransportT1E1ControllerPayload:
        """
        Get T1e1controller Profile Parcel by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/t1-e1-controller/{t1e1controllerId}

        :param transport_id: Feature Profile ID
        :param t1e1controller_id: Profile Parcel ID
        :returns: GetSingleSdwanTransportT1E1ControllerPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportT1E1ControllerPayload:
        """
        Get T1e1controller Profile Parcels for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/t1-e1-controller

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportT1E1ControllerPayload
        """
        ...

    def get(
        self, transport_id: str, t1e1controller_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportT1E1ControllerPayload, GetSingleSdwanTransportT1E1ControllerPayload
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/t1-e1-controller/{t1e1controllerId}
        if self._request_adapter.param_checker([(transport_id, str), (t1e1controller_id, str)], []):
            params = {
                "transportId": transport_id,
                "t1e1controllerId": t1e1controller_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/t1-e1-controller/{t1e1controllerId}",
                return_type=GetSingleSdwanTransportT1E1ControllerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/t1-e1-controller
        if self._request_adapter.param_checker([(transport_id, str)], [t1e1controller_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/t1-e1-controller",
                return_type=GetListSdwanTransportT1E1ControllerPayload,
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
