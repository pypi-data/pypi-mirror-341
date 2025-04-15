# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .crashlog.crashlog_builder import CrashlogBuilder


class DeviceBuilder:
    """
    Builds and executes requests for operations under /dca/device
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> List[Any]:
        """
        Get all devices
        POST /dataservice/dca/device

        :param payload: Query string
        :returns: List[Any]
        """
        return self._request_adapter.request(
            "POST", "/dataservice/dca/device", return_type=List[Any], payload=payload, **kw
        )

    @property
    def crashlog(self) -> CrashlogBuilder:
        """
        The crashlog property
        """
        from .crashlog.crashlog_builder import CrashlogBuilder

        return CrashlogBuilder(self._request_adapter)
