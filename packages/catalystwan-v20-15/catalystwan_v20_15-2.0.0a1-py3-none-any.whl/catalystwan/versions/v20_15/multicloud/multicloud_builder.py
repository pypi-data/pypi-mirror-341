# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .accounts.accounts_builder import AccountsBuilder
    from .audit.audit_builder import AuditBuilder
    from .billingaccounts.billingaccounts_builder import BillingaccountsBuilder
    from .cloud_routers_and_attachments.cloud_routers_and_attachments_builder import (
        CloudRoutersAndAttachmentsBuilder,
    )
    from .cloudgateway.cloudgateway_builder import CloudgatewayBuilder
    from .cloudgateways.cloudgateways_builder import CloudgatewaysBuilder
    from .cloudgatewaysetting.cloudgatewaysetting_builder import CloudgatewaysettingBuilder
    from .cloudgatewaytype.cloudgatewaytype_builder import CloudgatewaytypeBuilder
    from .config_group.config_group_builder import ConfigGroupBuilder
    from .connected_sites.connected_sites_builder import ConnectedSitesBuilder
    from .connectivity.connectivity_builder import ConnectivityBuilder
    from .connectivitygateway.connectivitygateway_builder import ConnectivitygatewayBuilder
    from .connectivitygatewaycreationoptions.connectivitygatewaycreationoptions_builder import (
        ConnectivitygatewaycreationoptionsBuilder,
    )
    from .corenetworkpolicy.corenetworkpolicy_builder import CorenetworkpolicyBuilder
    from .dashboard.dashboard_builder import DashboardBuilder
    from .device.device_builder import DeviceBuilder
    from .devicelink.devicelink_builder import DevicelinkBuilder
    from .devices.devices_builder import DevicesBuilder
    from .edge.edge_builder import EdgeBuilder
    from .gateway.gateway_builder import GatewayBuilder
    from .gateways.gateways_builder import GatewaysBuilder
    from .hostvpc.hostvpc_builder import HostvpcBuilder
    from .imagename.imagename_builder import ImagenameBuilder
    from .instancesize.instancesize_builder import InstancesizeBuilder
    from .interconnect.interconnect_builder import InterconnectBuilder
    from .interfacecolor.interfacecolor_builder import InterfacecolorBuilder
    from .license.license_builder import LicenseBuilder
    from .locations.locations_builder import LocationsBuilder
    from .loopback_cgw_color.loopback_cgw_color_builder import LoopbackCgwColorBuilder
    from .loopbacktransportcolor.loopbacktransportcolor_builder import LoopbacktransportcolorBuilder
    from .map.map_builder import MapBuilder
    from .mapping.mapping_builder import MappingBuilder
    from .partnerports.partnerports_builder import PartnerportsBuilder
    from .port_speed.port_speed_builder import PortSpeedBuilder
    from .push_cgw_config.push_cgw_config_builder import PushCgwConfigBuilder
    from .regions.regions_builder import RegionsBuilder
    from .settings.settings_builder import SettingsBuilder
    from .site.site_builder import SiteBuilder
    from .sshkeys.sshkeys_builder import SshkeysBuilder
    from .statistics.statistics_builder import StatisticsBuilder
    from .swimages.swimages_builder import SwimagesBuilder
    from .telemetry.telemetry_builder import TelemetryBuilder
    from .tunnels.tunnels_builder import TunnelsBuilder
    from .types.types_builder import TypesBuilder
    from .vhubs.vhubs_builder import VhubsBuilder
    from .vwan.vwan_builder import VwanBuilder
    from .vwans.vwans_builder import VwansBuilder
    from .widget.widget_builder import WidgetBuilder


