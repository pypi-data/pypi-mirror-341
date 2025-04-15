# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DebugLogPostRequest


class DebuglogBuilder:
    """
    Builds and executes requests for operations under /util/logging/debuglog
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: DebugLogPostRequest, **kw):
        """
        Test whether logging works
        POST /dataservice/util/logging/debuglog

        :param payload: Payload
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "debugLog")
        return self._request_adapter.request(
            "POST", "/dataservice/util/logging/debuglog", payload=payload, **kw
        )
