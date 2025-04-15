# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class PreviewBuilder:
    """
    Builds and executes requests for operations under /template/policy/list/localdomain/preview
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Preview a policy list based on the policy list type
        POST /dataservice/template/policy/list/localdomain/preview

        :param payload: Policy list
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/policy/list/localdomain/preview", payload=payload, **kw
        )

    def get(self, id: str, **kw) -> Any:
        """
        Preview a specific policy list entry based on id provided
        GET /dataservice/template/policy/list/localdomain/preview/{id}

        :param id: Policy Id
        :returns: Any
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/policy/list/localdomain/preview/{id}", params=params, **kw
        )
