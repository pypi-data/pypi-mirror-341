# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NwpiSettingDataPayload


class NwpiSettingViewBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/nwpiSettingView
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, type_: Optional[str] = None, **kw) -> NwpiSettingDataPayload:
        """
        get NWPI setting
        GET /dataservice/stream/device/nwpi/nwpiSettingView

        :param type_: setting type
        :returns: NwpiSettingDataPayload
        """
        logging.warning("Operation: %s is deprecated", "nwpiSettingView")
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/nwpiSettingView",
            return_type=NwpiSettingDataPayload,
            params=params,
            **kw,
        )
