# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetBootstrapConfigZip


class DownloadBuilder:
    """
    Builds and executes requests for operations under /system/device/bootstrap/download
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, id: str, **kw) -> GetBootstrapConfigZip:
        """
        Download vEdge device config
        GET /dataservice/system/device/bootstrap/download/{id}

        :param id: id
        :returns: GetBootstrapConfigZip
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/system/device/bootstrap/download/{id}",
            return_type=GetBootstrapConfigZip,
            params=params,
            **kw,
        )
