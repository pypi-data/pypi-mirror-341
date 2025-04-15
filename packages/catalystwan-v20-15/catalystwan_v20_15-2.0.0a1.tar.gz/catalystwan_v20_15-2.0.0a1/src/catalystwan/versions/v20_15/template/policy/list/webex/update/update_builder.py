# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class UpdateBuilder:
    """
    Builds and executes requests for operations under /template/policy/list/webex/update
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> List[Any]:
        """
        TEMP-Update Webex policy lists from Webex config
        POST /dataservice/template/policy/list/webex/update

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/policy/list/webex/update", return_type=List[Any], **kw
        )
