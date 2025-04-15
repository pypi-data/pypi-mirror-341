# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .interface.interface_builder import InterfaceBuilder
    from .mac.mac_builder import MacBuilder
    from .table.table_builder import TableBuilder


class BridgeBuilder:
    """
    Builds and executes requests for operations under /device/bridge
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)

    @property
    def mac(self) -> MacBuilder:
        """
        The mac property
        """
        from .mac.mac_builder import MacBuilder

        return MacBuilder(self._request_adapter)

    @property
    def table(self) -> TableBuilder:
        """
        The table property
        """
        from .table.table_builder import TableBuilder

        return TableBuilder(self._request_adapter)
