# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EventQueryInputResponse


class FieldsBuilder:
    """
    Builds and executes requests for operations under /event/query/fields
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> EventQueryInputResponse:
        """
        Get query fields
        GET /dataservice/event/query/fields

        :returns: EventQueryInputResponse
        """
        return self._request_adapter.request(
            "GET", "/dataservice/event/query/fields", return_type=EventQueryInputResponse, **kw
        )
