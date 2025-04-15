# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class ServiceChainMappingBuilder:
    """
    Builds and executes requests for operations under /v1/service-insertion/service-chain-mapping
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Gets all the Service Chain Mapping with service chain definition name and service chain number.
        GET /dataservice/v1/service-insertion/service-chain-mapping

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/service-insertion/service-chain-mapping",
            return_type=List[Any],
            **kw,
        )
