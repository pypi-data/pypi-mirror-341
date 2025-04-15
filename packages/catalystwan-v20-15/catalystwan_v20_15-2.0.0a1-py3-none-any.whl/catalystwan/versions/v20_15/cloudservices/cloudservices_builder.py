# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .accesstoken.accesstoken_builder import AccesstokenBuilder
    from .app.app_builder import AppBuilder
    from .authtoken.authtoken_builder import AuthtokenBuilder
    from .connect.connect_builder import ConnectBuilder
    from .credentials.credentials_builder import CredentialsBuilder
    from .devicecode.devicecode_builder import DevicecodeBuilder
    from .m365.m365_builder import M365Builder
    from .staging.staging_builder import StagingBuilder
    from .telemetry.telemetry_builder import TelemetryBuilder
    from .vanalytics.vanalytics_builder import VanalyticsBuilder


class CloudservicesBuilder:
    """
    Builds and executes requests for operations under /cloudservices
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def accesstoken(self) -> AccesstokenBuilder:
        """
        The accesstoken property
        """
        from .accesstoken.accesstoken_builder import AccesstokenBuilder

        return AccesstokenBuilder(self._request_adapter)

    @property
    def app(self) -> AppBuilder:
        """
        The app property
        """
        from .app.app_builder import AppBuilder

        return AppBuilder(self._request_adapter)

    @property
    def authtoken(self) -> AuthtokenBuilder:
        """
        The authtoken property
        """
        from .authtoken.authtoken_builder import AuthtokenBuilder

        return AuthtokenBuilder(self._request_adapter)

    @property
    def connect(self) -> ConnectBuilder:
        """
        The connect property
        """
        from .connect.connect_builder import ConnectBuilder

        return ConnectBuilder(self._request_adapter)

    @property
    def credentials(self) -> CredentialsBuilder:
        """
        The credentials property
        """
        from .credentials.credentials_builder import CredentialsBuilder

        return CredentialsBuilder(self._request_adapter)

    @property
    def devicecode(self) -> DevicecodeBuilder:
        """
        The devicecode property
        """
        from .devicecode.devicecode_builder import DevicecodeBuilder

        return DevicecodeBuilder(self._request_adapter)

    @property
    def m365(self) -> M365Builder:
        """
        The m365 property
        """
        from .m365.m365_builder import M365Builder

        return M365Builder(self._request_adapter)

    @property
    def staging(self) -> StagingBuilder:
        """
        The staging property
        """
        from .staging.staging_builder import StagingBuilder

        return StagingBuilder(self._request_adapter)

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
