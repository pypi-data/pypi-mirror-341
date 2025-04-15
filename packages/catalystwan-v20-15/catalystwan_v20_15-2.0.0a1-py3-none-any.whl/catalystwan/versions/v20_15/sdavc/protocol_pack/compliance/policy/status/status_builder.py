# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/compliance/policy/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, uuid: str, **kw):
        """
        Get policy compliance status
        GET /dataservice/sdavc/protocol-pack/compliance/policy/status/{uuid}

        :param uuid: Uuid
        :returns: None
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/sdavc/protocol-pack/compliance/policy/status/{uuid}",
            params=params,
            **kw,
        )
