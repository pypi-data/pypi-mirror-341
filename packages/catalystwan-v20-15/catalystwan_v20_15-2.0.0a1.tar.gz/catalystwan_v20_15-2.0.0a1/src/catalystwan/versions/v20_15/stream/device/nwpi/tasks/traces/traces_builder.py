# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import TaskTracesResponsePayload


class TracesBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/tasks/{taskId}/traces
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, task_id: str, **kw) -> TaskTracesResponsePayload:
        """
        Get all traces in one task
        GET /dataservice/stream/device/nwpi/tasks/{taskId}/traces

        :param task_id: taskId
        :returns: TaskTracesResponsePayload
        """
        params = {
            "taskId": task_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/tasks/{taskId}/traces",
            return_type=TaskTracesResponsePayload,
            params=params,
            **kw,
        )
