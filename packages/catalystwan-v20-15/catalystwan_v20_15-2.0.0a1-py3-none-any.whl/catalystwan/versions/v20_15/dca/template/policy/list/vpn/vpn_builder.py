# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class VpnBuilder:
    """
    Builds and executes requests for operations under /dca/template/policy/list/vpn
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> List[Any]:
        """
        Get VPN details
        POST /dataservice/dca/template/policy/list/vpn

        :param payload: Query string
        :returns: List[Any]
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/dca/template/policy/list/vpn",
            return_type=List[Any],
            payload=payload,
            **kw,
        )
