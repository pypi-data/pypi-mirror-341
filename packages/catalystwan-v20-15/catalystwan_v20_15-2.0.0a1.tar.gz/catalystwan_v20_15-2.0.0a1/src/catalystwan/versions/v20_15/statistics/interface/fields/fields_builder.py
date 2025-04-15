# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterfaceDocCountRequest


class FieldsBuilder:
    """
    Builds and executes requests for operations under /statistics/interface/fields
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[InterfaceDocCountRequest]:
        """
        Get fields and type
        GET /dataservice/statistics/interface/fields

        :returns: List[InterfaceDocCountRequest]
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/interface/fields",
            return_type=List[InterfaceDocCountRequest],
            **kw,
        )
