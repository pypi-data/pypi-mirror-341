# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .tloc.tloc_builder import TlocBuilder
    from .tloc_interface_map.tloc_interface_map_builder import TlocInterfaceMapBuilder


class DeviceBuilder:
    """
    Builds and executes requests for operations under /device/bfd/state/device
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get device BFD state summary
        GET /dataservice/device/bfd/state/device

        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/bfd/state/device", params=params, **kw
        )

    @property
    def tloc(self) -> TlocBuilder:
        """
        The tloc property
        """
        from .tloc.tloc_builder import TlocBuilder

        return TlocBuilder(self._request_adapter)

    @property
    def tloc_interface_map(self) -> TlocInterfaceMapBuilder:
        """
        The tlocInterfaceMap property
        """
        from .tloc_interface_map.tloc_interface_map_builder import TlocInterfaceMapBuilder

        return TlocInterfaceMapBuilder(self._request_adapter)
