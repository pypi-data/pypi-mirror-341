# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import FindVEdgeSoftwareVersion


class VersionBuilder:
    """
    Builds and executes requests for operations under /device/action/software/vedge/version
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> FindVEdgeSoftwareVersion:
        """
        Get vEdge software version
        GET /dataservice/device/action/software/vedge/version

        :returns: FindVEdgeSoftwareVersion
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/action/software/vedge/version",
            return_type=FindVEdgeSoftwareVersion,
            **kw,
        )
