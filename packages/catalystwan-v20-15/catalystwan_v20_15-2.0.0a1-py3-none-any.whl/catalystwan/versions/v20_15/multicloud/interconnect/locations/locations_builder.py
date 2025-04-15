# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class LocationsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/locations
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(self, interconnect_type: str, **kw):
        """
        API to delete the stored regions for an Interconnect provider type from vManage.
        DELETE /dataservice/multicloud/interconnect/{interconnect-type}/locations

        :param interconnect_type: Interconnect provider type
        :returns: None
        """
        params = {
            "interconnect-type": interconnect_type,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/multicloud/interconnect/{interconnect-type}/locations",
            params=params,
            **kw,
        )
