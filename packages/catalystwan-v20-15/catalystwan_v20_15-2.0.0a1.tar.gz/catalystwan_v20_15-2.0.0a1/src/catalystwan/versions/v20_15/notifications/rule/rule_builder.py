# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class RuleBuilder:
    """
    Builds and executes requests for operations under /notifications/rule
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, rule_id: str, payload: Any, **kw):
        """
        Update notification rule
        PUT /dataservice/notifications/rule

        :param rule_id: Rule Id
        :param payload: Notification rule
        :returns: None
        """
        params = {
            "ruleId": rule_id,
        }
        return self._request_adapter.request(
            "PUT", "/dataservice/notifications/rule", params=params, payload=payload, **kw
        )

    def post(self, payload: Any, **kw):
        """
        Add notification rule
        POST /dataservice/notifications/rule

        :param payload: Notification rule
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/notifications/rule", payload=payload, **kw
        )
