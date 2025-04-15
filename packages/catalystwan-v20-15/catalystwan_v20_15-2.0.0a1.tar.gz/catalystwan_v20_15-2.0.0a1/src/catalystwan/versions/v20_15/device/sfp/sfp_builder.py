# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .detail.detail_builder import DetailBuilder
    from .diagnostic.diagnostic_builder import DiagnosticBuilder
    from .diagnostic_measurement_alarm.diagnostic_measurement_alarm_builder import (
        DiagnosticMeasurementAlarmBuilder,
    )
    from .diagnostic_measurement_value.diagnostic_measurement_value_builder import (
        DiagnosticMeasurementValueBuilder,
    )


class SfpBuilder:
    """
    Builds and executes requests for operations under /device/sfp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def detail(self) -> DetailBuilder:
        """
        The detail property
        """
        from .detail.detail_builder import DetailBuilder

        return DetailBuilder(self._request_adapter)

    @property
    def diagnostic(self) -> DiagnosticBuilder:
        """
        The diagnostic property
        """
        from .diagnostic.diagnostic_builder import DiagnosticBuilder

        return DiagnosticBuilder(self._request_adapter)

    @property
    def diagnostic_measurement_alarm(self) -> DiagnosticMeasurementAlarmBuilder:
        """
        The diagnosticMeasurementAlarm property
        """
        from .diagnostic_measurement_alarm.diagnostic_measurement_alarm_builder import (
            DiagnosticMeasurementAlarmBuilder,
        )

        return DiagnosticMeasurementAlarmBuilder(self._request_adapter)

    @property
    def diagnostic_measurement_value(self) -> DiagnosticMeasurementValueBuilder:
        """
        The diagnosticMeasurementValue property
        """
        from .diagnostic_measurement_value.diagnostic_measurement_value_builder import (
            DiagnosticMeasurementValueBuilder,
        )

        return DiagnosticMeasurementValueBuilder(self._request_adapter)
