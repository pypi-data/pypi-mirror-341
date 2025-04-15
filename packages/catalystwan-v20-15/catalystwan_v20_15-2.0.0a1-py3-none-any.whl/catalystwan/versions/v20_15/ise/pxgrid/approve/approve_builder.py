# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class ApproveBuilder:
    """
    Builds and executes requests for operations under /ise/pxgrid/approve
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, **kw) -> bool:
        """
        Approve pxGrid account
        PUT /dataservice/ise/pxgrid/approve

        :returns: bool
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/ise/pxgrid/approve", return_type=bool, **kw
        )
