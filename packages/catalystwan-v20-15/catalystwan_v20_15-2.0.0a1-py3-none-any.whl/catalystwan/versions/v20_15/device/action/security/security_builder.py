# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .amp.amp_builder import AmpBuilder
    from .apikey.apikey_builder import ApikeyBuilder
    from .devices.devices_builder import DevicesBuilder


class SecurityBuilder:
    """
    Builds and executes requests for operations under /device/action/security
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def amp(self) -> AmpBuilder:
        """
        The amp property
        """
        from .amp.amp_builder import AmpBuilder

        return AmpBuilder(self._request_adapter)

    @property
    def apikey(self) -> ApikeyBuilder:
        """
        The apikey property
        """
        from .apikey.apikey_builder import ApikeyBuilder

        return ApikeyBuilder(self._request_adapter)

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)
