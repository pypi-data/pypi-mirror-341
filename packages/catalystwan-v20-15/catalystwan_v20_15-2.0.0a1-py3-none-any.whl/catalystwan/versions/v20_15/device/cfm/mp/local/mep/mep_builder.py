# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class MepBuilder:
    """
    Builds and executes requests for operations under /device/cfm/mp/local/mep
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        domain: Optional[str] = None,
        service: Optional[str] = None,
        mep_id: Optional[int] = None,
        **kw,
    ) -> Any:
        """
        Get mp local mep from device
        GET /dataservice/device/cfm/mp/local/mep

        :param domain: Domain Name
        :param service: Service Name
        :param mep_id: MEP ID
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "domain": domain,
            "service": service,
            "mep-id": mep_id,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/cfm/mp/local/mep", params=params, **kw
        )
