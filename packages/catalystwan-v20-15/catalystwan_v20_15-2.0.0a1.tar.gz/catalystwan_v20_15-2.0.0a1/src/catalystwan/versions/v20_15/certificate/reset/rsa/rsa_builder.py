# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class RsaBuilder:
    """
    Builds and executes requests for operations under /certificate/reset/rsa
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: str, **kw) -> str:
        """
        resetRSA for controllers
        POST /dataservice/certificate/reset/rsa

        :param payload: JSON payload with deviceIP details for rsa reset
        :returns: str
        """
        return self._request_adapter.request(
            "POST", "/dataservice/certificate/reset/rsa", return_type=str, payload=payload, **kw
        )
