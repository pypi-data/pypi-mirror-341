# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .auto.auto_builder import AutoBuilder
    from .manual.manual_builder import ManualBuilder


class ModeBuilder:
    """
    Builds and executes requests for operations under /device/action/software/package/utdsignature/{type}/mode
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def auto(self) -> AutoBuilder:
        """
        The auto property
        """
        from .auto.auto_builder import AutoBuilder

        return AutoBuilder(self._request_adapter)

    @property
    def manual(self) -> ManualBuilder:
        """
        The manual property
        """
        from .manual.manual_builder import ManualBuilder

        return ManualBuilder(self._request_adapter)
