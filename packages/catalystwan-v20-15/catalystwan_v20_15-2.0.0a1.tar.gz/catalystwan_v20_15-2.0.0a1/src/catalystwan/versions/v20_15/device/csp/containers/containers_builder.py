# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .container.container_builder import ContainerBuilder


class ContainersBuilder:
    """
    Builds and executes requests for operations under /device/csp/containers
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def container(self) -> ContainerBuilder:
        """
        The container property
        """
        from .container.container_builder import ContainerBuilder

        return ContainerBuilder(self._request_adapter)
