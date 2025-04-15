# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .account.account_builder import AccountBuilder
    from .authenticate.authenticate_builder import AuthenticateBuilder
    from .host.host_builder import HostBuilder
    from .mappedhostaccounts.mappedhostaccounts_builder import MappedhostaccountsBuilder


class CloudBuilder:
    """
    Builds and executes requests for operations under /template/cor/cloud
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get cloud list
        GET /dataservice/template/cor/cloud

        :returns: List[Any]
        """
        logging.warning("Operation: %s is deprecated", "getCloudList")
        return self._request_adapter.request(
            "GET", "/dataservice/template/cor/cloud", return_type=List[Any], **kw
        )

    @property
    def account(self) -> AccountBuilder:
        """
        The account property
        """
        from .account.account_builder import AccountBuilder

        return AccountBuilder(self._request_adapter)

    @property
    def authenticate(self) -> AuthenticateBuilder:
        """
        The authenticate property
        """
        from .authenticate.authenticate_builder import AuthenticateBuilder

        return AuthenticateBuilder(self._request_adapter)

    @property
    def host(self) -> HostBuilder:
        """
        The host property
        """
        from .host.host_builder import HostBuilder

        return HostBuilder(self._request_adapter)

    @property
    def mappedhostaccounts(self) -> MappedhostaccountsBuilder:
        """
        The mappedhostaccounts property
        """
        from .mappedhostaccounts.mappedhostaccounts_builder import MappedhostaccountsBuilder

        return MappedhostaccountsBuilder(self._request_adapter)
