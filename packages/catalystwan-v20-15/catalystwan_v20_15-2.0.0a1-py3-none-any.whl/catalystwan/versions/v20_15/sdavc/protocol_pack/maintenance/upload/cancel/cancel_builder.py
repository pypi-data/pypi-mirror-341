# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class CancelBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/maintenance/upload/cancel
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, uuid: str, **kw):
        """
        Cancel or discard an uploaded protocol pack
        POST /dataservice/sdavc/protocol-pack/maintenance/upload/cancel/{uuid}

        :param uuid: Uuid
        :returns: None
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/sdavc/protocol-pack/maintenance/upload/cancel/{uuid}",
            params=params,
            **kw,
        )
