# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .rsa.rsa_builder import RsaBuilder


class ResetBuilder:
    """
    Builds and executes requests for operations under /certificate/reset
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def rsa(self) -> RsaBuilder:
        """
        The rsa property
        """
        from .rsa.rsa_builder import RsaBuilder

        return RsaBuilder(self._request_adapter)
