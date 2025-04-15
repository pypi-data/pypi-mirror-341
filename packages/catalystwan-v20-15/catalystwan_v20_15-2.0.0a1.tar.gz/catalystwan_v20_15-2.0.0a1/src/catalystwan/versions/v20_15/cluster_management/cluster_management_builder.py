# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cluster_locked.cluster_locked_builder import ClusterLockedBuilder
    from .clusterworkflow.clusterworkflow_builder import ClusterworkflowBuilder
    from .configure.configure_builder import ConfigureBuilder
    from .connected_devices.connected_devices_builder import ConnectedDevicesBuilder
    from .health.health_builder import HealthBuilder
    from .host.host_builder import HostBuilder
    from .iplist.iplist_builder import IplistBuilder
    from .isready.isready_builder import IsreadyBuilder
    from .list.list_builder import ListBuilder
    from .node_properties.node_properties_builder import NodePropertiesBuilder
    from .remove.remove_builder import RemoveBuilder
    from .replicate_and_rebalance.replicate_and_rebalance_builder import (
        ReplicateAndRebalanceBuilder,
    )
    from .setup.setup_builder import SetupBuilder
    from .tenancy.tenancy_builder import TenancyBuilder
    from .tenant_list.tenant_list_builder import TenantListBuilder
    from .user_creds.user_creds_builder import UserCredsBuilder
    from .v_manage.v_manage_builder import VManageBuilder


class ClusterManagementBuilder:
    """
    Builds and executes requests for operations under /clusterManagement
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def cluster_locked(self) -> ClusterLockedBuilder:
        """
        The clusterLocked property
        """
        from .cluster_locked.cluster_locked_builder import ClusterLockedBuilder

        return ClusterLockedBuilder(self._request_adapter)

    @property
    def clusterworkflow(self) -> ClusterworkflowBuilder:
        """
        The clusterworkflow property
        """
        from .clusterworkflow.clusterworkflow_builder import ClusterworkflowBuilder

        return ClusterworkflowBuilder(self._request_adapter)

    @property
    def configure(self) -> ConfigureBuilder:
        """
        The configure property
        """
        from .configure.configure_builder import ConfigureBuilder

        return ConfigureBuilder(self._request_adapter)

    @property
    def connected_devices(self) -> ConnectedDevicesBuilder:
        """
        The connectedDevices property
        """
        from .connected_devices.connected_devices_builder import ConnectedDevicesBuilder

        return ConnectedDevicesBuilder(self._request_adapter)

    @property
    def health(self) -> HealthBuilder:
        """
        The health property
        """
        from .health.health_builder import HealthBuilder

        return HealthBuilder(self._request_adapter)

    @property
    def host(self) -> HostBuilder:
        """
        The host property
        """
        from .host.host_builder import HostBuilder

        return HostBuilder(self._request_adapter)

    @property
    def iplist(self) -> IplistBuilder:
        """
        The iplist property
        """
        from .iplist.iplist_builder import IplistBuilder

        return IplistBuilder(self._request_adapter)

    @property
    def isready(self) -> IsreadyBuilder:
        """
        The isready property
        """
        from .isready.isready_builder import IsreadyBuilder

        return IsreadyBuilder(self._request_adapter)

    @property
    def list(self) -> ListBuilder:
        """
        The list property
        """
        from .list.list_builder import ListBuilder

        return ListBuilder(self._request_adapter)

    @property
    def node_properties(self) -> NodePropertiesBuilder:
        """
        The nodeProperties property
        """
        from .node_properties.node_properties_builder import NodePropertiesBuilder

        return NodePropertiesBuilder(self._request_adapter)

    @property
    def remove(self) -> RemoveBuilder:
        """
        The remove property
        """
        from .remove.remove_builder import RemoveBuilder

        return RemoveBuilder(self._request_adapter)

    @property
    def replicate_and_rebalance(self) -> ReplicateAndRebalanceBuilder:
        """
        The replicateAndRebalance property
        """
        from .replicate_and_rebalance.replicate_and_rebalance_builder import (
            ReplicateAndRebalanceBuilder,
        )

        return ReplicateAndRebalanceBuilder(self._request_adapter)

    @property
    def setup(self) -> SetupBuilder:
        """
        The setup property
        """
        from .setup.setup_builder import SetupBuilder

        return SetupBuilder(self._request_adapter)

    @property
    def tenancy(self) -> TenancyBuilder:
        """
        The tenancy property
        """
        from .tenancy.tenancy_builder import TenancyBuilder

        return TenancyBuilder(self._request_adapter)

    @property
    def tenant_list(self) -> TenantListBuilder:
        """
        The tenantList property
        """
        from .tenant_list.tenant_list_builder import TenantListBuilder

        return TenantListBuilder(self._request_adapter)

    @property
    def user_creds(self) -> UserCredsBuilder:
        """
        The userCreds property
        """
        from .user_creds.user_creds_builder import UserCredsBuilder

        return UserCredsBuilder(self._request_adapter)

    @property
    def v_manage(self) -> VManageBuilder:
        """
        The vManage property
        """
        from .v_manage.v_manage_builder import VManageBuilder

        return VManageBuilder(self._request_adapter)
