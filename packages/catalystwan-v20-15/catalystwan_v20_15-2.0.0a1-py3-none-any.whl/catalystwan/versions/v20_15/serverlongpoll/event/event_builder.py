# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .poll.poll_builder import PollBuilder


class EventBuilder:
    """
    Builds and executes requests for operations under /serverlongpoll/event
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def poll(self) -> PollBuilder:
        """
        The poll property
        """
        from .poll.poll_builder import PollBuilder

        return PollBuilder(self._request_adapter)
