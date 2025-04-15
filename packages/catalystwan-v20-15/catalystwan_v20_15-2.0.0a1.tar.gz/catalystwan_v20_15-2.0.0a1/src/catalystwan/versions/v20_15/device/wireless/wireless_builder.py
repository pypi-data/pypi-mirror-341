# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .client.client_builder import ClientBuilder
    from .radio.radio_builder import RadioBuilder
    from .ssid.ssid_builder import SsidBuilder


class WirelessBuilder:
    """
    Builds and executes requests for operations under /device/wireless
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def client(self) -> ClientBuilder:
        """
        The client property
        """
        from .client.client_builder import ClientBuilder

        return ClientBuilder(self._request_adapter)

    @property
    def radio(self) -> RadioBuilder:
        """
        The radio property
        """
        from .radio.radio_builder import RadioBuilder

        return RadioBuilder(self._request_adapter)

    @property
    def ssid(self) -> SsidBuilder:
        """
        The ssid property
        """
        from .ssid.ssid_builder import SsidBuilder

        return SsidBuilder(self._request_adapter)
