# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .activate.activate_builder import ActivateBuilder
    from .approve.approve_builder import ApproveBuilder
    from .create.create_builder import CreateBuilder


class PxgridBuilder:
    """
    Builds and executes requests for operations under /ise/pxgrid
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def activate(self) -> ActivateBuilder:
        """
        The activate property
        """
        from .activate.activate_builder import ActivateBuilder

        return ActivateBuilder(self._request_adapter)

    @property
    def approve(self) -> ApproveBuilder:
        """
        The approve property
        """
        from .approve.approve_builder import ApproveBuilder

        return ApproveBuilder(self._request_adapter)

    @property
    def create(self) -> CreateBuilder:
        """
        The create property
        """
        from .create.create_builder import CreateBuilder

        return CreateBuilder(self._request_adapter)
