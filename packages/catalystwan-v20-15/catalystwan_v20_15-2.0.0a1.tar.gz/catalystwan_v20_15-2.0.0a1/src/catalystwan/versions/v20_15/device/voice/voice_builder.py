# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .dsp_active.dsp_active_builder import DspActiveBuilder
    from .phone_info.phone_info_builder import PhoneInfoBuilder
    from .profiles.profiles_builder import ProfilesBuilder
    from .sccp_ccm_groups.sccp_ccm_groups_builder import SccpCcmGroupsBuilder
    from .sccp_connections.sccp_connections_builder import SccpConnectionsBuilder
    from .voice_calls.voice_calls_builder import VoiceCallsBuilder
    from .voip_calls.voip_calls_builder import VoipCallsBuilder


class VoiceBuilder:
    """
    Builds and executes requests for operations under /device/voice
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def dsp_active(self) -> DspActiveBuilder:
        """
        The dspActive property
        """
        from .dsp_active.dsp_active_builder import DspActiveBuilder

        return DspActiveBuilder(self._request_adapter)

    @property
    def phone_info(self) -> PhoneInfoBuilder:
        """
        The phoneInfo property
        """
        from .phone_info.phone_info_builder import PhoneInfoBuilder

        return PhoneInfoBuilder(self._request_adapter)

    @property
    def profiles(self) -> ProfilesBuilder:
        """
        The profiles property
        """
        from .profiles.profiles_builder import ProfilesBuilder

        return ProfilesBuilder(self._request_adapter)

    @property
    def sccp_ccm_groups(self) -> SccpCcmGroupsBuilder:
        """
        The sccpCcmGroups property
        """
        from .sccp_ccm_groups.sccp_ccm_groups_builder import SccpCcmGroupsBuilder

        return SccpCcmGroupsBuilder(self._request_adapter)

    @property
    def sccp_connections(self) -> SccpConnectionsBuilder:
        """
        The sccpConnections property
        """
        from .sccp_connections.sccp_connections_builder import SccpConnectionsBuilder

        return SccpConnectionsBuilder(self._request_adapter)

    @property
    def voice_calls(self) -> VoiceCallsBuilder:
        """
        The voiceCalls property
        """
        from .voice_calls.voice_calls_builder import VoiceCallsBuilder

        return VoiceCallsBuilder(self._request_adapter)

    @property
    def voip_calls(self) -> VoipCallsBuilder:
        """
        The voipCalls property
        """
        from .voip_calls.voip_calls_builder import VoipCallsBuilder

        return VoipCallsBuilder(self._request_adapter)
