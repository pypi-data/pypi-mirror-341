# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface


class ListBuilder:
    """
    Builds and executes requests for operations under /certificate/vedge/list
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, state: Optional[str] = None, **kw) -> str:
        """
        get vEdge list
        GET /dataservice/certificate/vedge/list

        :param state: Certificate State
        :returns: str
        """
        params = {
            "state": state,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/certificate/vedge/list", return_type=str, params=params, **kw
        )

    def post(self, payload: str, action: Optional[str] = None, **kw) -> str:
        """
        Save vEdge list (send to controller)
        POST /dataservice/certificate/vedge/list

        :param action: Action Type
        :param payload: Required only for save action
        :returns: str
        """
        params = {
            "action": action,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/certificate/vedge/list",
            return_type=str,
            params=params,
            payload=payload,
            **kw,
        )
