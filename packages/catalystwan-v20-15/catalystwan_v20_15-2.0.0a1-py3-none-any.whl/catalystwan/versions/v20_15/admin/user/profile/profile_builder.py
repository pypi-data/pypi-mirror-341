# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .locale.locale_builder import LocaleBuilder
    from .password.password_builder import PasswordBuilder


class ProfileBuilder:
    """
    Builds and executes requests for operations under /admin/user/profile
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def locale(self) -> LocaleBuilder:
        """
        The locale property
        """
        from .locale.locale_builder import LocaleBuilder

        return LocaleBuilder(self._request_adapter)

    @property
    def password(self) -> PasswordBuilder:
        """
        The password property
        """
        from .password.password_builder import PasswordBuilder

        return PasswordBuilder(self._request_adapter)
