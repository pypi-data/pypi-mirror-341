# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .count.count_builder import CountBuilder
    from .status.status_builder import StatusBuilder


class TaskBuilder:
    """
    Builds and executes requests for operations under /networkdesign/profile/task
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def count(self) -> CountBuilder:
        """
        The count property
        """
        from .count.count_builder import CountBuilder

        return CountBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)
