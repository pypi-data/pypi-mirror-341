# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import PxGridInfo

if TYPE_CHECKING:
    from .cert.cert_builder import CertBuilder


class PxgridBuilder:
    """
    Builds and executes requests for operations under /ise/credentials/pxgrid
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> PxGridInfo:
        """
        Get PxGrid account
        GET /dataservice/ise/credentials/pxgrid

        :returns: PxGridInfo
        """
        return self._request_adapter.request(
            "GET", "/dataservice/ise/credentials/pxgrid", return_type=PxGridInfo, **kw
        )

    def delete(self, **kw) -> bool:
        """
        Delete PxGrid account information
        DELETE /dataservice/ise/credentials/pxgrid

        :returns: bool
        """
        return self._request_adapter.request(
            "DELETE", "/dataservice/ise/credentials/pxgrid", return_type=bool, **kw
        )

    @property
    def cert(self) -> CertBuilder:
        """
        The cert property
        """
        from .cert.cert_builder import CertBuilder

        return CertBuilder(self._request_adapter)
