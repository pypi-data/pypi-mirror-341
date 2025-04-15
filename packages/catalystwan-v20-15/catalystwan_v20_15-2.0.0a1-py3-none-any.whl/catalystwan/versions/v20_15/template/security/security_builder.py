# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .encrypt_text.encrypt_text_builder import EncryptTextBuilder


class SecurityBuilder:
    """
    Builds and executes requests for operations under /template/security
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def encrypt_text(self) -> EncryptTextBuilder:
        """
        The encryptText property
        """
        from .encrypt_text.encrypt_text_builder import EncryptTextBuilder

        return EncryptTextBuilder(self._request_adapter)
