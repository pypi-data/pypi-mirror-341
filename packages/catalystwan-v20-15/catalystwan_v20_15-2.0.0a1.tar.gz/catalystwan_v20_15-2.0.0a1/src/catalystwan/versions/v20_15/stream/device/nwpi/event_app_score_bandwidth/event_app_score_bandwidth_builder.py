# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EventAppScoreBandwidthResponsePayloadInner


class EventAppScoreBandwidthBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/eventAppScoreBandwidth
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        trace_id: int,
        timestamp: int,
        received_timestamp: int,
        state: Optional[str] = None,
        server_side_key: Optional[str] = None,
        client_side_key: Optional[str] = None,
        version: Optional[str] = None,
        vpn: Optional[str] = None,
        **kw,
    ) -> List[EventAppScoreBandwidthResponsePayloadInner]:
        """
        Get Trace Event Application Performance Score and Bandwidth for NWPI.
        GET /dataservice/stream/device/nwpi/eventAppScoreBandwidth

        :param trace_id: Trace id
        :param timestamp: Timestamp
        :param received_timestamp: Received timestamp
        :param state: State
        :param server_side_key: Server side key
        :param client_side_key: Client side key
        :param version: Version
        :param vpn: Vpn
        :returns: List[EventAppScoreBandwidthResponsePayloadInner]
        """
        logging.warning("Operation: %s is deprecated", "getEventAppScoreBandwidth")
        params = {
            "traceId": trace_id,
            "timestamp": timestamp,
            "receivedTimestamp": received_timestamp,
            "state": state,
            "serverSideKey": server_side_key,
            "clientSideKey": client_side_key,
            "version": version,
            "vpn": vpn,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/eventAppScoreBandwidth",
            return_type=List[EventAppScoreBandwidthResponsePayloadInner],
            params=params,
            **kw,
        )
