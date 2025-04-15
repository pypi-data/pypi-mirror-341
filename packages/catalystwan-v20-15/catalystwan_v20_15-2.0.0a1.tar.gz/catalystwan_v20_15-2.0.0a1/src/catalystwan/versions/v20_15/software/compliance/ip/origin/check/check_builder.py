# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class CheckBuilder:
    """
    Builds and executes requests for operations under /software/compliance/ip/origin/check
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> List[Any]:
        """
        Block IP based on list
        POST /dataservice/software/compliance/ip/origin/check

        :param payload: Device detail
        :returns: List[Any]
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/software/compliance/ip/origin/check",
            return_type=List[Any],
            payload=payload,
            **kw,
        )
