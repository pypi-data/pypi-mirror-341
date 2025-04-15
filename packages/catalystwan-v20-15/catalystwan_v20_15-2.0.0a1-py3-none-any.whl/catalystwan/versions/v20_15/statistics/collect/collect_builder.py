# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .thread.thread_builder import ThreadBuilder


class CollectBuilder:
    """
    Builds and executes requests for operations under /statistics/collect
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Start stats collect
        GET /dataservice/statistics/collect

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/statistics/collect", **kw)

    @property
    def thread(self) -> ThreadBuilder:
        """
        The thread property
        """
        from .thread.thread_builder import ThreadBuilder

        return ThreadBuilder(self._request_adapter)
