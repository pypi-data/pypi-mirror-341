# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class MigrateDeviceBuilder:
    """
    Builds and executes requests for operations under /system/device/migrateDevice
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, uuid: str, **kw) -> Any:
        """
        Migrate device software to vedge/cedge
        PUT /dataservice/system/device/migrateDevice/{uuid}

        :param uuid: Device uuid
        :returns: Any
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "PUT", "/dataservice/system/device/migrateDevice/{uuid}", params=params, **kw
        )
