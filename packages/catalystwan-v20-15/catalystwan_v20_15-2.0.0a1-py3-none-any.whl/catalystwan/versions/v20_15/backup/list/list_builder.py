# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import LocalBackupListResult


class ListBuilder:
    """
    Builds and executes requests for operations under /backup/list
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, size: Optional[str] = None, **kw) -> LocalBackupListResult:
        """
        List all backup files of a tenant stored in vManage
        GET /dataservice/backup/list

        :param size: Size
        :returns: LocalBackupListResult
        """
        params = {
            "size": size,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/backup/list",
            return_type=LocalBackupListResult,
            params=params,
            **kw,
        )
