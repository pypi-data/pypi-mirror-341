# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .mode.mode_builder import ModeBuilder


class UtdsignatureBuilder:
    """
    Builds and executes requests for operations under /device/action/software/package/utdsignature
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def mode(self) -> ModeBuilder:
        """
        The mode property
        """
        from .mode.mode_builder import ModeBuilder

        return ModeBuilder(self._request_adapter)
