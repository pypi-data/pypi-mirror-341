# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class VersionBuilder:
    """
    Builds and executes requests for operations under /clusterManagement/clusterworkflow/version
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        List vManages in the cluster


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/clusterManagement/clusterworkflow/version

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/clusterManagement/clusterworkflow/version",
            return_type=List[Any],
            **kw,
        )
