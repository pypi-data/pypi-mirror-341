# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .delete.delete_builder import DeleteBuilder
    from .record.record_builder import RecordBuilder
    from .start.start_builder import StartBuilder
    from .stop.stop_builder import StopBuilder


class TraceBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/trace
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def delete(self) -> DeleteBuilder:
        """
        The delete property
        """
        from .delete.delete_builder import DeleteBuilder

        return DeleteBuilder(self._request_adapter)

    @property
    def record(self) -> RecordBuilder:
        """
        The record property
        """
        from .record.record_builder import RecordBuilder

        return RecordBuilder(self._request_adapter)

    @property
    def start(self) -> StartBuilder:
        """
        The start property
        """
        from .start.start_builder import StartBuilder

        return StartBuilder(self._request_adapter)

    @property
    def stop(self) -> StopBuilder:
        """
        The stop property
        """
        from .stop.stop_builder import StopBuilder

        return StopBuilder(self._request_adapter)
