# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .aaa.aaa_builder import AaaBuilder
    from .events.events_builder import EventsBuilder
    from .radius.radius_builder import RadiusBuilder
    from .tacacs.tacacs_builder import TacacsBuilder
    from .user.user_builder import UserBuilder
    from .usergroup.usergroup_builder import UsergroupBuilder
    from .vpngroup.vpngroup_builder import VpngroupBuilder


class AdminBuilder:
    """
    Builds and executes requests for operations under /admin
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def aaa(self) -> AaaBuilder:
        """
        The aaa property
        """
        from .aaa.aaa_builder import AaaBuilder

        return AaaBuilder(self._request_adapter)

    @property
    def events(self) -> EventsBuilder:
        """
        The events property
        """
        from .events.events_builder import EventsBuilder

        return EventsBuilder(self._request_adapter)

    @property
    def radius(self) -> RadiusBuilder:
        """
        The radius property
        """
        from .radius.radius_builder import RadiusBuilder

        return RadiusBuilder(self._request_adapter)

    @property
    def tacacs(self) -> TacacsBuilder:
        """
        The tacacs property
        """
        from .tacacs.tacacs_builder import TacacsBuilder

        return TacacsBuilder(self._request_adapter)

    @property
    def user(self) -> UserBuilder:
        """
        The user property
        """
        from .user.user_builder import UserBuilder

        return UserBuilder(self._request_adapter)

    @property
    def usergroup(self) -> UsergroupBuilder:
        """
        The usergroup property
        """
        from .usergroup.usergroup_builder import UsergroupBuilder

        return UsergroupBuilder(self._request_adapter)

    @property
    def vpngroup(self) -> VpngroupBuilder:
        """
        The vpngroup property
        """
        from .vpngroup.vpngroup_builder import VpngroupBuilder

        return VpngroupBuilder(self._request_adapter)
