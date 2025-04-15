# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .migrate.migrate_builder import MigrateBuilder


class VsmartMtBuilder:
    """
    Builds and executes requests for operations under /tenant/vsmart-mt
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def migrate(self) -> MigrateBuilder:
        """
        The migrate property
        """
        from .migrate.migrate_builder import MigrateBuilder

        return MigrateBuilder(self._request_adapter)
