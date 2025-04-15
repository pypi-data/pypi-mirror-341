# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EventName


class PollBuilder:
    """
    Builds and executes requests for operations under /serverlongpoll/event/poll
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        partner_id: str,
        event_id: Optional[str] = None,
        event_names: Optional[List[EventName]] = None,
        wait_time: Optional[int] = 0,
        **kw,
    ):
        """
        Retrieve registration change information
        GET /dataservice/serverlongpoll/event/poll/{partnerId}

        :param partner_id: Partner Id
        :param event_id: Continuation token of ongoing event-polling session
        :param event_names: Names of type of events to filter on
        :param wait_time: Maximum polling wait time in seconds
        :returns: None
        """
        params = {
            "partnerId": partner_id,
            "event_id": event_id,
            "eventNames": event_names,
            "wait_time": wait_time,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/serverlongpoll/event/poll/{partnerId}", params=params, **kw
        )
