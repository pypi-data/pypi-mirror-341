# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NwpiSettingDataPayload


class UpsertSettingBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/upsertSetting
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: NwpiSettingDataPayload, **kw):
        """
        insert or update setting
        POST /dataservice/stream/device/nwpi/upsertSetting

        :param payload: Payload
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "upsertSetting")
        return self._request_adapter.request(
            "POST", "/dataservice/stream/device/nwpi/upsertSetting", payload=payload, **kw
        )
