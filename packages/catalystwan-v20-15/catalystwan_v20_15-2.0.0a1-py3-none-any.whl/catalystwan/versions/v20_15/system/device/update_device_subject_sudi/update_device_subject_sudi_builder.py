# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class UpdateDeviceSubjectSudiBuilder:
    """
    Builds and executes requests for operations under /system/device/updateDeviceSubjectSUDI
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, uuid: str, **kw):
        """
        update subject sudi value of given device uuid
        PUT /dataservice/system/device/updateDeviceSubjectSUDI/{uuid}

        :param uuid: Device uuid
        :returns: None
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "PUT", "/dataservice/system/device/updateDeviceSubjectSUDI/{uuid}", params=params, **kw
        )
