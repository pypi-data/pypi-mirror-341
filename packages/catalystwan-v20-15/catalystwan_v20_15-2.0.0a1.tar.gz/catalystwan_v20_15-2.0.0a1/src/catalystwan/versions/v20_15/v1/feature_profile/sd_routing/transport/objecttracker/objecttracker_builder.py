# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportObjectTrackerFeaturePostRequest,
    CreateSdroutingTransportObjectTrackerFeaturePostResponse,
    EditSdroutingTransportObjectTrackerFeaturePutRequest,
    EditSdroutingTransportObjectTrackerFeaturePutResponse,
    GetListSdRoutingTransportObjecttrackerPayload,
    GetSingleSdRoutingTransportObjecttrackerPayload,
)


class ObjecttrackerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/objecttracker
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateSdroutingTransportObjectTrackerFeaturePostRequest,
        **kw,
    ) -> CreateSdroutingTransportObjectTrackerFeaturePostResponse:
        """
        Create a SD-Routing Object Tracker Feature for Transport Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttracker

        :param transport_id: Transport Profile ID
        :param payload: SD-Routing Object Tracker Feature for Transport Feature Profile
        :returns: CreateSdroutingTransportObjectTrackerFeaturePostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttracker",
            return_type=CreateSdroutingTransportObjectTrackerFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        object_tracker_id: str,
        payload: EditSdroutingTransportObjectTrackerFeaturePutRequest,
        **kw,
    ) -> EditSdroutingTransportObjectTrackerFeaturePutResponse:
        """
        Edit a SD-Routing Object Tracker Feature for Transport Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttracker/{objectTrackerId}

        :param transport_id: Transport Profile ID
        :param object_tracker_id: Object Tracker ID
        :param payload: SD-Routing Object Tracker Feature for Transport Feature Profile
        :returns: EditSdroutingTransportObjectTrackerFeaturePutResponse
        """
        params = {
            "transportId": transport_id,
            "objectTrackerId": object_tracker_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttracker/{objectTrackerId}",
            return_type=EditSdroutingTransportObjectTrackerFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, object_tracker_id: str, **kw):
        """
        Delete a SD-Routing Object Tracker Feature for Transport Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttracker/{objectTrackerId}

        :param transport_id: Transport Profile ID
        :param object_tracker_id: Object Tracker ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "objectTrackerId": object_tracker_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttracker/{objectTrackerId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, object_tracker_id: str, **kw
    ) -> GetSingleSdRoutingTransportObjecttrackerPayload:
        """
        Get a SD-Routing Object Tracker Feature for Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttracker/{objectTrackerId}

        :param transport_id: Transport Profile ID
        :param object_tracker_id: Object Tracker ID
        :returns: GetSingleSdRoutingTransportObjecttrackerPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdRoutingTransportObjecttrackerPayload:
        """
        Get all SD-Routing Object Tracker Features for Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttracker

        :param transport_id: Transport Profile ID
        :returns: GetListSdRoutingTransportObjecttrackerPayload
        """
        ...

    def get(
        self, transport_id: str, object_tracker_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportObjecttrackerPayload,
        GetSingleSdRoutingTransportObjecttrackerPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttracker/{objectTrackerId}
        if self._request_adapter.param_checker([(transport_id, str), (object_tracker_id, str)], []):
            params = {
                "transportId": transport_id,
                "objectTrackerId": object_tracker_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttracker/{objectTrackerId}",
                return_type=GetSingleSdRoutingTransportObjecttrackerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttracker
        if self._request_adapter.param_checker([(transport_id, str)], [object_tracker_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttracker",
                return_type=GetListSdRoutingTransportObjecttrackerPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
