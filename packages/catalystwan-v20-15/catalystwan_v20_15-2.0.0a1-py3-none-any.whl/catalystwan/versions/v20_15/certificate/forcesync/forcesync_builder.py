# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .root_cert.root_cert_builder import RootCertBuilder


class ForcesyncBuilder:
    """
    Builds and executes requests for operations under /certificate/forcesync
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def root_cert(self) -> RootCertBuilder:
        """
        The rootCert property
        """
        from .root_cert.root_cert_builder import RootCertBuilder

        return RootCertBuilder(self._request_adapter)
