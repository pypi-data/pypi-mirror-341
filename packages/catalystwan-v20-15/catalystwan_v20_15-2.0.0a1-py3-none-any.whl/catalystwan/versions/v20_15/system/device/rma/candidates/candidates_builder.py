# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetRmaCandidates


class CandidatesBuilder:
    """
    Builds and executes requests for operations under /system/device/rma/candidates
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_type: str, uuid: Optional[str] = None, **kw) -> GetRmaCandidates:
        """
        Get RMA candidates by device type
        GET /dataservice/system/device/rma/candidates/{deviceType}

        :param device_type: deviceType
        :param uuid: uuid
        :returns: GetRmaCandidates
        """
        params = {
            "deviceType": device_type,
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/system/device/rma/candidates/{deviceType}",
            return_type=GetRmaCandidates,
            params=params,
            **kw,
        )
