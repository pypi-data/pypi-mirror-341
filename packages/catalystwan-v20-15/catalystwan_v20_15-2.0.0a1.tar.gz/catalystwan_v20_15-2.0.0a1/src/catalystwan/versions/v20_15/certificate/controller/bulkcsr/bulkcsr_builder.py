# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface


class BulkcsrBuilder:
    """
    Builds and executes requests for operations under /certificate/controller/bulkcsr
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, csr_key_length: Optional[str] = None, **kw) -> str:
        """
        Generate CSR for all controller
        POST /dataservice/certificate/controller/bulkcsr

        :param csr_key_length: Optional Parameter: CSR Key Length
        :returns: str
        """
        params = {
            "csrKeyLength": csr_key_length,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/certificate/controller/bulkcsr",
            return_type=str,
            params=params,
            **kw,
        )
