# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .nics.nics_builder import NicsBuilder
    from .notifications.notifications_builder import NotificationsBuilder
    from .oper.oper_builder import OperBuilder
    from .state.state_builder import StateBuilder


class VmBuilder:
    """
    Builds and executes requests for operations under /device/vm
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def nics(self) -> NicsBuilder:
        """
        The nics property
        """
        from .nics.nics_builder import NicsBuilder

        return NicsBuilder(self._request_adapter)

    @property
    def notifications(self) -> NotificationsBuilder:
        """
        The notifications property
        """
        from .notifications.notifications_builder import NotificationsBuilder

        return NotificationsBuilder(self._request_adapter)

    @property
    def oper(self) -> OperBuilder:
        """
        The oper property
        """
        from .oper.oper_builder import OperBuilder

        return OperBuilder(self._request_adapter)

    @property
    def state(self) -> StateBuilder:
        """
        The state property
        """
        from .state.state_builder import StateBuilder

        return StateBuilder(self._request_adapter)
