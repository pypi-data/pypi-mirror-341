# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .action.action_builder import ActionBuilder
    from .rangefrom.rangefrom_builder import RangefromBuilder
    from .settings.settings_builder import SettingsBuilder
    from .statsdbinfo.statsdbinfo_builder import StatsdbinfoBuilder
    from .status.status_builder import StatusBuilder


class MigrationBuilder:
    """
    Builds and executes requests for operations under /util/olapdb/migration
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def action(self) -> ActionBuilder:
        """
        The action property
        """
        from .action.action_builder import ActionBuilder

        return ActionBuilder(self._request_adapter)

    @property
    def rangefrom(self) -> RangefromBuilder:
        """
        The rangefrom property
        """
        from .rangefrom.rangefrom_builder import RangefromBuilder

        return RangefromBuilder(self._request_adapter)

    @property
    def settings(self) -> SettingsBuilder:
        """
        The settings property
        """
        from .settings.settings_builder import SettingsBuilder

        return SettingsBuilder(self._request_adapter)

    @property
    def statsdbinfo(self) -> StatsdbinfoBuilder:
        """
        The statsdbinfo property
        """
        from .statsdbinfo.statsdbinfo_builder import StatsdbinfoBuilder

        return StatsdbinfoBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)
