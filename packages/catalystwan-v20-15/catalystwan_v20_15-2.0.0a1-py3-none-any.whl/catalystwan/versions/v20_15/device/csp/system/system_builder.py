# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .native.native_builder import NativeBuilder
    from .processlist.processlist_builder import ProcesslistBuilder
    from .settings.settings_builder import SettingsBuilder
    from .status.status_builder import StatusBuilder


class SystemBuilder:
    """
    Builds and executes requests for operations under /device/csp/system
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def native(self) -> NativeBuilder:
        """
        The native property
        """
        from .native.native_builder import NativeBuilder

        return NativeBuilder(self._request_adapter)

    @property
    def processlist(self) -> ProcesslistBuilder:
        """
        The processlist property
        """
        from .processlist.processlist_builder import ProcesslistBuilder

        return ProcesslistBuilder(self._request_adapter)

    @property
    def settings(self) -> SettingsBuilder:
        """
        The settings property
        """
        from .settings.settings_builder import SettingsBuilder

        return SettingsBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)
