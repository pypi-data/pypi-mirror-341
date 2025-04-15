# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EditAppDetailsPutRequest, PayloadItems


class ApplicationsBuilder:
    """
    Builds and executes requests for operations under /app-registry/applications
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, traffic_class: Optional[str] = None, business_relevance: Optional[str] = None, **kw
    ) -> List[Any]:
        """
        Get All the App for the given conditions
        GET /dataservice/app-registry/applications

        :param traffic_class: Traffic Class
        :param business_relevance: Business Relevance
        :returns: List[Any]
        """
        params = {
            "trafficClass": traffic_class,
            "businessRelevance": business_relevance,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/app-registry/applications",
            return_type=List[Any],
            params=params,
            **kw,
        )

    @overload
    def put(self, payload: Any, app_id: str, **kw) -> PayloadItems:
        """
        Edit App Details
        PUT /dataservice/app-registry/applications/{appId}

        :param payload: Request body
        :param app_id: appId
        :returns: PayloadItems
        """
        ...

    @overload
    def put(self, payload: List[EditAppDetailsPutRequest], **kw) -> List[Any]:
        """
        Edit App Details
        PUT /dataservice/app-registry/applications

        :param payload: Payload
        :returns: List[Any]
        """
        ...

    def put(
        self,
        payload: Union[Any, List[EditAppDetailsPutRequest]],
        app_id: Optional[str] = None,
        **kw,
    ) -> Union[List[Any], PayloadItems]:
        # /dataservice/app-registry/applications/{appId}
        if self._request_adapter.param_checker([(payload, Any), (app_id, str)], []):
            params = {
                "appId": app_id,
            }
            return self._request_adapter.request(
                "PUT",
                "/dataservice/app-registry/applications/{appId}",
                return_type=PayloadItems,
                params=params,
                payload=payload,
                **kw,
            )
        # /dataservice/app-registry/applications
        if self._request_adapter.param_checker(
            [(payload, List[EditAppDetailsPutRequest])], [app_id]
        ):
            return self._request_adapter.request(
                "PUT",
                "/dataservice/app-registry/applications",
                return_type=List[Any],
                payload=payload,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
