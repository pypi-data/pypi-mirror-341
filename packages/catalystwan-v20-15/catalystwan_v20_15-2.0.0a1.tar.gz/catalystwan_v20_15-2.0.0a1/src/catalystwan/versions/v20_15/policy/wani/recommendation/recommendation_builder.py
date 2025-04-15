# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .process.process_builder import ProcessBuilder


class RecommendationBuilder:
    """
    Builds and executes requests for operations under /policy/wani/recommendation
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def process(self) -> ProcessBuilder:
        """
        The process property
        """
        from .process.process_builder import ProcessBuilder

        return ProcessBuilder(self._request_adapter)
