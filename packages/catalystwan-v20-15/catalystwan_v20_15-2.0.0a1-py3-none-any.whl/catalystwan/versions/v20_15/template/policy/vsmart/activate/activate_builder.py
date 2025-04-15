# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .central.central_builder import CentralBuilder


class ActivateBuilder:
    """
    Builds and executes requests for operations under /template/policy/vsmart/activate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, policy_id: str, payload: Any, **kw) -> Any:
        """
        Activate vsmart policy for a given policy id
        POST /dataservice/template/policy/vsmart/activate/{policyId}

        :param policy_id: Policy Id
        :param payload: Template policy
        :returns: Any
        """
        params = {
            "policyId": policy_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/template/policy/vsmart/activate/{policyId}",
            params=params,
            payload=payload,
            **kw,
        )

    @property
    def central(self) -> CentralBuilder:
        """
        The central property
        """
        from .central.central_builder import CentralBuilder

        return CentralBuilder(self._request_adapter)
