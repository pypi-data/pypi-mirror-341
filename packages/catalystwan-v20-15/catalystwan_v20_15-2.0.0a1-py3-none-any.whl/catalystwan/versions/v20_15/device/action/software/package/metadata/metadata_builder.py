# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class MetadataBuilder:
    """
    Builds and executes requests for operations under /device/action/software/package/{versionId}/metadata
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, version_id: str, **kw):
        """
        Update Package Metadata
        GET /dataservice/device/action/software/package/{versionId}/metadata

        :param version_id: versionId
        :returns: None
        """
        params = {
            "versionId": version_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/action/software/package/{versionId}/metadata",
            params=params,
            **kw,
        )

    def put(self, version_id: str, payload: Any, **kw):
        """
        Update Package Metadata
        PUT /dataservice/device/action/software/package/{versionId}/metadata

        :param version_id: versionId
        :param payload: Request body to Update Package Metadata
        :returns: None
        """
        params = {
            "versionId": version_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/device/action/software/package/{versionId}/metadata",
            params=params,
            payload=payload,
            **kw,
        )
