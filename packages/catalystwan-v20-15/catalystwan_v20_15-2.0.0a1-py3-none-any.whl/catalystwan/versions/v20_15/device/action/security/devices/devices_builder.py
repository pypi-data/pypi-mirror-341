# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GroupId, PolicyTypeParam


class DevicesBuilder:
    """
    Builds and executes requests for operations under /device/action/security/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, policy_type: PolicyTypeParam, group_id: GroupId, **kw) -> List[Any]:
        """
        Get list of devices by security policy type
        GET /dataservice/device/action/security/devices/{policyType}

        :param policy_type: Policy type
        :param group_id: Group Id
        :returns: List[Any]
        """
        params = {
            "policyType": policy_type,
            "groupId": group_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/action/security/devices/{policyType}",
            return_type=List[Any],
            params=params,
            **kw,
        )
