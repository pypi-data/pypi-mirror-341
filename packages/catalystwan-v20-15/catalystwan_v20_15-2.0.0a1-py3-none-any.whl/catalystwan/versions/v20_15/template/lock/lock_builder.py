# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class LockBuilder:
    """
    Builds and executes requests for operations under /template/lock
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, process_id: str, **kw):
        """
        Update lease
        PUT /dataservice/template/lock/{processId}

        :param process_id: Process Id
        :returns: None
        """
        params = {
            "processId": process_id,
        }
        return self._request_adapter.request(
            "PUT", "/dataservice/template/lock/{processId}", params=params, **kw
        )

    def delete(self, process_id: str, **kw):
        """
        Remove lock
        DELETE /dataservice/template/lock/{processId}

        :param process_id: Process Id
        :returns: None
        """
        params = {
            "processId": process_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/template/lock/{processId}", params=params, **kw
        )
