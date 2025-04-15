# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .mp.mp_builder import MpBuilder


class CfmBuilder:
    """
    Builds and executes requests for operations under /device/cfm
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def mp(self) -> MpBuilder:
        """
        The mp property
        """
        from .mp.mp_builder import MpBuilder

        return MpBuilder(self._request_adapter)
