# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NotificationsRulesResponse


class RulesBuilder:
    """
    Builds and executes requests for operations under /notifications/rules
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, rule_id: Optional[str] = None, site_id: Optional[str] = None, **kw
    ) -> NotificationsRulesResponse:
        """
        Get all rules or specific notification rule by its Id
        GET /dataservice/notifications/rules

        :param rule_id: Rule id
        :param site_id: Site id
        :returns: NotificationsRulesResponse
        """
        params = {
            "ruleId": rule_id,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/notifications/rules",
            return_type=NotificationsRulesResponse,
            params=params,
            **kw,
        )

    def delete(self, rule_id: str, **kw):
        """
        Delete notification rule
        DELETE /dataservice/notifications/rules

        :param rule_id: Rule Id
        :returns: None
        """
        params = {
            "ruleId": rule_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/notifications/rules", params=params, **kw
        )
