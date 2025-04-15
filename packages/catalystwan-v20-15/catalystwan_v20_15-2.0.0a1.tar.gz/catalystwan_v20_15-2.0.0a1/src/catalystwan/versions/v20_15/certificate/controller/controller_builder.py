# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .bulkcsr.bulkcsr_builder import BulkcsrBuilder
    from .certstatus.certstatus_builder import CertstatusBuilder


class ControllerBuilder:
    """
    Builds and executes requests for operations under /certificate/controller
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def bulkcsr(self) -> BulkcsrBuilder:
        """
        The bulkcsr property
        """
        from .bulkcsr.bulkcsr_builder import BulkcsrBuilder

        return BulkcsrBuilder(self._request_adapter)

    @property
    def certstatus(self) -> CertstatusBuilder:
        """
        The certstatus property
        """
        from .certstatus.certstatus_builder import CertstatusBuilder

        return CertstatusBuilder(self._request_adapter)
