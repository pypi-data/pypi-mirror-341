# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .association.association_builder import AssociationBuilder
    from .license.license_builder import LicenseBuilder
    from .sync.sync_builder import SyncBuilder
    from .template.template_builder import TemplateBuilder
    from .user_settings.user_settings_builder import UserSettingsBuilder


class SmartLicensingBuilder:
    """
    Builds and executes requests for operations under /v1/smart-licensing
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def association(self) -> AssociationBuilder:
        """
        The association property
        """
        from .association.association_builder import AssociationBuilder

        return AssociationBuilder(self._request_adapter)

    @property
    def license(self) -> LicenseBuilder:
        """
        The license property
        """
        from .license.license_builder import LicenseBuilder

        return LicenseBuilder(self._request_adapter)

    @property
    def sync(self) -> SyncBuilder:
        """
        The sync property
        """
        from .sync.sync_builder import SyncBuilder

        return SyncBuilder(self._request_adapter)

    @property
    def template(self) -> TemplateBuilder:
        """
        The template property
        """
        from .template.template_builder import TemplateBuilder

        return TemplateBuilder(self._request_adapter)

    @property
    def user_settings(self) -> UserSettingsBuilder:
        """
        The user-settings property
        """
        from .user_settings.user_settings_builder import UserSettingsBuilder

        return UserSettingsBuilder(self._request_adapter)
