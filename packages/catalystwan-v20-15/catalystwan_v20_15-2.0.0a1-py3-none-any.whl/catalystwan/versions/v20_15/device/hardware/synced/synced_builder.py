# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .alarms.alarms_builder import AlarmsBuilder
    from .environment.environment_builder import EnvironmentBuilder
    from .inventory.inventory_builder import InventoryBuilder


class SyncedBuilder:
    """
    Builds and executes requests for operations under /device/hardware/synced
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def alarms(self) -> AlarmsBuilder:
        """
        The alarms property
        """
        from .alarms.alarms_builder import AlarmsBuilder

        return AlarmsBuilder(self._request_adapter)

    @property
    def environment(self) -> EnvironmentBuilder:
        """
        The environment property
        """
        from .environment.environment_builder import EnvironmentBuilder

        return EnvironmentBuilder(self._request_adapter)

    @property
    def inventory(self) -> InventoryBuilder:
        """
        The inventory property
        """
        from .inventory.inventory_builder import InventoryBuilder

        return InventoryBuilder(self._request_adapter)
