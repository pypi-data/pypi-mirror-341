# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateManagementVpnProfileParcelForTransportPostRequest,
    CreateManagementVpnProfileParcelForTransportPostResponse,
    EditManagementVpnProfileParcelForTransportPutRequest,
    EditManagementVpnProfileParcelForTransportPutResponse,
    GetListSdwanTransportManagementVpnPayload,
    GetSingleSdwanTransportManagementVpnPayload,
)

if TYPE_CHECKING:
    from .interface.interface_builder import InterfaceBuilder
    from .schema.schema_builder import SchemaBuilder


class VpnBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/management/vpn
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateManagementVpnProfileParcelForTransportPostRequest,
        **kw,
    ) -> CreateManagementVpnProfileParcelForTransportPostResponse:
        """
        Create a Management Vpn Profile Parcel for Transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn

        :param transport_id: Feature Profile ID
        :param payload: Management Vpn Profile Parcel
        :returns: CreateManagementVpnProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn",
            return_type=CreateManagementVpnProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        payload: EditManagementVpnProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditManagementVpnProfileParcelForTransportPutResponse:
        """
        Update a Management Vpn Profile Parcel for Transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param payload: Management Vpn Profile Parcel
        :returns: EditManagementVpnProfileParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}",
            return_type=EditManagementVpnProfileParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, **kw):
        """
        Delete a Management Vpn Profile Parcel for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, **kw
    ) -> GetSingleSdwanTransportManagementVpnPayload:
        """
        Get Management Vpn Profile Parcel by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :returns: GetSingleSdwanTransportManagementVpnPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportManagementVpnPayload:
        """
        Get Management Vpn Profile Parcels for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportManagementVpnPayload
        """
        ...

    def get(
        self, transport_id: str, vpn_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportManagementVpnPayload, GetSingleSdwanTransportManagementVpnPayload
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}
        if self._request_adapter.param_checker([(transport_id, str), (vpn_id, str)], []):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn/{vpnId}",
                return_type=GetSingleSdwanTransportManagementVpnPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn
        if self._request_adapter.param_checker([(transport_id, str)], [vpn_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/management/vpn",
                return_type=GetListSdwanTransportManagementVpnPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)
