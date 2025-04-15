# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface


class InspectBuilder:
    """
    Builds and executes requests for operations under /container-manager/inspect
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, container_name: str, host_ip: Optional[str] = None, **kw) -> str:
        """
        Get container inspect data
        GET /dataservice/container-manager/inspect/{containerName}

        :param container_name: Container name
        :param host_ip: Container host IP
        :returns: str
        """
        params = {
            "containerName": container_name,
            "hostIp": host_ip,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/container-manager/inspect/{containerName}",
            return_type=str,
            params=params,
            **kw,
        )
