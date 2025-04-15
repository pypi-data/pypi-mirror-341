# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EventFlowFromAppHopResponsePayloadInner


class EventFlowFromAppHopBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/eventFlowFromAppHop
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        trace_id: int,
        timestamp: int,
        direction: str,
        from_: str,
        to: str,
        device_trace_id: int,
        state: Optional[str] = None,
        application: Optional[str] = None,
        version: Optional[str] = None,
        server_side_key: Optional[str] = None,
        client_side_key: Optional[str] = None,
        vpn: Optional[str] = None,
        **kw,
    ) -> List[EventFlowFromAppHopResponsePayloadInner]:
        """
        Get Trace Event Flow From Application And Hop for NWPI.
        GET /dataservice/stream/device/nwpi/eventFlowFromAppHop

        :param trace_id: Trace id
        :param timestamp: Timestamp
        :param direction: Direction
        :param from_: From
        :param to: To
        :param device_trace_id: Device trace id
        :param state: State
        :param application: Application
        :param version: Version
        :param server_side_key: Server side key
        :param client_side_key: Client side key
        :param vpn: Vpn
        :returns: List[EventFlowFromAppHopResponsePayloadInner]
        """
        logging.warning("Operation: %s is deprecated", "getEventFlowFromAppHop")
        params = {
            "traceId": trace_id,
            "timestamp": timestamp,
            "direction": direction,
            "from": from_,
            "to": to,
            "deviceTraceId": device_trace_id,
            "state": state,
            "application": application,
            "version": version,
            "serverSideKey": server_side_key,
            "clientSideKey": client_side_key,
            "vpn": vpn,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/eventFlowFromAppHop",
            return_type=List[EventFlowFromAppHopResponsePayloadInner],
            params=params,
            **kw,
        )
