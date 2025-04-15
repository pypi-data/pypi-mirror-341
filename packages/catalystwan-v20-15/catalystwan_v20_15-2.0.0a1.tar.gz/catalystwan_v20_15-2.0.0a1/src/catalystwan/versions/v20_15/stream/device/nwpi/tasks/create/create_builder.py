# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import TasksCreateResponsePayload


class CreateBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/tasks/create
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> TasksCreateResponsePayload:
        """
        Task Action - Create
        POST /dataservice/stream/device/nwpi/tasks/create

        :param payload: Payload
        :returns: TasksCreateResponsePayload
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/stream/device/nwpi/tasks/create",
            return_type=TasksCreateResponsePayload,
            payload=payload,
            **kw,
        )
