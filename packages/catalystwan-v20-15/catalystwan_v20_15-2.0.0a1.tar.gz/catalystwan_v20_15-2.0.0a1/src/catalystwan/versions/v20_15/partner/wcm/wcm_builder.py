# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .netconf.netconf_builder import NetconfBuilder


class WcmBuilder:
    """
    Builds and executes requests for operations under /partner/wcm
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def netconf(self) -> NetconfBuilder:
        """
        The netconf property
        """
        from .netconf.netconf_builder import NetconfBuilder

        return NetconfBuilder(self._request_adapter)
