# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .licenses.licenses_builder import LicensesBuilder


class TemplateBuilder:
    """
    Builds and executes requests for operations under /msla/template
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Retrieve all MSLA template
        GET /dataservice/msla/template

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/msla/template", **kw)

    @property
    def licenses(self) -> LicensesBuilder:
        """
        The licenses property
        """
        from .licenses.licenses_builder import LicensesBuilder

        return LicensesBuilder(self._request_adapter)
