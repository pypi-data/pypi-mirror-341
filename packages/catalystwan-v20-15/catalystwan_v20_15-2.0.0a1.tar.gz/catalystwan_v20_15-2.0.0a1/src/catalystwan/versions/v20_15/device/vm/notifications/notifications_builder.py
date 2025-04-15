# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class NotificationsBuilder:
    """
    Builds and executes requests for operations under /device/vm/notifications
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, user_group: str, **kw) -> Any:
        """
        Get CloudDock vm lifecycle state
        GET /dataservice/device/vm/notifications

        :param user_group: userGroup Name
        :returns: Any
        """
        params = {
            "userGroup": user_group,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/vm/notifications", params=params, **kw
        )
