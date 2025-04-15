# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class RemoteserverBuilder:
    """
    Builds and executes requests for operations under /device/action/software/remoteserver
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, version_id: str, **kw) -> Any:
        """
        Get Image Remote Server Details
        GET /dataservice/device/action/software/remoteserver/{versionId}

        :param version_id: Version
        :returns: Any
        """
        params = {
            "versionId": version_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/action/software/remoteserver/{versionId}",
            params=params,
            **kw,
        )

    def put(self, version_id: str, payload: Any, **kw):
        """
        Update Image Remote Server Details
        PUT /dataservice/device/action/software/remoteserver/{versionId}

        :param version_id: Image ID
        :param payload: Update image remote server details
        :returns: None
        """
        params = {
            "versionId": version_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/device/action/software/remoteserver/{versionId}",
            params=params,
            payload=payload,
            **kw,
        )
