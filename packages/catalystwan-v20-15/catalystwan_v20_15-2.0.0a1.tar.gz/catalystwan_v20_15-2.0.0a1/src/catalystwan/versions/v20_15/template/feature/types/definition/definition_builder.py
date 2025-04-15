# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class DefinitionBuilder:
    """
    Builds and executes requests for operations under /template/feature/types/definition
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, type_name: str, version: str, **kw) -> List[Any]:
        """
        Generate template type definition


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/template/feature/types/definition/{type_name}/{version}

        :param type_name: Feature template type
        :param version: Version
        :returns: List[Any]
        """
        params = {
            "type_name": type_name,
            "version": version,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/template/feature/types/definition/{type_name}/{version}",
            return_type=List[Any],
            params=params,
            **kw,
        )
