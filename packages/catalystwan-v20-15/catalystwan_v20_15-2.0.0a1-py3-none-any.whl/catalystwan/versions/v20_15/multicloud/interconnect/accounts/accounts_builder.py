# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectAccount

if TYPE_CHECKING:
    from .billing_accounts.billing_accounts_builder import BillingAccountsBuilder
    from .cloud.cloud_builder import CloudBuilder
    from .connectivity.connectivity_builder import ConnectivityBuilder
    from .credentials.credentials_builder import CredentialsBuilder
    from .locations.locations_builder import LocationsBuilder


class AccountsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/accounts
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: InterconnectAccount, **kw) -> InterconnectAccount:
        """
        API to associate an Interconnect provider account to vManage.
        POST /dataservice/multicloud/interconnect/accounts

        :param payload: Request Payload for Multicloud Interconnect Accounts
        :returns: InterconnectAccount
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/interconnect/accounts",
            return_type=InterconnectAccount,
            payload=payload,
            **kw,
        )

    def put(self, interconnect_account_id: str, payload: InterconnectAccount, **kw):
        """
        API to edit associated Interconnect provider account name and description.
        PUT /dataservice/multicloud/interconnect/accounts/{interconnect-account-id}

        :param interconnect_account_id: Interconnect provider account id
        :param payload: Request Payload for Multicloud Interconnect Accounts
        :returns: None
        """
        params = {
            "interconnect-account-id": interconnect_account_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/interconnect/accounts/{interconnect-account-id}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, interconnect_account_id: str, **kw):
        """
        API to disassociate Interconnect provider account from vManage.
        DELETE /dataservice/multicloud/interconnect/accounts/{interconnect-account-id}

        :param interconnect_account_id: Interconnect provider account id
        :returns: None
        """
        params = {
            "interconnect-account-id": interconnect_account_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/multicloud/interconnect/accounts/{interconnect-account-id}",
            params=params,
            **kw,
        )

    @overload
    def get(self, *, interconnect_account_id: str, **kw) -> InterconnectAccount:
        """
        API to retrieve associated Interconnect provider account details by id.
        GET /dataservice/multicloud/interconnect/accounts/{interconnect-account-id}

        :param interconnect_account_id: Interconnect provider account id
        :returns: InterconnectAccount
        """
        ...

    @overload
    def get(self, *, interconnect_type: Optional[str] = None, **kw) -> List[InterconnectAccount]:
        """
        API to retrieve Interconnect provider accounts.
        GET /dataservice/multicloud/interconnect/accounts

        :param interconnect_type: Interconnect provider type
        :returns: List[InterconnectAccount]
        """
        ...

    def get(
        self,
        *,
        interconnect_type: Optional[str] = None,
        interconnect_account_id: Optional[str] = None,
        **kw,
    ) -> Union[List[InterconnectAccount], InterconnectAccount]:
        # /dataservice/multicloud/interconnect/accounts/{interconnect-account-id}
        if self._request_adapter.param_checker(
            [(interconnect_account_id, str)], [interconnect_type]
        ):
            params = {
                "interconnect-account-id": interconnect_account_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/multicloud/interconnect/accounts/{interconnect-account-id}",
                return_type=InterconnectAccount,
                params=params,
                **kw,
            )
        # /dataservice/multicloud/interconnect/accounts
        if self._request_adapter.param_checker([], [interconnect_account_id]):
            params = {
                "interconnect-type": interconnect_type,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/multicloud/interconnect/accounts",
                return_type=List[InterconnectAccount],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def billing_accounts(self) -> BillingAccountsBuilder:
        """
        The billing-accounts property
        """
        from .billing_accounts.billing_accounts_builder import BillingAccountsBuilder

        return BillingAccountsBuilder(self._request_adapter)

    @property
    def cloud(self) -> CloudBuilder:
        """
        The cloud property
        """
        from .cloud.cloud_builder import CloudBuilder

        return CloudBuilder(self._request_adapter)

    @property
    def connectivity(self) -> ConnectivityBuilder:
        """
        The connectivity property
        """
        from .connectivity.connectivity_builder import ConnectivityBuilder

        return ConnectivityBuilder(self._request_adapter)

    @property
    def credentials(self) -> CredentialsBuilder:
        """
        The credentials property
        """
        from .credentials.credentials_builder import CredentialsBuilder

        return CredentialsBuilder(self._request_adapter)

    @property
    def locations(self) -> LocationsBuilder:
        """
        The locations property
        """
        from .locations.locations_builder import LocationsBuilder

        return LocationsBuilder(self._request_adapter)
