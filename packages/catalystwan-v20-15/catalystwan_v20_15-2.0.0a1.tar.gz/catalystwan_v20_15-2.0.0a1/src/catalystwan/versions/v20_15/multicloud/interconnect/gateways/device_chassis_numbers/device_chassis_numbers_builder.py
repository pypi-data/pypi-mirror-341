# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse2003, InterconnectTypeParam


class DeviceChassisNumbersBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/gateways/device-chassis-numbers
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        interconnect_type: InterconnectTypeParam,
        config_group_id: Optional[str] = None,
        device_solution_type: Optional[str] = None,
        **kw,
    ) -> List[InlineResponse2003]:
        """
        API to retrieve available devices or devices associated to a config group.
        GET /dataservice/multicloud/interconnect/{interconnect-type}/gateways/device-chassis-numbers

        :param interconnect_type: Interconnect provider type
        :param config_group_id: Config Group Id
        :param device_solution_type: Device solution type
        :returns: List[InlineResponse2003]
        """
        params = {
            "interconnect-type": interconnect_type,
            "config-group-id": config_group_id,
            "device-solution-type": device_solution_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/{interconnect-type}/gateways/device-chassis-numbers",
            return_type=List[InlineResponse2003],
            params=params,
            **kw,
        )
