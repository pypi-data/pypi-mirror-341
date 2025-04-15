# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetDataCenters


class DatacentersBuilder:
    """
    Builds and executes requests for operations under /sig/datacenters
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, type_: str, tunneltype: str, devicetype: str, **kw) -> Any:
        """
        Get list of data centers for zscaler or umbrella
        GET /dataservice/sig/datacenters/{type}/{tunneltype}/{devicetype}

        :param type_: Provider type
        :param tunneltype: Type of the tunnel ipsec/gre
        :param devicetype: Type of the device vedge/cedge
        :returns: Any
        """
        ...

    @overload
    def get(self, type_: str, tunneltype: str, **kw) -> GetDataCenters:
        """
        The API to get all sig data center for given provider type
        GET /dataservice/sig/datacenters/{type}/{tunneltype}

        :param type_: Type
        :param tunneltype: Tunneltype
        :returns: GetDataCenters
        """
        ...

    def get(
        self, type_: str, tunneltype: str, devicetype: Optional[str] = None, **kw
    ) -> Union[GetDataCenters, Any]:
        # /dataservice/sig/datacenters/{type}/{tunneltype}/{devicetype}
        if self._request_adapter.param_checker(
            [(type_, str), (tunneltype, str), (devicetype, str)], []
        ):
            params = {
                "type": type_,
                "tunneltype": tunneltype,
                "devicetype": devicetype,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/sig/datacenters/{type}/{tunneltype}/{devicetype}",
                params=params,
                **kw,
            )
        # /dataservice/sig/datacenters/{type}/{tunneltype}
        if self._request_adapter.param_checker([(type_, str), (tunneltype, str)], [devicetype]):
            params = {
                "type": type_,
                "tunneltype": tunneltype,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/sig/datacenters/{type}/{tunneltype}",
                return_type=GetDataCenters,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
