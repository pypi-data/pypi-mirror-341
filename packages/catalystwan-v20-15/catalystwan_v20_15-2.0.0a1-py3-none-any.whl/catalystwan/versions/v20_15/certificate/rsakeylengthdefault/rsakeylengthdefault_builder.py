# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class RsakeylengthdefaultBuilder:
    """
    Builds and executes requests for operations under /certificate/rsakeylengthdefault
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> str:
        """
        Check if all devices in network use 2048-b RSA Key length for their device certs.
        GET /dataservice/certificate/rsakeylengthdefault

        :returns: str
        """
        return self._request_adapter.request(
            "GET", "/dataservice/certificate/rsakeylengthdefault", return_type=str, **kw
        )
