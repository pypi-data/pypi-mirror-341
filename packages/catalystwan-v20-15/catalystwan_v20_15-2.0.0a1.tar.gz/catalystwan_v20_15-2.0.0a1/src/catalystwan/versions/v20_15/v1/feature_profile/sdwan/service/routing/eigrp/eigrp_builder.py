# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateRoutingEigrpProfileParcelForServicePostRequest,
    CreateRoutingEigrpProfileParcelForServicePostResponse,
    EditRoutingEigrpProfileParcelForServicePutRequest,
    EditRoutingEigrpProfileParcelForServicePutResponse,
    GetListSdwanServiceRoutingEigrpPayload,
    GetSingleSdwanServiceRoutingEigrpPayload,
)


class EigrpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/routing/eigrp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateRoutingEigrpProfileParcelForServicePostRequest, **kw
    ) -> CreateRoutingEigrpProfileParcelForServicePostResponse:
        """
        Create a Routing Eigrp Profile Feature for Service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/eigrp

        :param service_id: Feature Profile ID
        :param payload: Routing Eigrp Profile Feature
        :returns: CreateRoutingEigrpProfileParcelForServicePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/eigrp",
            return_type=CreateRoutingEigrpProfileParcelForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        eigrp_id: str,
        payload: EditRoutingEigrpProfileParcelForServicePutRequest,
        **kw,
    ) -> EditRoutingEigrpProfileParcelForServicePutResponse:
        """
        Update a Routing Eigrp Profile Feature for Service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/eigrp/{eigrpId}

        :param service_id: Feature Profile ID
        :param eigrp_id: Profile Feature ID
        :param payload: Routing Eigrp Profile Feature
        :returns: EditRoutingEigrpProfileParcelForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "eigrpId": eigrp_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/eigrp/{eigrpId}",
            return_type=EditRoutingEigrpProfileParcelForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, eigrp_id: str, **kw):
        """
        Delete a Routing Eigrp Profile Feature for Service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/eigrp/{eigrpId}

        :param service_id: Feature Profile ID
        :param eigrp_id: Profile Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "eigrpId": eigrp_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/eigrp/{eigrpId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, service_id: str, eigrp_id: str, **kw) -> GetSingleSdwanServiceRoutingEigrpPayload:
        """
        Get Routing Eigrp Profile Feature by parcelId for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/eigrp/{eigrpId}

        :param service_id: Feature Profile ID
        :param eigrp_id: Profile Feature ID
        :returns: GetSingleSdwanServiceRoutingEigrpPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdwanServiceRoutingEigrpPayload:
        """
        Get Routing Eigrp Profile Features for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/eigrp

        :param service_id: Feature Profile ID
        :returns: GetListSdwanServiceRoutingEigrpPayload
        """
        ...

    def get(
        self, service_id: str, eigrp_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanServiceRoutingEigrpPayload, GetSingleSdwanServiceRoutingEigrpPayload]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/eigrp/{eigrpId}
        if self._request_adapter.param_checker([(service_id, str), (eigrp_id, str)], []):
            params = {
                "serviceId": service_id,
                "eigrpId": eigrp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/eigrp/{eigrpId}",
                return_type=GetSingleSdwanServiceRoutingEigrpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/eigrp
        if self._request_adapter.param_checker([(service_id, str)], [eigrp_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/eigrp",
                return_type=GetListSdwanServiceRoutingEigrpPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
