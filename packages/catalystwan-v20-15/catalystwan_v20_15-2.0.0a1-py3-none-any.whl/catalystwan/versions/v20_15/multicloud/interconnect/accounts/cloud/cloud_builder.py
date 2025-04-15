# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .connectivity.connectivity_builder import ConnectivityBuilder


class CloudBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/accounts/{interconnect-account-id}/cloud
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def connectivity(self) -> ConnectivityBuilder:
        """
        The connectivity property
        """
        from .connectivity.connectivity_builder import ConnectivityBuilder

        return ConnectivityBuilder(self._request_adapter)
