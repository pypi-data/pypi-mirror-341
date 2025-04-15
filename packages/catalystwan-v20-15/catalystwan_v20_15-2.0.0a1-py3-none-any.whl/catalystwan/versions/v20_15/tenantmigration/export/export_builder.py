# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import MigrateTenantModel


class ExportBuilder:
    """
    Builds and executes requests for operations under /tenantmigration/export
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: MigrateTenantModel, **kw) -> Any:
        """
        Export tenant data
        POST /dataservice/tenantmigration/export

        :param payload: Payload
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/tenantmigration/export", payload=payload, **kw
        )
