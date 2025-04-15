# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .attachedconfig.attachedconfig_builder import AttachedconfigBuilder


class ConfigBuilder:
    """
    Builds and executes requests for operations under /dca/template/device/config
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def attachedconfig(self) -> AttachedconfigBuilder:
        """
        The attachedconfig property
        """
        from .attachedconfig.attachedconfig_builder import AttachedconfigBuilder

        return AttachedconfigBuilder(self._request_adapter)
