# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SyncDevicesResp


class SyncBuilder:
    """
    Builds and executes requests for operations under /system/device/smartaccount/sync
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> SyncDevicesResp:
        """
        Sync devices from Smart-Account
        POST /dataservice/system/device/smartaccount/sync

        :param payload: Request body for Sync devices from Smart-Account
        :returns: SyncDevicesResp
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/system/device/smartaccount/sync",
            return_type=SyncDevicesResp,
            payload=payload,
            **kw,
        )
