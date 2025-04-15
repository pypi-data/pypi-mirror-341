# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .analyze_cli_config.analyze_cli_config_builder import AnalyzeCliConfigBuilder
    from .running_ios_cli_config.running_ios_cli_config_builder import RunningIosCliConfigBuilder
    from .unsupported_cli_config.unsupported_cli_config_builder import UnsupportedCliConfigBuilder


class DeviceBuilder:
    """
    Builds and executes requests for operations under /v1/device
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def analyze_cli_config(self) -> AnalyzeCliConfigBuilder:
        """
        The analyzeCliConfig property
        """
        from .analyze_cli_config.analyze_cli_config_builder import AnalyzeCliConfigBuilder

        return AnalyzeCliConfigBuilder(self._request_adapter)

    @property
    def running_ios_cli_config(self) -> RunningIosCliConfigBuilder:
        """
        The runningIosCliConfig property
        """
        from .running_ios_cli_config.running_ios_cli_config_builder import (
            RunningIosCliConfigBuilder,
        )

        return RunningIosCliConfigBuilder(self._request_adapter)

    @property
    def unsupported_cli_config(self) -> UnsupportedCliConfigBuilder:
        """
        The unsupportedCliConfig property
        """
        from .unsupported_cli_config.unsupported_cli_config_builder import (
            UnsupportedCliConfigBuilder,
        )

        return UnsupportedCliConfigBuilder(self._request_adapter)
