# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class AttachedconfigBuilder:
    """
    Builds and executes requests for operations under /template/device/config/attachedconfig
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, policy_id: Optional[str] = None, **kw) -> Any:
        """
        Get attached config to device


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/template/device/config/attachedconfig

        :param device_id: Device Model ID
        :param policy_id: Policy id
        :returns: Any
        """
        params = {
            "deviceId": device_id,
            "policyId": policy_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/device/config/attachedconfig", params=params, **kw
        )
