# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .file.file_builder import FileBuilder


class InputBuilder:
    """
    Builds and executes requests for operations under /template/device/config/process/input
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def file(self) -> FileBuilder:
        """
        The file property
        """
        from .file.file_builder import FileBuilder

        return FileBuilder(self._request_adapter)
