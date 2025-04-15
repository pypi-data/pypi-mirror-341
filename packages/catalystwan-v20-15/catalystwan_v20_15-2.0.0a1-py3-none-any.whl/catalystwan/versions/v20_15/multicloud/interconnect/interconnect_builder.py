# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .accounts.accounts_builder import AccountsBuilder
    from .audit.audit_builder import AuditBuilder
    from .cloud.cloud_builder import CloudBuilder
    from .colors.colors_builder import ColorsBuilder
    from .config_group.config_group_builder import ConfigGroupBuilder
    from .connectivity.connectivity_builder import ConnectivityBuilder
    from .dashboard.dashboard_builder import DashboardBuilder
    from .entitlement.entitlement_builder import EntitlementBuilder
    from .gateways.gateways_builder import GatewaysBuilder
    from .ip_transit.ip_transit_builder import IpTransitBuilder
    from .locations.locations_builder import LocationsBuilder
    from .monitoring.monitoring_builder import MonitoringBuilder
    from .service_sw_package.service_sw_package_builder import ServiceSwPackageBuilder
    from .services.services_builder import ServicesBuilder
    from .settings.settings_builder import SettingsBuilder
    from .sshkeys.sshkeys_builder import SshkeysBuilder
    from .types.types_builder import TypesBuilder
    from .widget.widget_builder import WidgetBuilder


class InterconnectBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def accounts(self) -> AccountsBuilder:
        """
        The accounts property
        """
        from .accounts.accounts_builder import AccountsBuilder

        return AccountsBuilder(self._request_adapter)

    @property
    def audit(self) -> AuditBuilder:
        """
        The audit property
        """
        from .audit.audit_builder import AuditBuilder

        return AuditBuilder(self._request_adapter)

    @property
    def cloud(self) -> CloudBuilder:
        """
        The cloud property
        """
        from .cloud.cloud_builder import CloudBuilder

        return CloudBuilder(self._request_adapter)

    @property
    def colors(self) -> ColorsBuilder:
        """
        The colors property
        """
        from .colors.colors_builder import ColorsBuilder

        return ColorsBuilder(self._request_adapter)

    @property
    def config_group(self) -> ConfigGroupBuilder:
        """
        The config-group property
        """
        from .config_group.config_group_builder import ConfigGroupBuilder

        return ConfigGroupBuilder(self._request_adapter)

    @property
    def connectivity(self) -> ConnectivityBuilder:
        """
        The connectivity property
        """
        from .connectivity.connectivity_builder import ConnectivityBuilder

        return ConnectivityBuilder(self._request_adapter)

    @property
    def dashboard(self) -> DashboardBuilder:
        """
        The dashboard property
        """
        from .dashboard.dashboard_builder import DashboardBuilder

        return DashboardBuilder(self._request_adapter)

    @property
    def entitlement(self) -> EntitlementBuilder:
        """
        The entitlement property
        """
        from .entitlement.entitlement_builder import EntitlementBuilder

        return EntitlementBuilder(self._request_adapter)

    @property
    def gateways(self) -> GatewaysBuilder:
        """
        The gateways property
        """
        from .gateways.gateways_builder import GatewaysBuilder

        return GatewaysBuilder(self._request_adapter)

    @property
    def ip_transit(self) -> IpTransitBuilder:
        """
        The ip-transit property
        """
        from .ip_transit.ip_transit_builder import IpTransitBuilder

        return IpTransitBuilder(self._request_adapter)

    @property
    def locations(self) -> LocationsBuilder:
        """
        The locations property
        """
        from .locations.locations_builder import LocationsBuilder

        return LocationsBuilder(self._request_adapter)

    @property
    def monitoring(self) -> MonitoringBuilder:
        """
        The monitoring property
        """
        from .monitoring.monitoring_builder import MonitoringBuilder

        return MonitoringBuilder(self._request_adapter)

    @property
    def service_sw_package(self) -> ServiceSwPackageBuilder:
        """
        The service-sw-package property
        """
        from .service_sw_package.service_sw_package_builder import ServiceSwPackageBuilder

        return ServiceSwPackageBuilder(self._request_adapter)

    @property
    def services(self) -> ServicesBuilder:
        """
        The services property
        """
        from .services.services_builder import ServicesBuilder

        return ServicesBuilder(self._request_adapter)

    @property
    def settings(self) -> SettingsBuilder:
        """
        The settings property
        """
        from .settings.settings_builder import SettingsBuilder

        return SettingsBuilder(self._request_adapter)

    @property
    def sshkeys(self) -> SshkeysBuilder:
        """
        The sshkeys property
        """
        from .sshkeys.sshkeys_builder import SshkeysBuilder

        return SshkeysBuilder(self._request_adapter)

    @property
    def types(self) -> TypesBuilder:
        """
        The types property
        """
        from .types.types_builder import TypesBuilder

        return TypesBuilder(self._request_adapter)

    @property
    def widget(self) -> WidgetBuilder:
        """
        The widget property
        """
        from .widget.widget_builder import WidgetBuilder

        return WidgetBuilder(self._request_adapter)
