# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class SelfsignedcertBuilder:
    """
    Builds and executes requests for operations under /certificate/vmanage/selfsignedcert
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> str:
        """
        get vManage self signed cert
        GET /dataservice/certificate/vmanage/selfsignedcert

        :returns: str
        """
        return self._request_adapter.request(
            "GET", "/dataservice/certificate/vmanage/selfsignedcert", return_type=str, **kw
        )
