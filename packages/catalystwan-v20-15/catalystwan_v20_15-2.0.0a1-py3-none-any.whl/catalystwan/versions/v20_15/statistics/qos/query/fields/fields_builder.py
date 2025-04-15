# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import QoSQueryFieldsResp


class FieldsBuilder:
    """
    Builds and executes requests for operations under /statistics/qos/query/fields
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> QoSQueryFieldsResp:
        """
        Get query fields
        GET /dataservice/statistics/qos/query/fields

        :returns: QoSQueryFieldsResp
        """
        return self._request_adapter.request(
            "GET", "/dataservice/statistics/qos/query/fields", return_type=QoSQueryFieldsResp, **kw
        )
