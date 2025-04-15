# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class FileBuilder:
    """
    Builds and executes requests for operations under /statistics/download/{processType}/file
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        process_type: str,
        file_type: str,
        queue: str,
        device_ip: str,
        token: str,
        file_name: str,
        **kw,
    ) -> Any:
        """
        Downloading stats file
        GET /dataservice/statistics/download/{processType}/file/{fileType}/{queue}/{deviceIp}/{token}/{fileName}

        :param process_type: Process type
        :param file_type: File type
        :param queue: Queue name
        :param device_ip: Device IP
        :param token: Token
        :param file_name: File name
        :returns: Any
        """
        params = {
            "processType": process_type,
            "fileType": file_type,
            "queue": queue,
            "deviceIp": device_ip,
            "token": token,
            "fileName": file_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/download/{processType}/file/{fileType}/{queue}/{deviceIp}/{token}/{fileName}",
            params=params,
            **kw,
        )
