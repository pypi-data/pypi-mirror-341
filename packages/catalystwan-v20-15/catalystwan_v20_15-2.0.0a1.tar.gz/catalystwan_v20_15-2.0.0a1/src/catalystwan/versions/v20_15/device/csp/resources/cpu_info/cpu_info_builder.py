# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .allocation.allocation_builder import AllocationBuilder
    from .cpus.cpus_builder import CpusBuilder
    from .vnfs.vnfs_builder import VnfsBuilder


class CpuInfoBuilder:
    """
    Builds and executes requests for operations under /device/csp/resources/cpu-info
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def allocation(self) -> AllocationBuilder:
        """
        The allocation property
        """
        from .allocation.allocation_builder import AllocationBuilder

        return AllocationBuilder(self._request_adapter)

    @property
    def cpus(self) -> CpusBuilder:
        """
        The cpus property
        """
        from .cpus.cpus_builder import CpusBuilder

        return CpusBuilder(self._request_adapter)

    @property
    def vnfs(self) -> VnfsBuilder:
        """
        The vnfs property
        """
        from .vnfs.vnfs_builder import VnfsBuilder

        return VnfsBuilder(self._request_adapter)
