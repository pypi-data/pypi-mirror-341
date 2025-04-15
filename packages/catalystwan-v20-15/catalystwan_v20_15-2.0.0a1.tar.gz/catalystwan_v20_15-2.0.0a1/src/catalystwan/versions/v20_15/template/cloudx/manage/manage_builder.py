# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .apps.apps_builder import AppsBuilder


class ManageBuilder:
    """
    Builds and executes requests for operations under /template/cloudx/manage
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def apps(self) -> AppsBuilder:
        """
        The apps property
        """
        from .apps.apps_builder import AppsBuilder

        return AppsBuilder(self._request_adapter)
