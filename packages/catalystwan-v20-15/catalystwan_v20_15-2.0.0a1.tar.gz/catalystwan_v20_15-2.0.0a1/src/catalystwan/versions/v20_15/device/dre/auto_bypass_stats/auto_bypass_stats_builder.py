# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class AutoBypassStatsBuilder:
    """
    Builds and executes requests for operations under /device/dre/auto-bypass-stats
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        appqoe_dre_auto_bypass_server_ip: Optional[str] = None,
        appqoe_dre_auto_bypass_port: Optional[int] = None,
        **kw,
    ) -> Any:
        """
        Get DRE auto-bypass statistics
        GET /dataservice/device/dre/auto-bypass-stats

        :param appqoe_dre_auto_bypass_server_ip: Server IP
        :param appqoe_dre_auto_bypass_port: Port
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "appqoe-dre-auto-bypass-server-ip": appqoe_dre_auto_bypass_server_ip,
            "appqoe-dre-auto-bypass-port": appqoe_dre_auto_bypass_port,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/dre/auto-bypass-stats", params=params, **kw
        )
