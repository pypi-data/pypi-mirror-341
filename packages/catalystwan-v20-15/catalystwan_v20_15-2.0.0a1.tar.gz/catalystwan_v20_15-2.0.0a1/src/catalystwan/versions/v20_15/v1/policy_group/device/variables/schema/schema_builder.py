# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class SchemaBuilder:
    """
    Builds and executes requests for operations under /v1/policy-group/{policyGroupId}/device/variables/schema
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, policy_group_id: str, **kw) -> Any:
        """
        get device variables schema
        GET /dataservice/v1/policy-group/{policyGroupId}/device/variables/schema

        :param policy_group_id: Policy Group Id
        :returns: Any
        """
        params = {
            "policyGroupId": policy_group_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/policy-group/{policyGroupId}/device/variables/schema",
            params=params,
            **kw,
        )
