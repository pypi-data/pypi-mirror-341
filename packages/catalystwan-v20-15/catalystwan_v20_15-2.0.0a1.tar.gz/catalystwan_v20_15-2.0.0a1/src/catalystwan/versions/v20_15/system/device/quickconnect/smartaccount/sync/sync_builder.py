# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SmartAccountModel, SyncDevicesResp


class SyncBuilder:
    """
    Builds and executes requests for operations under /system/device/quickconnect/smartaccount/sync
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: SmartAccountModel, **kw) -> SyncDevicesResp:
        """
        Sync devices from Smart-Account
        POST /dataservice/system/device/quickconnect/smartaccount/sync

        :param payload: Payload
        :returns: SyncDevicesResp
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/system/device/quickconnect/smartaccount/sync",
            return_type=SyncDevicesResp,
            payload=payload,
            **kw,
        )
