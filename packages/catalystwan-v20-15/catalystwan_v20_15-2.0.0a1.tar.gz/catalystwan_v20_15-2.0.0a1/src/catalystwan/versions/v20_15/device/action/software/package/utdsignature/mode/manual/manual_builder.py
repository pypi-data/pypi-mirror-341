# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InstallPkg


class ManualBuilder:
    """
    Builds and executes requests for operations under /device/action/software/package/utdsignature/{type}/mode/manual
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, type_: str, payload: InstallPkg, **kw):
        """
        upload Utd image
        POST /dataservice/device/action/software/package/utdsignature/{type}/mode/manual

        :param type_: Type
        :param payload: Utd image File
        :returns: None
        """
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/device/action/software/package/utdsignature/{type}/mode/manual",
            params=params,
            payload=payload,
            **kw,
        )
