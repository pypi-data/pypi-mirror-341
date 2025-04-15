# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .state.state_builder import StateBuilder


class OperBuilder:
    """
    Builds and executes requests for operations under /device/vm/oper
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def state(self) -> StateBuilder:
        """
        The state property
        """
        from .state.state_builder import StateBuilder

        return StateBuilder(self._request_adapter)
