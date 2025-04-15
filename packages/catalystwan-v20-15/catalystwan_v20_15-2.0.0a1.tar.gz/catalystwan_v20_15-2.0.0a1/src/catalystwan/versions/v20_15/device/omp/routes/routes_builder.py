# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .advertised.advertised_builder import AdvertisedBuilder
    from .received.received_builder import ReceivedBuilder


class RoutesBuilder:
    """
    Builds and executes requests for operations under /device/omp/routes
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def advertised(self) -> AdvertisedBuilder:
        """
        The advertised property
        """
        from .advertised.advertised_builder import AdvertisedBuilder

        return AdvertisedBuilder(self._request_adapter)

    @property
    def received(self) -> ReceivedBuilder:
        """
        The received property
        """
        from .received.received_builder import ReceivedBuilder

        return ReceivedBuilder(self._request_adapter)
