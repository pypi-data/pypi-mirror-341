# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetAccounts, PostAccounts, PostAccountsResponse, PutAccounts

if TYPE_CHECKING:
    from .credentials.credentials_builder import CredentialsBuilder
    from .edge.edge_builder import EdgeBuilder


class AccountsBuilder:
    """
    Builds and executes requests for operations under /multicloud/accounts
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: PostAccounts, **kw) -> PostAccountsResponse:
        """
        Add Cloud Account
        POST /dataservice/multicloud/accounts

        :param payload: Payloads for updating Cloud Gateway based on CloudType
        :returns: PostAccountsResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/accounts",
            return_type=PostAccountsResponse,
            payload=payload,
            **kw,
        )

    def put(self, account_id: str, payload: PutAccounts, **kw):
        """
        Obtain all accounts for all clouds
        PUT /dataservice/multicloud/accounts/{accountId}

        :param account_id: Account id
        :param payload: Payloads for updating Cloud Gateway based on CloudType
        :returns: None
        """
        params = {
            "accountId": account_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/accounts/{accountId}",
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, account_id: str, **kw):
        """
        Obtain all accounts for all clouds
        DELETE /dataservice/multicloud/accounts/{accountId}

        :param account_id: Account id
        :returns: None
        """
        params = {
            "accountId": account_id,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/multicloud/accounts/{accountId}", params=params, **kw
        )

    @overload
    def get(self, *, account_id: str, **kw) -> GetAccounts:
        """
        Obtain all accounts for all clouds
        GET /dataservice/multicloud/accounts/{accountId}

        :param account_id: Account id
        :returns: GetAccounts
        """
        ...

    @overload
    def get(
        self, *, cloud_type: Optional[str] = None, cloud_gateway_enabled: Optional[str] = None, **kw
    ) -> List[GetAccounts]:
        """
        Obtain all accounts for all clouds
        GET /dataservice/multicloud/accounts

        :param cloud_type: Multicloud provider type
        :param cloud_gateway_enabled: Multicloud cloud gateway enabled
        :returns: List[GetAccounts]
        """
        ...

    def get(
        self,
        *,
        cloud_type: Optional[str] = None,
        cloud_gateway_enabled: Optional[str] = None,
        account_id: Optional[str] = None,
        **kw,
    ) -> Union[List[GetAccounts], GetAccounts]:
        # /dataservice/multicloud/accounts/{accountId}
        if self._request_adapter.param_checker(
            [(account_id, str)], [cloud_type, cloud_gateway_enabled]
        ):
            params = {
                "accountId": account_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/multicloud/accounts/{accountId}",
                return_type=GetAccounts,
                params=params,
                **kw,
            )
        # /dataservice/multicloud/accounts
        if self._request_adapter.param_checker([], [account_id]):
            params = {
                "cloudType": cloud_type,
                "cloudGatewayEnabled": cloud_gateway_enabled,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/multicloud/accounts",
                return_type=List[GetAccounts],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def credentials(self) -> CredentialsBuilder:
        """
        The credentials property
        """
        from .credentials.credentials_builder import CredentialsBuilder

        return CredentialsBuilder(self._request_adapter)

    @property
    def edge(self) -> EdgeBuilder:
        """
        The edge property
        """
        from .edge.edge_builder import EdgeBuilder

        return EdgeBuilder(self._request_adapter)
