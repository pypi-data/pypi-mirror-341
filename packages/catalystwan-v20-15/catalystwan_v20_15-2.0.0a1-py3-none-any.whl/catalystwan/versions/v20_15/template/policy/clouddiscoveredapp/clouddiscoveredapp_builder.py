# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class ClouddiscoveredappBuilder:
    """
    Builds and executes requests for operations under /template/policy/clouddiscoveredapp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get all cloud discovered applications
        GET /dataservice/template/policy/clouddiscoveredapp

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/template/policy/clouddiscoveredapp", return_type=List[Any], **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Set SLA class for policy cloud discovered applications
        POST /dataservice/template/policy/clouddiscoveredapp

        :param payload: App payload
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/policy/clouddiscoveredapp", payload=payload, **kw
        )
