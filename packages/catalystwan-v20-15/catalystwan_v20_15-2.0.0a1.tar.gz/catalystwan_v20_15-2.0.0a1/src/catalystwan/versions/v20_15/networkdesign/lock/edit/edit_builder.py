# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class EditBuilder:
    """
    Builds and executes requests for operations under /networkdesign/lock/edit
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> Any:
        """
        Acquire edit lock
        POST /dataservice/networkdesign/lock/edit

        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "acquireEditLock")
        return self._request_adapter.request("POST", "/dataservice/networkdesign/lock/edit", **kw)
