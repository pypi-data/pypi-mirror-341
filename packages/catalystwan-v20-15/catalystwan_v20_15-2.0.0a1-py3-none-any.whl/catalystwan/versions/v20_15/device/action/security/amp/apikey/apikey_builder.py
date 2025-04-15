# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ApikeyBuilder:
    """
    Builds and executes requests for operations under /device/action/security/amp/apikey
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(self, uuid: str, **kw) -> Any:
        """
        Process amp api key deletion operation
        DELETE /dataservice/device/action/security/amp/apikey/{uuid}

        :param uuid: Uuid
        :returns: Any
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/device/action/security/amp/apikey/{uuid}", params=params, **kw
        )
