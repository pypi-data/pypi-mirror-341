# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class SetupBuilder:
    """
    Builds and executes requests for operations under /clusterManagement/setup
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, payload: Any, **kw):
        """
        Update vManage cluster info


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        PUT /dataservice/clusterManagement/setup

        :param payload: vManage cluster config
        :returns: None
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/clusterManagement/setup", payload=payload, **kw
        )

    def post(self, payload: Any, **kw):
        """
        Add vManage to cluster
        POST /dataservice/clusterManagement/setup

        :param payload: vManage cluster config
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/clusterManagement/setup", payload=payload, **kw
        )
