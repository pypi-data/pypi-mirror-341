# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .devicelist.devicelist_builder import DevicelistBuilder
    from .fwall.fwall_builder import FwallBuilder
    from .ips.ips_builder import IpsBuilder
    from .urlf.urlf_builder import UrlfBuilder


class PolicyBuilder:
    """
    Builds and executes requests for operations under /security/policy
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def devicelist(self) -> DevicelistBuilder:
        """
        The devicelist property
        """
        from .devicelist.devicelist_builder import DevicelistBuilder

        return DevicelistBuilder(self._request_adapter)

    @property
    def fwall(self) -> FwallBuilder:
        """
        The fwall property
        """
        from .fwall.fwall_builder import FwallBuilder

        return FwallBuilder(self._request_adapter)

    @property
    def ips(self) -> IpsBuilder:
        """
        The ips property
        """
        from .ips.ips_builder import IpsBuilder

        return IpsBuilder(self._request_adapter)

    @property
    def urlf(self) -> UrlfBuilder:
        """
        The urlf property
        """
        from .urlf.urlf_builder import UrlfBuilder

        return UrlfBuilder(self._request_adapter)
