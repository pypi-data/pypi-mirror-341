# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class RootcaBuilder:
    """
    Builds and executes requests for operations under /sslproxy/settings/enterprise/rootca
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get vManage enterprise root certificate
        GET /dataservice/sslproxy/settings/enterprise/rootca

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/sslproxy/settings/enterprise/rootca", **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Set vManage enterprise root certificate
        POST /dataservice/sslproxy/settings/enterprise/rootca

        :param payload: Set enterprise root CA request
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/sslproxy/settings/enterprise/rootca", payload=payload, **kw
        )
