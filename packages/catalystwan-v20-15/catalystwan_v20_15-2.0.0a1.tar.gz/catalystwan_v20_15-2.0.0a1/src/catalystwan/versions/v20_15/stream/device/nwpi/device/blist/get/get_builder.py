# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceBlistResponsePayloadInner


class GetBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/device/blist/get
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[DeviceBlistResponsePayloadInner]:
        """
        Get Device BlackList for NWPI.
        GET /dataservice/stream/device/nwpi/device/blist/get

        :returns: List[DeviceBlistResponsePayloadInner]
        """
        logging.warning("Operation: %s is deprecated", "getDeviceBList")
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/device/blist/get",
            return_type=List[DeviceBlistResponsePayloadInner],
            **kw,
        )
