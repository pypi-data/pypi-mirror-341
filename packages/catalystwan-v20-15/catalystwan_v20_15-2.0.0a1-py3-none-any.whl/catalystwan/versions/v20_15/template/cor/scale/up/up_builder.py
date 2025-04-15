# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class UpBuilder:
    """
    Builds and executes requests for operations under /template/cor/scale/up
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Scale up cloud on ramp
        POST /dataservice/template/cor/scale/up

        :param payload: Update VPC
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "scaleUp")
        return self._request_adapter.request(
            "POST", "/dataservice/template/cor/scale/up", payload=payload, **kw
        )