class MulticloudBuilder:
    """
    Builds and executes requests for operations under /multicloud
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
    def billingaccounts(self) -> BillingaccountsBuilder:
        """
        The billingaccounts property
        """
        from .billingaccounts.billingaccounts_builder import BillingaccountsBuilder

        return BillingaccountsBuilder(self._request_adapter)

    @property
    def cloud_routers_and_attachments(self) -> CloudRoutersAndAttachmentsBuilder:
        """
        The cloudRoutersAndAttachments property
        """
        from .cloud_routers_and_attachments.cloud_routers_and_attachments_builder import (
            CloudRoutersAndAttachmentsBuilder,
        )

        return CloudRoutersAndAttachmentsBuilder(self._request_adapter)

    @property
    def cloudgateway(self) -> CloudgatewayBuilder:
        """
        The cloudgateway property
        """
        from .cloudgateway.cloudgateway_builder import CloudgatewayBuilder

        return CloudgatewayBuilder(self._request_adapter)

    @property
    def cloudgateways(self) -> CloudgatewaysBuilder:
        """
        The cloudgateways property
        """
        from .cloudgateways.cloudgateways_builder import CloudgatewaysBuilder

        return CloudgatewaysBuilder(self._request_adapter)

    @property
    def cloudgatewaysetting(self) -> CloudgatewaysettingBuilder:
        """
        The cloudgatewaysetting property
        """
        from .cloudgatewaysetting.cloudgatewaysetting_builder import CloudgatewaysettingBuilder

        return CloudgatewaysettingBuilder(self._request_adapter)

    @property
    def cloudgatewaytype(self) -> CloudgatewaytypeBuilder:
        """
        The cloudgatewaytype property
        """
        from .cloudgatewaytype.cloudgatewaytype_builder import CloudgatewaytypeBuilder

        return CloudgatewaytypeBuilder(self._request_adapter)

    @property
    def config_group(self) -> ConfigGroupBuilder:
        """
        The config-group property
        """
        from .config_group.config_group_builder import ConfigGroupBuilder

        return ConfigGroupBuilder(self._request_adapter)

    @property
    def connected_sites(self) -> ConnectedSitesBuilder:
        """
        The connected-sites property
        """
        from .connected_sites.connected_sites_builder import ConnectedSitesBuilder

        return ConnectedSitesBuilder(self._request_adapter)

    @property
    def connectivity(self) -> ConnectivityBuilder:
        """
        The connectivity property
        """
        from .connectivity.connectivity_builder import ConnectivityBuilder

        return ConnectivityBuilder(self._request_adapter)

    @property
    def connectivitygateway(self) -> ConnectivitygatewayBuilder:
        """
        The connectivitygateway property
        """
        from .connectivitygateway.connectivitygateway_builder import ConnectivitygatewayBuilder

        return ConnectivitygatewayBuilder(self._request_adapter)

    @property
    def connectivitygatewaycreationoptions(self) -> ConnectivitygatewaycreationoptionsBuilder:
        """
        The connectivitygatewaycreationoptions property
        """
        from .connectivitygatewaycreationoptions.connectivitygatewaycreationoptions_builder import (
            ConnectivitygatewaycreationoptionsBuilder,
        )

        return ConnectivitygatewaycreationoptionsBuilder(self._request_adapter)

    @property
    def corenetworkpolicy(self) -> CorenetworkpolicyBuilder:
        """
        The corenetworkpolicy property
        """
        from .corenetworkpolicy.corenetworkpolicy_builder import CorenetworkpolicyBuilder

        return CorenetworkpolicyBuilder(self._request_adapter)

    @property
    def dashboard(self) -> DashboardBuilder:
        """
        The dashboard property
        """
        from .dashboard.dashboard_builder import DashboardBuilder

        return DashboardBuilder(self._request_adapter)

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def devicelink(self) -> DevicelinkBuilder:
        """
        The devicelink property
        """
        from .devicelink.devicelink_builder import DevicelinkBuilder

        return DevicelinkBuilder(self._request_adapter)

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)

    @property
    def edge(self) -> EdgeBuilder:
        """
        The edge property
        """
        from .edge.edge_builder import EdgeBuilder

        return EdgeBuilder(self._request_adapter)

    @property
    def gateway(self) -> GatewayBuilder:
        """
        The gateway property
        """
        from .gateway.gateway_builder import GatewayBuilder

        return GatewayBuilder(self._request_adapter)

    @property
    def gateways(self) -> GatewaysBuilder:
        """
        The gateways property
        """
        from .gateways.gateways_builder import GatewaysBuilder

        return GatewaysBuilder(self._request_adapter)

    @property
    def hostvpc(self) -> HostvpcBuilder:
        """
        The hostvpc property
        """
        from .hostvpc.hostvpc_builder import HostvpcBuilder

        return HostvpcBuilder(self._request_adapter)

    @property
    def imagename(self) -> ImagenameBuilder:
        """
        The imagename property
        """
        from .imagename.imagename_builder import ImagenameBuilder

        return ImagenameBuilder(self._request_adapter)

    @property
    def instancesize(self) -> InstancesizeBuilder:
        """
        The instancesize property
        """
        from .instancesize.instancesize_builder import InstancesizeBuilder

        return InstancesizeBuilder(self._request_adapter)

    @property
    def interconnect(self) -> InterconnectBuilder:
        """
        The interconnect property
        """
        from .interconnect.interconnect_builder import InterconnectBuilder

        return InterconnectBuilder(self._request_adapter)

    @property
    def interfacecolor(self) -> InterfacecolorBuilder:
        """
        The interfacecolor property
        """
        from .interfacecolor.interfacecolor_builder import InterfacecolorBuilder

        return InterfacecolorBuilder(self._request_adapter)

    @property
    def license(self) -> LicenseBuilder:
        """
        The license property
        """
        from .license.license_builder import LicenseBuilder

        return LicenseBuilder(self._request_adapter)

    @property
    def locations(self) -> LocationsBuilder:
        """
        The locations property
        """
        from .locations.locations_builder import LocationsBuilder

        return LocationsBuilder(self._request_adapter)

    @property
    def loopback_cgw_color(self) -> LoopbackCgwColorBuilder:
        """
        The loopbackCGWColor property
        """
        from .loopback_cgw_color.loopback_cgw_color_builder import LoopbackCgwColorBuilder

        return LoopbackCgwColorBuilder(self._request_adapter)

    @property
    def loopbacktransportcolor(self) -> LoopbacktransportcolorBuilder:
        """
        The loopbacktransportcolor property
        """
        from .loopbacktransportcolor.loopbacktransportcolor_builder import (
            LoopbacktransportcolorBuilder,
        )

        return LoopbacktransportcolorBuilder(self._request_adapter)

    @property
    def map(self) -> MapBuilder:
        """
        The map property
        """
        from .map.map_builder import MapBuilder

        return MapBuilder(self._request_adapter)

    @property
    def mapping(self) -> MappingBuilder:
        """
        The mapping property
        """
        from .mapping.mapping_builder import MappingBuilder

        return MappingBuilder(self._request_adapter)

    @property
    def partnerports(self) -> PartnerportsBuilder:
        """
        The partnerports property
        """
        from .partnerports.partnerports_builder import PartnerportsBuilder

        return PartnerportsBuilder(self._request_adapter)

    @property
    def port_speed(self) -> PortSpeedBuilder:
        """
        The portSpeed property
        """
        from .port_speed.port_speed_builder import PortSpeedBuilder

        return PortSpeedBuilder(self._request_adapter)

    @property
    def push_cgw_config(self) -> PushCgwConfigBuilder:
        """
        The pushCgwConfig property
        """
        from .push_cgw_config.push_cgw_config_builder import PushCgwConfigBuilder

        return PushCgwConfigBuilder(self._request_adapter)

    @property
    def regions(self) -> RegionsBuilder:
        """
        The regions property
        """
        from .regions.regions_builder import RegionsBuilder

        return RegionsBuilder(self._request_adapter)

    @property
    def settings(self) -> SettingsBuilder:
        """
        The settings property
        """
        from .settings.settings_builder import SettingsBuilder

        return SettingsBuilder(self._request_adapter)

    @property
    def site(self) -> SiteBuilder:
        """
        The site property
        """
        from .site.site_builder import SiteBuilder

        return SiteBuilder(self._request_adapter)

    @property
    def sshkeys(self) -> SshkeysBuilder:
        """
        The sshkeys property
        """
        from .sshkeys.sshkeys_builder import SshkeysBuilder

        return SshkeysBuilder(self._request_adapter)

    @property
    def statistics(self) -> StatisticsBuilder:
        """
        The statistics property
        """
        from .statistics.statistics_builder import StatisticsBuilder

        return StatisticsBuilder(self._request_adapter)

    @property
    def swimages(self) -> SwimagesBuilder:
        """
        The swimages property
        """
        from .swimages.swimages_builder import SwimagesBuilder

        return SwimagesBuilder(self._request_adapter)

    @property
    def telemetry(self) -> TelemetryBuilder:
        """
        The telemetry property
        """
        from .telemetry.telemetry_builder import TelemetryBuilder

        return TelemetryBuilder(self._request_adapter)

    @property
    def tunnels(self) -> TunnelsBuilder:
        """
        The tunnels property
        """
        from .tunnels.tunnels_builder import TunnelsBuilder

        return TunnelsBuilder(self._request_adapter)

    @property
    def types(self) -> TypesBuilder:
        """
        The types property
        """
        from .types.types_builder import TypesBuilder

        return TypesBuilder(self._request_adapter)

    @property
    def vhubs(self) -> VhubsBuilder:
        """
        The vhubs property
        """
        from .vhubs.vhubs_builder import VhubsBuilder

        return VhubsBuilder(self._request_adapter)

    @property
    def vwan(self) -> VwanBuilder:
        """
        The vwan property
        """
        from .vwan.vwan_builder import VwanBuilder

        return VwanBuilder(self._request_adapter)

    @property
    def vwans(self) -> VwansBuilder:
        """
        The vwans property
        """
        from .vwans.vwans_builder import VwansBuilder

        return VwansBuilder(self._request_adapter)

    @property
    def widget(self) -> WidgetBuilder:
        """
        The widget property
        """
        from .widget.widget_builder import WidgetBuilder

        return WidgetBuilder(self._request_adapter)
