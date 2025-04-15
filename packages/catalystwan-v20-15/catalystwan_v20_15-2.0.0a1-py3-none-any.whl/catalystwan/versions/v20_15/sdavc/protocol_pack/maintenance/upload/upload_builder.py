# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ProtocolPackUploadRequest

if TYPE_CHECKING:
    from .cancel.cancel_builder import CancelBuilder
    from .confirm.confirm_builder import ConfirmBuilder
    from .status.status_builder import StatusBuilder


class UploadBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/maintenance/upload
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: ProtocolPackUploadRequest, **kw):
        """
        Upload protocol pack to SDAVC
        POST /dataservice/sdavc/protocol-pack/maintenance/upload

        :param payload: Protocol Pack File
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/sdavc/protocol-pack/maintenance/upload", payload=payload, **kw
        )

    @property
    def cancel(self) -> CancelBuilder:
        """
        The cancel property
        """
        from .cancel.cancel_builder import CancelBuilder

        return CancelBuilder(self._request_adapter)

    @property
    def confirm(self) -> ConfirmBuilder:
        """
        The confirm property
        """
        from .confirm.confirm_builder import ConfirmBuilder

        return ConfirmBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)
