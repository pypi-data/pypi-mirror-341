# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class OptoutBuilder:
    """
    Builds and executes requests for operations under /cloudservices/telemetry/optout
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(self, payload: Optional[str] = None, **kw) -> Any:
        """
        Telemetry Opt Out
        DELETE /dataservice/cloudservices/telemetry/optout

        :param payload: Payload
        :returns: Any
        """
        return self._request_adapter.request(
            "DELETE", "/dataservice/cloudservices/telemetry/optout", payload=payload, **kw
        )
