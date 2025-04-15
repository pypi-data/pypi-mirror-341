# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AlarmSeverityMapping


class SeveritymappingsBuilder:
    """
    Builds and executes requests for operations under /alarms/severitymappings
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[AlarmSeverityMapping]:
        """
        Gets alarm severity mappings
        GET /dataservice/alarms/severitymappings

        :returns: List[AlarmSeverityMapping]
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/alarms/severitymappings",
            return_type=List[AlarmSeverityMapping],
            **kw,
        )
