# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import PushCgwConfig, Taskid


class PushCgwConfigBuilder:
    """
    Builds and executes requests for operations under /multicloud/pushCgwConfig
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: PushCgwConfig, **kw) -> Taskid:
        """
        Push configuration to devices of CGW
        POST /dataservice/multicloud/pushCgwConfig

        :param payload: Push configuration to devices of CGW
        :returns: Taskid
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/pushCgwConfig",
            return_type=Taskid,
            payload=payload,
            **kw,
        )
