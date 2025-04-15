# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .encrypt.encrypt_builder import EncryptBuilder


class EncryptTextBuilder:
    """
    Builds and executes requests for operations under /template/security/encryptText
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def encrypt(self) -> EncryptBuilder:
        """
        The encrypt property
        """
        from .encrypt.encrypt_builder import EncryptBuilder

        return EncryptBuilder(self._request_adapter)
