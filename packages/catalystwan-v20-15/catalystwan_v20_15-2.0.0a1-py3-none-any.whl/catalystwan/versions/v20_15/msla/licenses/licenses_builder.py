# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import MslaLicensesInner

if TYPE_CHECKING:
    from .compliance.compliance_builder import ComplianceBuilder
    from .sync.sync_builder import SyncBuilder


class LicensesBuilder:
    """
    Builds and executes requests for operations under /msla/licenses
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, uuid: Optional[str] = None, **kw) -> List[MslaLicensesInner]:
        """
        Get all the licenses
        GET /dataservice/msla/licenses

        :param uuid: Uuid
        :returns: List[MslaLicensesInner]
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/msla/licenses",
            return_type=List[MslaLicensesInner],
            params=params,
            **kw,
        )

    @property
    def compliance(self) -> ComplianceBuilder:
        """
        The compliance property
        """
        from .compliance.compliance_builder import ComplianceBuilder

        return ComplianceBuilder(self._request_adapter)

    @property
    def sync(self) -> SyncBuilder:
        """
        The sync property
        """
        from .sync.sync_builder import SyncBuilder

        return SyncBuilder(self._request_adapter)
