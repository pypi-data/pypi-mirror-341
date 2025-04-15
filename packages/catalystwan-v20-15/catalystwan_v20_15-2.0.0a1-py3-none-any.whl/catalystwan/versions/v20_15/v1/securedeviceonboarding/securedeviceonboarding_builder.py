# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .commplans.commplans_builder import CommplansBuilder
    from .deviceusage.deviceusage_builder import DeviceusageBuilder
    from .fetch_sdo_token.fetch_sdo_token_builder import FetchSdoTokenBuilder
    from .get_url_for_sdo_identity_service.get_url_for_sdo_identity_service_builder import (
        GetUrlForSdoIdentityServiceBuilder,
    )
    from .provider_credentials.provider_credentials_builder import ProviderCredentialsBuilder
    from .providercredentials.providercredentials_builder import ProvidercredentialsBuilder
    from .providerscredentials.providerscredentials_builder import ProviderscredentialsBuilder
    from .rateplans.rateplans_builder import RateplansBuilder
    from .registeredproviders.registeredproviders_builder import RegisteredprovidersBuilder


class SecuredeviceonboardingBuilder:
    """
    Builds and executes requests for operations under /v1/securedeviceonboarding
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def commplans(self) -> CommplansBuilder:
        """
        The commplans property
        """
        from .commplans.commplans_builder import CommplansBuilder

        return CommplansBuilder(self._request_adapter)

    @property
    def deviceusage(self) -> DeviceusageBuilder:
        """
        The deviceusage property
        """
        from .deviceusage.deviceusage_builder import DeviceusageBuilder

        return DeviceusageBuilder(self._request_adapter)

    @property
    def fetch_sdo_token(self) -> FetchSdoTokenBuilder:
        """
        The fetchSdoToken property
        """
        from .fetch_sdo_token.fetch_sdo_token_builder import FetchSdoTokenBuilder

        return FetchSdoTokenBuilder(self._request_adapter)

    @property
    def get_url_for_sdo_identity_service(self) -> GetUrlForSdoIdentityServiceBuilder:
        """
        The getUrlForSdoIdentityService property
        """
        from .get_url_for_sdo_identity_service.get_url_for_sdo_identity_service_builder import (
            GetUrlForSdoIdentityServiceBuilder,
        )

        return GetUrlForSdoIdentityServiceBuilder(self._request_adapter)

    @property
    def provider_credentials(self) -> ProviderCredentialsBuilder:
        """
        The providerCredentials property
        """
        from .provider_credentials.provider_credentials_builder import ProviderCredentialsBuilder

        return ProviderCredentialsBuilder(self._request_adapter)

    @property
    def providercredentials(self) -> ProvidercredentialsBuilder:
        """
        The providercredentials property
        """
        from .providercredentials.providercredentials_builder import ProvidercredentialsBuilder

        return ProvidercredentialsBuilder(self._request_adapter)

    @property
    def providerscredentials(self) -> ProviderscredentialsBuilder:
        """
        The providerscredentials property
        """
        from .providerscredentials.providerscredentials_builder import ProviderscredentialsBuilder

        return ProviderscredentialsBuilder(self._request_adapter)

    @property
    def rateplans(self) -> RateplansBuilder:
        """
        The rateplans property
        """
        from .rateplans.rateplans_builder import RateplansBuilder

        return RateplansBuilder(self._request_adapter)

    @property
    def registeredproviders(self) -> RegisteredprovidersBuilder:
        """
        The registeredproviders property
        """
        from .registeredproviders.registeredproviders_builder import RegisteredprovidersBuilder

        return RegisteredprovidersBuilder(self._request_adapter)
