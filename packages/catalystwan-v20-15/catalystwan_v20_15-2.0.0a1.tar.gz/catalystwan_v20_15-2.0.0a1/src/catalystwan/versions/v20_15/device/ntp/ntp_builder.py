# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .associations.associations_builder import AssociationsBuilder
    from .peer.peer_builder import PeerBuilder
    from .status.status_builder import StatusBuilder


class NtpBuilder:
    """
    Builds and executes requests for operations under /device/ntp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def associations(self) -> AssociationsBuilder:
        """
        The associations property
        """
        from .associations.associations_builder import AssociationsBuilder

        return AssociationsBuilder(self._request_adapter)

    @property
    def peer(self) -> PeerBuilder:
        """
        The peer property
        """
        from .peer.peer_builder import PeerBuilder

        return PeerBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)
