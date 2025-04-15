# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse200

if TYPE_CHECKING:
    from .active_count.active_count_builder import ActiveCountBuilder
    from .clean.clean_builder import CleanBuilder


class TasksBuilder:
    """
    Builds and executes requests for operations under /device/action/status/tasks
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> InlineResponse200:
        """
        Find running tasks
        GET /dataservice/device/action/status/tasks

        :returns: InlineResponse200
        """
        return self._request_adapter.request(
            "GET", "/dataservice/device/action/status/tasks", return_type=InlineResponse200, **kw
        )

    @property
    def active_count(self) -> ActiveCountBuilder:
        """
        The activeCount property
        """
        from .active_count.active_count_builder import ActiveCountBuilder

        return ActiveCountBuilder(self._request_adapter)

    @property
    def clean(self) -> CleanBuilder:
        """
        The clean property
        """
        from .clean.clean_builder import CleanBuilder

        return CleanBuilder(self._request_adapter)
