# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AnalyzeCliConfig


class AnalyzeCliConfigBuilder:
    """
    Builds and executes requests for operations under /v1/device/analyzeCliConfig
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: AnalyzeCliConfig, **kw) -> Any:
        """
        Analyze CLI Config for device
        POST /dataservice/v1/device/analyzeCliConfig

        :param payload: CLI Configs for device
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/v1/device/analyzeCliConfig", payload=payload, **kw
        )
