# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cloudservices.cloudservices_builder import CloudservicesBuilder
    from .dca.dca_builder import DcaBuilder


class ConfigurationBuilder:
    """
    Builds and executes requests for operations under /dca/settings/configuration
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def cloudservices(self) -> CloudservicesBuilder:
        """
        The cloudservices property
        """
        from .cloudservices.cloudservices_builder import CloudservicesBuilder

        return CloudservicesBuilder(self._request_adapter)

    @property
    def dca(self) -> DcaBuilder:
        """
        The dca property
        """
        from .dca.dca_builder import DcaBuilder

        return DcaBuilder(self._request_adapter)
