# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ActionParam


class ActionBuilder:
    """
    Builds and executes requests for operations under /util/olapdb/migration/action
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, action: ActionParam, **kw) -> str:
        """
        Migration actions - start pause or restart migration
        POST /dataservice/util/olapdb/migration/action/{action}

        :param action: Migration action
        :returns: str
        """
        params = {
            "action": action,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/util/olapdb/migration/action/{action}",
            return_type=str,
            params=params,
            **kw,
        )
