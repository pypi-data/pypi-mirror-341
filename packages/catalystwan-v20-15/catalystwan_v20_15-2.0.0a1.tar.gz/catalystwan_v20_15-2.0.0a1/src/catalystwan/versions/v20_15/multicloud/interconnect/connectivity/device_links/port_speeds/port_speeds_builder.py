# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse20011


class PortSpeedsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/connectivity/device-links/port-speeds
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, interconnect_type: str, **kw) -> InlineResponse20011:
        """
        API to get supported port speeds for Device-Link by Interconnect provider.
        GET /dataservice/multicloud/interconnect/{interconnect-type}/connectivity/device-links/port-speeds

        :param interconnect_type: Interconnect Provider Type
        :returns: InlineResponse20011
        """
        params = {
            "interconnect-type": interconnect_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/{interconnect-type}/connectivity/device-links/port-speeds",
            return_type=InlineResponse20011,
            params=params,
            **kw,
        )
