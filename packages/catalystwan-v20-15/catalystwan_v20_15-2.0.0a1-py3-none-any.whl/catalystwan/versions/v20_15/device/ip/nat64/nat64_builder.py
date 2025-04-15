# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .translation.translation_builder import TranslationBuilder


class Nat64Builder:
    """
    Builds and executes requests for operations under /device/ip/nat64
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def translation(self) -> TranslationBuilder:
        """
        The translation property
        """
        from .translation.translation_builder import TranslationBuilder

        return TranslationBuilder(self._request_adapter)
