# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .force.force_builder import ForceBuilder


class TenantstatusBuilder:
    """
    Builds and executes requests for operations under /tenantstatus
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        List all tenant status


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/tenantstatus

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/tenantstatus", return_type=List[Any], **kw
        )

    @property
    def force(self) -> ForceBuilder:
        """
        The force property
        """
        from .force.force_builder import ForceBuilder

        return ForceBuilder(self._request_adapter)
