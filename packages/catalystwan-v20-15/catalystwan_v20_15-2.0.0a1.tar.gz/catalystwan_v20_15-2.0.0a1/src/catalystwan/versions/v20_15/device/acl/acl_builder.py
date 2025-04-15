# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .matchcounter.matchcounter_builder import MatchcounterBuilder


class AclBuilder:
    """
    Builds and executes requests for operations under /device/acl
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def matchcounter(self) -> MatchcounterBuilder:
        """
        The matchcounter property
        """
        from .matchcounter.matchcounter_builder import MatchcounterBuilder

        return MatchcounterBuilder(self._request_adapter)
