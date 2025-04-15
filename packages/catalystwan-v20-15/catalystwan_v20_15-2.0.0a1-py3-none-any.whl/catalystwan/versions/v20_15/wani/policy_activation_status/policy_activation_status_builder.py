# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ActivationStatusRes


class PolicyActivationStatusBuilder:
    """
    Builds and executes requests for operations under /wani/{policyType}/{policyId}/policyActivationStatus
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, policy_type: str, policy_id: str, **kw) -> ActivationStatusRes:
        """
        Get if specified policy is apart of a activated centralized policy, if it is the response also gives the centralized policy id, the users original defined centralized policy id, and if current policy is apart of a active wani policy.
        GET /dataservice/wani/{policyType}/{policyId}/policyActivationStatus

        :param policy_type: Policy type
        :param policy_id: Policy id
        :returns: ActivationStatusRes
        """
        params = {
            "policyType": policy_type,
            "policyId": policy_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/wani/{policyType}/{policyId}/policyActivationStatus",
            return_type=ActivationStatusRes,
            params=params,
            **kw,
        )
