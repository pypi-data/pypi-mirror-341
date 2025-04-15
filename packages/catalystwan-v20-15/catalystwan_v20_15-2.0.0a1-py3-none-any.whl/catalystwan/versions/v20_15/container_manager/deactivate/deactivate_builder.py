# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface


class DeactivateBuilder:
    """
    Builds and executes requests for operations under /container-manager/deactivate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, container_name: str, host_ip: Optional[str] = None, **kw):
        """
        Deactivate container on remote host
        POST /dataservice/container-manager/deactivate/{containerName}

        :param container_name: Container name
        :param host_ip: Container host IP
        :returns: None
        """
        params = {
            "containerName": container_name,
            "hostIp": host_ip,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/container-manager/deactivate/{containerName}", params=params, **kw
        )
