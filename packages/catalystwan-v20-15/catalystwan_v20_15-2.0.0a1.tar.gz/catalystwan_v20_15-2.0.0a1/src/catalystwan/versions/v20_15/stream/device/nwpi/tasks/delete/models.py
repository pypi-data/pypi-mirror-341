# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Optional


@dataclass
class TasksDeleteResponsePayloadMessage:
    duration: Optional[str] = _field(default=None)
    entry_time: Optional[int] = _field(default=None)
    events: Optional[str] = _field(default=None)
    expire_time: Optional[int] = _field(default=None, metadata={"alias": "expire-time"})
    message: Optional[str] = _field(default=None)
    sites: Optional[str] = _field(default=None)
    state: Optional[str] = _field(default=None)
    task_id: Optional[int] = _field(default=None, metadata={"alias": "taskId"})
    task_name: Optional[str] = _field(default=None, metadata={"alias": "taskName"})
    traces: Optional[bool] = _field(default=None)


@dataclass
class TasksDeleteResponsePayload:
    """
    Auto on task schema for DELETE response
    """

    action: Optional[str] = _field(default=None)
    message: Optional[TasksDeleteResponsePayloadMessage] = _field(default=None)
    task_id: Optional[str] = _field(default=None, metadata={"alias": "taskId"})
