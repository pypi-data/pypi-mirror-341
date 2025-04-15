# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InstalledCertsInner

if TYPE_CHECKING:
    from .csr.csr_builder import CsrBuilder
    from .list.list_builder import ListBuilder


class VedgeBuilder:
    """
    Builds and executes requests for operations under /certificate/vedge
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, uuid: str, **kw) -> List[InstalledCertsInner]:
        """
        get device installed cert
        GET /dataservice/certificate/vedge

        :param uuid: Uuid
        :returns: List[InstalledCertsInner]
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/certificate/vedge",
            return_type=List[InstalledCertsInner],
            params=params,
            **kw,
        )

    @property
    def csr(self) -> CsrBuilder:
        """
        The csr property
        """
        from .csr.csr_builder import CsrBuilder

        return CsrBuilder(self._request_adapter)

    @property
    def list(self) -> ListBuilder:
        """
        The list property
        """
        from .list.list_builder import ListBuilder

        return ListBuilder(self._request_adapter)
