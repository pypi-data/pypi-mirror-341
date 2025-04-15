# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface


class AppFwdCflowdV6FlowsBuilder:
    """
    Builds and executes requests for operations under /device/cedgecflowd/app-fwd-cflowd-v6-flows
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        vpn_id: Optional[int] = None,
        src_addr: Optional[str] = None,
        dst_addr: Optional[str] = None,
        app: Optional[str] = None,
        family: Optional[str] = None,
        **kw,
    ):
        """
        Get list of app fwd cflowd v6 flows from device
        GET /dataservice/device/cedgecflowd/app-fwd-cflowd-v6-flows

        :param device_id: Device id
        :param vpn_id: Vpn id
        :param src_addr: Src addr
        :param dst_addr: Dst addr
        :param app: App
        :param family: Family
        :returns: None
        """
        params = {
            "deviceId": device_id,
            "vpn-id": vpn_id,
            "src-addr": src_addr,
            "dst-addr": dst_addr,
            "app": app,
            "family": family,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/cedgecflowd/app-fwd-cflowd-v6-flows", params=params, **kw
        )
