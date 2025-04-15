# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .isdnstatus.isdnstatus_builder import IsdnstatusBuilder


class VoiceisdninfoBuilder:
    """
    Builds and executes requests for operations under /device/voiceisdninfo
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def isdnstatus(self) -> IsdnstatusBuilder:
        """
        The isdnstatus property
        """
        from .isdnstatus.isdnstatus_builder import IsdnstatusBuilder

        return IsdnstatusBuilder(self._request_adapter)
