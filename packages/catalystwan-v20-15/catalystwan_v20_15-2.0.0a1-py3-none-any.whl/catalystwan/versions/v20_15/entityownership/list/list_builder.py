# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EntityOwnershipInfo


class ListBuilder:
    """
    Builds and executes requests for operations under /entityownership/list
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> EntityOwnershipInfo:
        """
        List all entity ownership info
        GET /dataservice/entityownership/list

        :returns: EntityOwnershipInfo
        """
        return self._request_adapter.request(
            "GET", "/dataservice/entityownership/list", return_type=EntityOwnershipInfo, **kw
        )
