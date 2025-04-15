# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .preferredpath.preferredpath_builder import PreferredpathBuilder


class M365Builder:
    """
    Builds and executes requests for operations under /cloudservices/m365
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def preferredpath(self) -> PreferredpathBuilder:
        """
        The preferredpath property
        """
        from .preferredpath.preferredpath_builder import PreferredpathBuilder

        return PreferredpathBuilder(self._request_adapter)
