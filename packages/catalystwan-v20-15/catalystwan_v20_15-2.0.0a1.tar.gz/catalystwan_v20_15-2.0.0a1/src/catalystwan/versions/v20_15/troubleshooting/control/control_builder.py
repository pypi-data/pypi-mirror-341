# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetControlConnections


class ControlBuilder:
    """
    Builds and executes requests for operations under /troubleshooting/control
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, uuid: str, **kw) -> GetControlConnections:
        """
        Troubleshoot control connections
        GET /dataservice/troubleshooting/control/{uuid}

        :param uuid: Uuid
        :returns: GetControlConnections
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/troubleshooting/control/{uuid}",
            return_type=GetControlConnections,
            params=params,
            **kw,
        )
