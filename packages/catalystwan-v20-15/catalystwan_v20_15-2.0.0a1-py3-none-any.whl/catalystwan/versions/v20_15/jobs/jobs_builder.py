# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .batch.batch_builder import BatchBuilder


class JobsBuilder:
    """
    Builds and executes requests for operations under /jobs
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def batch(self) -> BatchBuilder:
        """
        The batch property
        """
        from .batch.batch_builder import BatchBuilder

        return BatchBuilder(self._request_adapter)
