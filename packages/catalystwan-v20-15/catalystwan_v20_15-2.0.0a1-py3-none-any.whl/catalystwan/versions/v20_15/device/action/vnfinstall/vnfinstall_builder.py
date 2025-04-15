# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class VnfinstallBuilder:
    """
    Builds and executes requests for operations under /device/action/vnfinstall
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Process an installation operation
        POST /dataservice/device/action/vnfinstall

        :param payload: Installation request payload
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "processVnfInstall")
        return self._request_adapter.request(
            "POST", "/dataservice/device/action/vnfinstall", payload=payload, **kw
        )
