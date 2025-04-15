# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DecommissionVedgeCloud


class DecommissionBuilder:
    """
    Builds and executes requests for operations under /system/device/decommission
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, uuid: str, **kw) -> DecommissionVedgeCloud:
        """
        Decomission vEdge device
        PUT /dataservice/system/device/decommission/{uuid}

        :param uuid: Device uuid
        :returns: DecommissionVedgeCloud
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/system/device/decommission/{uuid}",
            return_type=DecommissionVedgeCloud,
            params=params,
            **kw,
        )
