# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .authenticate.authenticate_builder import AuthenticateBuilder


class CloudBuilder:
    """
    Builds and executes requests for operations under /template/cortex/cloud
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def authenticate(self) -> AuthenticateBuilder:
        """
        The authenticate property
        """
        from .authenticate.authenticate_builder import AuthenticateBuilder

        return AuthenticateBuilder(self._request_adapter)
