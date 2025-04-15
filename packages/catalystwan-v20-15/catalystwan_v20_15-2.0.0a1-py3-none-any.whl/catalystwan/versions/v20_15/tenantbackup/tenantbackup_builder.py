# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .delete.delete_builder import DeleteBuilder
    from .download.download_builder import DownloadBuilder
    from .export.export_builder import ExportBuilder
    from .import_.import_builder import ImportBuilder
    from .list.list_builder import ListBuilder


class TenantbackupBuilder:
    """
    Builds and executes requests for operations under /tenantbackup
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def delete(self) -> DeleteBuilder:
        """
        The delete property
        """
        from .delete.delete_builder import DeleteBuilder

        return DeleteBuilder(self._request_adapter)

    @property
    def download(self) -> DownloadBuilder:
        """
        The download property
        """
        from .download.download_builder import DownloadBuilder

        return DownloadBuilder(self._request_adapter)

    @property
    def export(self) -> ExportBuilder:
        """
        The export property
        """
        from .export.export_builder import ExportBuilder

        return ExportBuilder(self._request_adapter)

    @property
    def import_(self) -> ImportBuilder:
        """
        The import property
        """
        from .import_.import_builder import ImportBuilder

        return ImportBuilder(self._request_adapter)

    @property
    def list(self) -> ListBuilder:
        """
        The list property
        """
        from .list.list_builder import ListBuilder

        return ListBuilder(self._request_adapter)
