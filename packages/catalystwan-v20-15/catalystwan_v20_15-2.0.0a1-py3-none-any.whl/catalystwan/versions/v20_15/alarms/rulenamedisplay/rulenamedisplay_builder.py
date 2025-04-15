# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .keyvalue.keyvalue_builder import KeyvalueBuilder


class RulenamedisplayBuilder:
    """
    Builds and executes requests for operations under /alarms/rulenamedisplay
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def keyvalue(self) -> KeyvalueBuilder:
        """
        The keyvalue property
        """
        from .keyvalue.keyvalue_builder import KeyvalueBuilder

        return KeyvalueBuilder(self._request_adapter)
