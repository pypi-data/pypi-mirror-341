# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .saas.saas_builder import SaasBuilder


class CloudonrampBuilder:
    """
    Builds and executes requests for operations under /v1/cloudonramp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def saas(self) -> SaasBuilder:
        """
        The saas property
        """
        from .saas.saas_builder import SaasBuilder

        return SaasBuilder(self._request_adapter)
