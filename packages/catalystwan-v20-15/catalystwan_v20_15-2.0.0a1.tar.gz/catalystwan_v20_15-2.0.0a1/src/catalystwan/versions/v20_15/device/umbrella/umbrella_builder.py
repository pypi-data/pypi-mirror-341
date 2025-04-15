# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .device_registration.device_registration_builder import DeviceRegistrationBuilder
    from .dnscrypt.dnscrypt_builder import DnscryptBuilder
    from .dp_stats.dp_stats_builder import DpStatsBuilder
    from .overview.overview_builder import OverviewBuilder
    from .umbrella_config.umbrella_config_builder import UmbrellaConfigBuilder


class UmbrellaBuilder:
    """
    Builds and executes requests for operations under /device/umbrella
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def device_registration(self) -> DeviceRegistrationBuilder:
        """
        The device-registration property
        """
        from .device_registration.device_registration_builder import DeviceRegistrationBuilder

        return DeviceRegistrationBuilder(self._request_adapter)

    @property
    def dnscrypt(self) -> DnscryptBuilder:
        """
        The dnscrypt property
        """
        from .dnscrypt.dnscrypt_builder import DnscryptBuilder

        return DnscryptBuilder(self._request_adapter)

    @property
    def dp_stats(self) -> DpStatsBuilder:
        """
        The dp-stats property
        """
        from .dp_stats.dp_stats_builder import DpStatsBuilder

        return DpStatsBuilder(self._request_adapter)

    @property
    def overview(self) -> OverviewBuilder:
        """
        The overview property
        """
        from .overview.overview_builder import OverviewBuilder

        return OverviewBuilder(self._request_adapter)

    @property
    def umbrella_config(self) -> UmbrellaConfigBuilder:
        """
        The umbrella-config property
        """
        from .umbrella_config.umbrella_config_builder import UmbrellaConfigBuilder

        return UmbrellaConfigBuilder(self._request_adapter)
