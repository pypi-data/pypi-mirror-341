# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .accesstoken.accesstoken_builder import AccesstokenBuilder
    from .alarm.alarm_builder import AlarmBuilder
    from .idtoken.idtoken_builder import IdtokenBuilder
    from .otp.otp_builder import OtpBuilder
    from .telemetry.telemetry_builder import TelemetryBuilder
    from .vanalytics.vanalytics_builder import VanalyticsBuilder


class CloudservicesBuilder:
    """
    Builds and executes requests for operations under /dca/cloudservices
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get cloud service settings
        GET /dataservice/dca/cloudservices

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/dca/cloudservices", **kw)

    @property
    def accesstoken(self) -> AccesstokenBuilder:
        """
        The accesstoken property
        """
        from .accesstoken.accesstoken_builder import AccesstokenBuilder

        return AccesstokenBuilder(self._request_adapter)

    @property
    def alarm(self) -> AlarmBuilder:
        """
        The alarm property
        """
        from .alarm.alarm_builder import AlarmBuilder

        return AlarmBuilder(self._request_adapter)

    @property
    def idtoken(self) -> IdtokenBuilder:
        """
        The idtoken property
        """
        from .idtoken.idtoken_builder import IdtokenBuilder

        return IdtokenBuilder(self._request_adapter)

    @property
    def otp(self) -> OtpBuilder:
        """
        The otp property
        """
        from .otp.otp_builder import OtpBuilder

        return OtpBuilder(self._request_adapter)

    @property
    def telemetry(self) -> TelemetryBuilder:
        """
        The telemetry property
        """
        from .telemetry.telemetry_builder import TelemetryBuilder

        return TelemetryBuilder(self._request_adapter)

    @property
    def vanalytics(self) -> VanalyticsBuilder:
        """
        The vanalytics property
        """
        from .vanalytics.vanalytics_builder import VanalyticsBuilder

        return VanalyticsBuilder(self._request_adapter)
