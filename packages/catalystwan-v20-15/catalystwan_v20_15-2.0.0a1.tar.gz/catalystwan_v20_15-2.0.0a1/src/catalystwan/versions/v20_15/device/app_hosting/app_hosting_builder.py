# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .attached_devices.attached_devices_builder import AttachedDevicesBuilder
    from .details.details_builder import DetailsBuilder
    from .guest_routes.guest_routes_builder import GuestRoutesBuilder
    from .network_interfaces.network_interfaces_builder import NetworkInterfacesBuilder
    from .network_utilization.network_utilization_builder import NetworkUtilizationBuilder
    from .processes.processes_builder import ProcessesBuilder
    from .storage_utilization.storage_utilization_builder import StorageUtilizationBuilder
    from .utilization.utilization_builder import UtilizationBuilder


class AppHostingBuilder:
    """
    Builds and executes requests for operations under /device/app-hosting
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def attached_devices(self) -> AttachedDevicesBuilder:
        """
        The attached-devices property
        """
        from .attached_devices.attached_devices_builder import AttachedDevicesBuilder

        return AttachedDevicesBuilder(self._request_adapter)

    @property
    def details(self) -> DetailsBuilder:
        """
        The details property
        """
        from .details.details_builder import DetailsBuilder

        return DetailsBuilder(self._request_adapter)

    @property
    def guest_routes(self) -> GuestRoutesBuilder:
        """
        The guest-routes property
        """
        from .guest_routes.guest_routes_builder import GuestRoutesBuilder

        return GuestRoutesBuilder(self._request_adapter)

    @property
    def network_interfaces(self) -> NetworkInterfacesBuilder:
        """
        The network-interfaces property
        """
        from .network_interfaces.network_interfaces_builder import NetworkInterfacesBuilder

        return NetworkInterfacesBuilder(self._request_adapter)

    @property
    def network_utilization(self) -> NetworkUtilizationBuilder:
        """
        The network-utilization property
        """
        from .network_utilization.network_utilization_builder import NetworkUtilizationBuilder

        return NetworkUtilizationBuilder(self._request_adapter)

    @property
    def processes(self) -> ProcessesBuilder:
        """
        The processes property
        """
        from .processes.processes_builder import ProcessesBuilder

        return ProcessesBuilder(self._request_adapter)

    @property
    def storage_utilization(self) -> StorageUtilizationBuilder:
        """
        The storage-utilization property
        """
        from .storage_utilization.storage_utilization_builder import StorageUtilizationBuilder

        return StorageUtilizationBuilder(self._request_adapter)

    @property
    def utilization(self) -> UtilizationBuilder:
        """
        The utilization property
        """
        from .utilization.utilization_builder import UtilizationBuilder

        return UtilizationBuilder(self._request_adapter)
