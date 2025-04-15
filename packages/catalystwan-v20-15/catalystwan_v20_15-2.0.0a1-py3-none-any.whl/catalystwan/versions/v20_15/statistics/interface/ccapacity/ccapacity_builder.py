# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .distribution.distribution_builder import DistributionBuilder


class CcapacityBuilder:
    """
    Builds and executes requests for operations under /statistics/interface/ccapacity
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def distribution(self) -> DistributionBuilder:
        """
        The distribution property
        """
        from .distribution.distribution_builder import DistributionBuilder

        return DistributionBuilder(self._request_adapter)
