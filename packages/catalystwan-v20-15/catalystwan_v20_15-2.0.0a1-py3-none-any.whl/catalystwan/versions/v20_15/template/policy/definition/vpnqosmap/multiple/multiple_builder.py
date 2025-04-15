# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class MultipleBuilder:
    """
    Builds and executes requests for operations under /template/policy/definition/vpnqosmap/multiple
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, id: str, payload: Any, **kw) -> Any:
        """
        Edit multiple policy definitions
        PUT /dataservice/template/policy/definition/vpnqosmap/multiple/{id}

        :param id: Policy Id
        :param payload: Policy definition
        :returns: Any
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/template/policy/definition/vpnqosmap/multiple/{id}",
            params=params,
            payload=payload,
            **kw,
        )
