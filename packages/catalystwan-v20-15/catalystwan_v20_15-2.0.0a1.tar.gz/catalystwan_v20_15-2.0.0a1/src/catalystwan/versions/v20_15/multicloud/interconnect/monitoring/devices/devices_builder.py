# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectDeviceInfoExtended


class DevicesBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/monitoring/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, interconnect_type: str, interconnect_gateway_name: Optional[str] = None, **kw
    ) -> List[InterconnectDeviceInfoExtended]:
        """
        API to retrieve Interconnect devices by Interconnect type for monitoring.
        GET /dataservice/multicloud/interconnect/{interconnect-type}/monitoring/devices

        :param interconnect_type: Interconnect provider type
        :param interconnect_gateway_name: Interconnect Gateway Name
        :returns: List[InterconnectDeviceInfoExtended]
        """
        params = {
            "interconnect-type": interconnect_type,
            "interconnect-gateway-name": interconnect_gateway_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/{interconnect-type}/monitoring/devices",
            return_type=List[InterconnectDeviceInfoExtended],
            params=params,
            **kw,
        )
