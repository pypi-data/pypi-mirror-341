# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CedgeServiceProfileSwitchportParcelRestfulResourcePostRequest,
    CedgeServiceProfileSwitchportParcelRestfulResourcePostResponse,
    EditSwitchportParcelAssociationForServicePutRequest,
    EditSwitchportParcelAssociationForServicePutResponse,
    GetListSdwanServiceSwitchportPayload,
    GetSingleSdwanServiceSwitchportPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class SwitchportBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/switchport
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        payload: CedgeServiceProfileSwitchportParcelRestfulResourcePostRequest,
        **kw,
    ) -> CedgeServiceProfileSwitchportParcelRestfulResourcePostResponse:
        """
        Create a switchport Parcel to a service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/switchport

        :param service_id: Feature Profile ID
        :param payload: Feature Profile Id
        :returns: CedgeServiceProfileSwitchportParcelRestfulResourcePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/switchport",
            return_type=CedgeServiceProfileSwitchportParcelRestfulResourcePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        switchport_id: str,
        payload: EditSwitchportParcelAssociationForServicePutRequest,
        **kw,
    ) -> EditSwitchportParcelAssociationForServicePutResponse:
        """
        Update a Switchport Parcel association for service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/switchport/{switchportId}

        :param service_id: Feature Profile ID
        :param switchport_id: Switchport ID
        :param payload: Switchport Profile Parcel
        :returns: EditSwitchportParcelAssociationForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "switchportId": switchport_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/switchport/{switchportId}",
            return_type=EditSwitchportParcelAssociationForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, switchport_id: str, **kw):
        """
        Delete a Switchport Parcel for service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/switchport/{switchportId}

        :param service_id: Feature Profile ID
        :param switchport_id: Switchport Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "switchportId": switchport_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/switchport/{switchportId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, switchport_id: str, **kw
    ) -> GetSingleSdwanServiceSwitchportPayload:
        """
        Get Switchport Parcel by switchportId for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/switchport/{switchportId}

        :param service_id: Feature Profile ID
        :param switchport_id: Switchport Parcel ID
        :returns: GetSingleSdwanServiceSwitchportPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdwanServiceSwitchportPayload:
        """
        Get Switchport Parcels for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/switchport

        :param service_id: Feature Profile ID
        :returns: GetListSdwanServiceSwitchportPayload
        """
        ...

    def get(
        self, service_id: str, switchport_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanServiceSwitchportPayload, GetSingleSdwanServiceSwitchportPayload]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/switchport/{switchportId}
        if self._request_adapter.param_checker([(service_id, str), (switchport_id, str)], []):
            params = {
                "serviceId": service_id,
                "switchportId": switchport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/switchport/{switchportId}",
                return_type=GetSingleSdwanServiceSwitchportPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/switchport
        if self._request_adapter.param_checker([(service_id, str)], [switchport_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/switchport",
                return_type=GetListSdwanServiceSwitchportPayload,
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
