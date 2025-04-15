# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class SslproxyBuilder:
    """
    Builds and executes requests for operations under /sslproxy/generate/csr/sslproxy
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        CSR request SSL proxy for edge
        POST /dataservice/sslproxy/generate/csr/sslproxy

        :param payload: CSR request for edge
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "generateSslProxyCSR")
        return self._request_adapter.request(
            "POST", "/dataservice/sslproxy/generate/csr/sslproxy", payload=payload, **kw
        )
