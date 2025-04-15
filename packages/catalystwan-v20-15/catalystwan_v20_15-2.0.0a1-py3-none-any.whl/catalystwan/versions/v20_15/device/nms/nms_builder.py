# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .running.running_builder import RunningBuilder


class NmsBuilder:
    """
    Builds and executes requests for operations under /device/nms
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def running(self) -> RunningBuilder:
        """
        The running property
        """
        from .running.running_builder import RunningBuilder

        return RunningBuilder(self._request_adapter)
