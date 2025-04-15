# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .gcr_and_attachments.gcr_and_attachments_builder import GcrAndAttachmentsBuilder
    from .vhubs.vhubs_builder import VhubsBuilder
    from .vwans.vwans_builder import VwansBuilder


class AccountsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/cloud/{cloud-type}/accounts
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def gcr_and_attachments(self) -> GcrAndAttachmentsBuilder:
        """
        The gcr-and-attachments property
        """
        from .gcr_and_attachments.gcr_and_attachments_builder import GcrAndAttachmentsBuilder

        return GcrAndAttachmentsBuilder(self._request_adapter)

    @property
    def vhubs(self) -> VhubsBuilder:
        """
        The vhubs property
        """
        from .vhubs.vhubs_builder import VhubsBuilder

        return VhubsBuilder(self._request_adapter)

    @property
    def vwans(self) -> VwansBuilder:
        """
        The vwans property
        """
        from .vwans.vwans_builder import VwansBuilder

        return VwansBuilder(self._request_adapter)
