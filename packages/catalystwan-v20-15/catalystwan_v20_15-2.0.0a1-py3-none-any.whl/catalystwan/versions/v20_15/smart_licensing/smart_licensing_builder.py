# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .authenticate.authenticate_builder import AuthenticateBuilder
    from .fetch_accounts.fetch_accounts_builder import FetchAccountsBuilder
    from .fetch_all_sa.fetch_all_sa_builder import FetchAllSaBuilder
    from .fetch_reports_for_sa.fetch_reports_for_sa_builder import FetchReportsForSaBuilder
    from .get_user_settings.get_user_settings_builder import GetUserSettingsBuilder
    from .sync_licenses.sync_licenses_builder import SyncLicensesBuilder


class SmartLicensingBuilder:
    """
    Builds and executes requests for operations under /smartLicensing
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def authenticate(self) -> AuthenticateBuilder:
        """
        The authenticate property
        """
        from .authenticate.authenticate_builder import AuthenticateBuilder

        return AuthenticateBuilder(self._request_adapter)

    @property
    def fetch_accounts(self) -> FetchAccountsBuilder:
        """
        The fetchAccounts property
        """
        from .fetch_accounts.fetch_accounts_builder import FetchAccountsBuilder

        return FetchAccountsBuilder(self._request_adapter)

    @property
    def fetch_all_sa(self) -> FetchAllSaBuilder:
        """
        The fetchAllSa property
        """
        from .fetch_all_sa.fetch_all_sa_builder import FetchAllSaBuilder

        return FetchAllSaBuilder(self._request_adapter)

    @property
    def fetch_reports_for_sa(self) -> FetchReportsForSaBuilder:
        """
        The fetchReportsForSa property
        """
        from .fetch_reports_for_sa.fetch_reports_for_sa_builder import FetchReportsForSaBuilder

        return FetchReportsForSaBuilder(self._request_adapter)

    @property
    def get_user_settings(self) -> GetUserSettingsBuilder:
        """
        The getUserSettings property
        """
        from .get_user_settings.get_user_settings_builder import GetUserSettingsBuilder

        return GetUserSettingsBuilder(self._request_adapter)

    @property
    def sync_licenses(self) -> SyncLicensesBuilder:
        """
        The syncLicenses property
        """
        from .sync_licenses.sync_licenses_builder import SyncLicensesBuilder

        return SyncLicensesBuilder(self._request_adapter)
