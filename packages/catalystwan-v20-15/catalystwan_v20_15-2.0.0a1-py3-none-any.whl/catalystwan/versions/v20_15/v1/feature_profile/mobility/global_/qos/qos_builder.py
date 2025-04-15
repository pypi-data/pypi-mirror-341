# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateQosFeatureForGlobalPostRequest,
    CreateQosFeatureForGlobalPostResponse,
    EditQosFeatureForGlobalPutRequest,
    EditQosFeatureForGlobalPutResponse,
    GetListMobilityGlobalQosPayload,
    GetSingleMobilityGlobalQosPayload,
)


class QosBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility/global/{globalId}/qos
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, global_id: str, payload: CreateQosFeatureForGlobalPostRequest, **kw
    ) -> CreateQosFeatureForGlobalPostResponse:
        """
        Create a Qos Feature for Global feature profile
        POST /dataservice/v1/feature-profile/mobility/global/{globalId}/qos

        :param global_id: Feature Profile ID
        :param payload: Qos Feature
        :returns: CreateQosFeatureForGlobalPostResponse
        """
        params = {
            "globalId": global_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/mobility/global/{globalId}/qos",
            return_type=CreateQosFeatureForGlobalPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, global_id: str, qos_id: str, payload: EditQosFeatureForGlobalPutRequest, **kw
    ) -> EditQosFeatureForGlobalPutResponse:
        """
        Update a Qos Feature for Global feature profile
        PUT /dataservice/v1/feature-profile/mobility/global/{globalId}/qos/{qosId}

        :param global_id: Feature Profile ID
        :param qos_id: Feature ID
        :param payload: Qos Feature
        :returns: EditQosFeatureForGlobalPutResponse
        """
        params = {
            "globalId": global_id,
            "qosId": qos_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/mobility/global/{globalId}/qos/{qosId}",
            return_type=EditQosFeatureForGlobalPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, global_id: str, qos_id: str, **kw):
        """
        Delete a Qos Feature for Global feature profile
        DELETE /dataservice/v1/feature-profile/mobility/global/{globalId}/qos/{qosId}

        :param global_id: Feature Profile ID
        :param qos_id: Feature ID
        :returns: None
        """
        params = {
            "globalId": global_id,
            "qosId": qos_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/mobility/global/{globalId}/qos/{qosId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, global_id: str, qos_id: str, **kw) -> GetSingleMobilityGlobalQosPayload:
        """
        Get Qos Feature by parcelId for Global feature profile
        GET /dataservice/v1/feature-profile/mobility/global/{globalId}/qos/{qosId}

        :param global_id: Feature Profile ID
        :param qos_id: Feature ID
        :returns: GetSingleMobilityGlobalQosPayload
        """
        ...

    @overload
    def get(self, global_id: str, **kw) -> GetListMobilityGlobalQosPayload:
        """
        Get Qos Feature for Global feature profile
        GET /dataservice/v1/feature-profile/mobility/global/{globalId}/qos

        :param global_id: Feature Profile ID
        :returns: GetListMobilityGlobalQosPayload
        """
        ...

    def get(
        self, global_id: str, qos_id: Optional[str] = None, **kw
    ) -> Union[GetListMobilityGlobalQosPayload, GetSingleMobilityGlobalQosPayload]:
        # /dataservice/v1/feature-profile/mobility/global/{globalId}/qos/{qosId}
        if self._request_adapter.param_checker([(global_id, str), (qos_id, str)], []):
            params = {
                "globalId": global_id,
                "qosId": qos_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{globalId}/qos/{qosId}",
                return_type=GetSingleMobilityGlobalQosPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/mobility/global/{globalId}/qos
        if self._request_adapter.param_checker([(global_id, str)], [qos_id]):
            params = {
                "globalId": global_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{globalId}/qos",
                return_type=GetListMobilityGlobalQosPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
