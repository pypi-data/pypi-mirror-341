# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .licenses.licenses_builder import LicensesBuilder


class EntitlementBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/entitlement
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def licenses(self) -> LicensesBuilder:
        """
        The licenses property
        """
        from .licenses.licenses_builder import LicensesBuilder

        return LicensesBuilder(self._request_adapter)
