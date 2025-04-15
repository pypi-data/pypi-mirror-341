# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .create.create_builder import CreateBuilder
    from .delete.delete_builder import DeleteBuilder
    from .event_stats_data.event_stats_data_builder import EventStatsDataBuilder
    from .stop.stop_builder import StopBuilder
    from .task_history.task_history_builder import TaskHistoryBuilder
    from .traces.traces_builder import TracesBuilder


class TasksBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/tasks
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def create(self) -> CreateBuilder:
        """
        The create property
        """
        from .create.create_builder import CreateBuilder

        return CreateBuilder(self._request_adapter)

    @property
    def delete(self) -> DeleteBuilder:
        """
        The delete property
        """
        from .delete.delete_builder import DeleteBuilder

        return DeleteBuilder(self._request_adapter)

    @property
    def event_stats_data(self) -> EventStatsDataBuilder:
        """
        The eventStatsData property
        """
        from .event_stats_data.event_stats_data_builder import EventStatsDataBuilder

        return EventStatsDataBuilder(self._request_adapter)

    @property
    def stop(self) -> StopBuilder:
        """
        The stop property
        """
        from .stop.stop_builder import StopBuilder

        return StopBuilder(self._request_adapter)

    @property
    def task_history(self) -> TaskHistoryBuilder:
        """
        The taskHistory property
        """
        from .task_history.task_history_builder import TaskHistoryBuilder

        return TaskHistoryBuilder(self._request_adapter)

    @property
    def traces(self) -> TracesBuilder:
        """
        The traces property
        """
        from .traces.traces_builder import TracesBuilder

        return TracesBuilder(self._request_adapter)
