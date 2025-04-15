# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .devices.devices_builder import DevicesBuilder
    from .download.download_builder import DownloadBuilder
    from .fetchaccounts.fetchaccounts_builder import FetchaccountsBuilder
    from .testbed_mode.testbed_mode_builder import TestbedModeBuilder


class HsecBuilder:
    """
    Builds and executes requests for operations under /hsec
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)

    @property
    def download(self) -> DownloadBuilder:
        """
        The download property
        """
        from .download.download_builder import DownloadBuilder

        return DownloadBuilder(self._request_adapter)

    @property
    def fetchaccounts(self) -> FetchaccountsBuilder:
        """
        The fetchaccounts property
        """
        from .fetchaccounts.fetchaccounts_builder import FetchaccountsBuilder

        return FetchaccountsBuilder(self._request_adapter)

    @property
    def testbed_mode(self) -> TestbedModeBuilder:
        """
        The testbedMode property
        """
        from .testbed_mode.testbed_mode_builder import TestbedModeBuilder

        return TestbedModeBuilder(self._request_adapter)
