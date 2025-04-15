# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import TasksDeleteResponsePayload


class DeleteBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/tasks/delete
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(self, task_id: str, **kw) -> TasksDeleteResponsePayload:
        """
        Delete Auto On Task
        DELETE /dataservice/stream/device/nwpi/tasks/delete/{taskId}

        :param task_id: taskId
        :returns: TasksDeleteResponsePayload
        """
        params = {
            "taskId": task_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/stream/device/nwpi/tasks/delete/{taskId}",
            return_type=TasksDeleteResponsePayload,
            params=params,
            **kw,
        )
