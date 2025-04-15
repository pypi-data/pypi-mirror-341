# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class BulkBuilder:
    """
    Builds and executes requests for operations under /template/policy/definition/intrusionprevention/bulk
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, payload: Any, **kw) -> Any:
        """
        Create/Edit policy definitions in bulk
        PUT /dataservice/template/policy/definition/intrusionprevention/bulk

        :param payload: Policy definition
        :returns: Any
        """
        return self._request_adapter.request(
            "PUT",
            "/dataservice/template/policy/definition/intrusionprevention/bulk",
            payload=payload,
            **kw,
        )
