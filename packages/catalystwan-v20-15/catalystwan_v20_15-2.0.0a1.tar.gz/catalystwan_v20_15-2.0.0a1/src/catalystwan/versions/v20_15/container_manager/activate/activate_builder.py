# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface


class ActivateBuilder:
    """
    Builds and executes requests for operations under /container-manager/activate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        container_name: str,
        url: Optional[str] = None,
        host_ip: Optional[str] = None,
        checksum: Optional[str] = None,
        **kw,
    ):
        """
        Activate container on remote host
        POST /dataservice/container-manager/activate/{containerName}

        :param container_name: Container name
        :param url: Container image URL
        :param host_ip: Container host IP
        :param checksum: Container image checksum
        :returns: None
        """
        params = {
            "containerName": container_name,
            "url": url,
            "hostIp": host_ip,
            "checksum": checksum,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/container-manager/activate/{containerName}", params=params, **kw
        )
