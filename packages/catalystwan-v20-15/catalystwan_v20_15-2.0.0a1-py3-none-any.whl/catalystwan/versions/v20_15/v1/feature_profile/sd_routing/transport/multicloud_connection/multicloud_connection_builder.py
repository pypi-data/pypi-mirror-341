# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateMultiCloudConnection1PostRequest,
    CreateMultiCloudConnection1PostResponse,
    EditMultiCloudConnection1PutRequest,
    EditMultiCloudConnection1PutResponse,
    GetListSdRoutingTransportVrfWanMulticloudConnectionPayload,
    GetSingleSdRoutingTransportVrfWanMulticloudConnectionPayload,
)


class MulticloudConnectionBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/multicloud-connection
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, transport_id: str, payload: CreateMultiCloudConnection1PostRequest, **kw
    ) -> CreateMultiCloudConnection1PostResponse:
        """
        Associate a MultiCloudConnection Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/multicloud-connection

        :param transport_id: Feature Profile ID
        :param payload: MultiConnection Extension Payload for defining the multicloud connection to the cloud gateway
        :returns: CreateMultiCloudConnection1PostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/multicloud-connection",
            return_type=CreateMultiCloudConnection1PostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        multi_cloud_connection_id: str,
        payload: EditMultiCloudConnection1PutRequest,
        **kw,
    ) -> EditMultiCloudConnection1PutResponse:
        """
        Update a multicloud connection parcel
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/multicloud-connection/{multiCloudConnectionId}

        :param transport_id: Feature Profile ID
        :param multi_cloud_connection_id: Profile Parcel ID
        :param payload: Multicloud Connection Profile Parcel
        :returns: EditMultiCloudConnection1PutResponse
        """
        params = {
            "transportId": transport_id,
            "multiCloudConnectionId": multi_cloud_connection_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/multicloud-connection/{multiCloudConnectionId}",
            return_type=EditMultiCloudConnection1PutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, multi_cloud_connection_id: str, **kw):
        """
        Delete a MultiCloud Connection Profile Parcel for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/multicloud-connection/{multiCloudConnectionId}

        :param transport_id: Feature Profile ID
        :param multi_cloud_connection_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "multiCloudConnectionId": multi_cloud_connection_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/multicloud-connection/{multiCloudConnectionId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, multi_cloud_connection_id: str, **kw
    ) -> GetSingleSdRoutingTransportVrfWanMulticloudConnectionPayload:
        """
        Get Lan Vpn Profile Parcel by parcelId for Service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/multicloud-connection/{multiCloudConnectionId}

        :param transport_id: Feature Profile ID
        :param multi_cloud_connection_id: Profile Parcel ID
        :returns: GetSingleSdRoutingTransportVrfWanMulticloudConnectionPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, **kw
    ) -> GetListSdRoutingTransportVrfWanMulticloudConnectionPayload:
        """
        Get Lan Vpn Profile Parcels for Service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/multicloud-connection

        :param transport_id: Feature Profile ID
        :returns: GetListSdRoutingTransportVrfWanMulticloudConnectionPayload
        """
        ...

    def get(
        self, transport_id: str, multi_cloud_connection_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportVrfWanMulticloudConnectionPayload,
        GetSingleSdRoutingTransportVrfWanMulticloudConnectionPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/multicloud-connection/{multiCloudConnectionId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (multi_cloud_connection_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "multiCloudConnectionId": multi_cloud_connection_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/multicloud-connection/{multiCloudConnectionId}",
                return_type=GetSingleSdRoutingTransportVrfWanMulticloudConnectionPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/multicloud-connection
        if self._request_adapter.param_checker([(transport_id, str)], [multi_cloud_connection_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/multicloud-connection",
                return_type=GetListSdRoutingTransportVrfWanMulticloudConnectionPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
