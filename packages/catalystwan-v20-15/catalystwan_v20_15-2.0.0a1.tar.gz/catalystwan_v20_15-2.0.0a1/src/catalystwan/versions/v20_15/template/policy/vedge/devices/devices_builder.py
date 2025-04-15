# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional, overload

from catalystwan.abc import RequestAdapterInterface


class DevicesBuilder:
    """
    Builds and executes requests for operations under /template/policy/vedge/devices
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, policy_id: str, **kw) -> List[Any]:
        """
        Get device list by policy
        GET /dataservice/template/policy/vedge/devices/{policyId}

        :param policy_id: Policy Id
        :returns: List[Any]
        """
        ...

    @overload
    def get(self, **kw) -> List[Any]:
        """
        Get device list
        GET /dataservice/template/policy/vedge/devices

        :returns: List[Any]
        """
        ...

    def get(self, policy_id: Optional[str] = None, **kw) -> List[Any]:
        # /dataservice/template/policy/vedge/devices/{policyId}
        if self._request_adapter.param_checker([(policy_id, str)], []):
            params = {
                "policyId": policy_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/template/policy/vedge/devices/{policyId}",
                return_type=List[Any],
                params=params,
                **kw,
            )
        # /dataservice/template/policy/vedge/devices
        if self._request_adapter.param_checker([], [policy_id]):
            return self._request_adapter.request(
                "GET", "/dataservice/template/policy/vedge/devices", return_type=List[Any], **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")
