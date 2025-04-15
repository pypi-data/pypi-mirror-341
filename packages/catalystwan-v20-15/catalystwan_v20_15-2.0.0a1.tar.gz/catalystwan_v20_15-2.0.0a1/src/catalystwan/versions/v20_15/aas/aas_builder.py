# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .init.init_builder import InitBuilder
    from .reset_credentials.reset_credentials_builder import ResetCredentialsBuilder


class AasBuilder:
    """
    Builds and executes requests for operations under /aas
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def init(self) -> InitBuilder:
        """
        The init property
        """
        from .init.init_builder import InitBuilder

        return InitBuilder(self._request_adapter)

    @property
    def reset_credentials(self) -> ResetCredentialsBuilder:
        """
        The reset-credentials property
        """
        from .reset_credentials.reset_credentials_builder import ResetCredentialsBuilder

        return ResetCredentialsBuilder(self._request_adapter)
