# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .hostvpc.hostvpc_builder import HostvpcBuilder


class DevicepairBuilder:
    """
    Builds and executes requests for operations under /template/cor/devicepair
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Add device pair
        POST /dataservice/template/cor/devicepair

        :param payload: Add device pair request
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "addDevicePair")
        return self._request_adapter.request(
            "POST", "/dataservice/template/cor/devicepair", payload=payload, **kw
        )

    @property
    def hostvpc(self) -> HostvpcBuilder:
        """
        The hostvpc property
        """
        from .hostvpc.hostvpc_builder import HostvpcBuilder

        return HostvpcBuilder(self._request_adapter)
