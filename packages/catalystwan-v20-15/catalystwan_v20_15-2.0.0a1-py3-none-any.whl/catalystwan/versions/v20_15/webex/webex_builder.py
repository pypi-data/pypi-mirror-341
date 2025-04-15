# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .accesscode.accesscode_builder import AccesscodeBuilder
    from .datacenter.datacenter_builder import DatacenterBuilder
    from .redirect.redirect_builder import RedirectBuilder


class WebexBuilder:
    """
    Builds and executes requests for operations under /webex
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def accesscode(self) -> AccesscodeBuilder:
        """
        The accesscode property
        """
        from .accesscode.accesscode_builder import AccesscodeBuilder

        return AccesscodeBuilder(self._request_adapter)

    @property
    def datacenter(self) -> DatacenterBuilder:
        """
        The datacenter property
        """
        from .datacenter.datacenter_builder import DatacenterBuilder

        return DatacenterBuilder(self._request_adapter)

    @property
    def redirect(self) -> RedirectBuilder:
        """
        The redirect property
        """
        from .redirect.redirect_builder import RedirectBuilder

        return RedirectBuilder(self._request_adapter)
