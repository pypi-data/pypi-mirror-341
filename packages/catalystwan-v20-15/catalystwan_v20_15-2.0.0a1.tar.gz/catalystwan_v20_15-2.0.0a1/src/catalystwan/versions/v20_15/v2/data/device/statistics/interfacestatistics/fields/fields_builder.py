# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Field


class FieldsBuilder:
    """
    Builds and executes requests for operations under /v2/data/device/statistics/interfacestatistics/fields
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Field]:
        """
        Get statistics fields and types
        GET /dataservice/v2/data/device/statistics/interfacestatistics/fields

        :returns: List[Field]
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/v2/data/device/statistics/interfacestatistics/fields",
            return_type=List[Field],
            **kw,
        )
