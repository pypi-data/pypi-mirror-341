# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse20016


class SshkeysBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/sshkeys
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, interconnect_provider_name: str, interconnect_account_id: str, **kw
    ) -> InlineResponse20016:
        """
        Get ssh keys for Interconnect provider.
        GET /dataservice/multicloud/interconnect/sshkeys

        :param interconnect_provider_name: Interconnect provider name
        :param interconnect_account_id: Interconnect account id
        :returns: InlineResponse20016
        """
        params = {
            "interconnect-provider-name": interconnect_provider_name,
            "interconnect-account-id": interconnect_account_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/sshkeys",
            return_type=InlineResponse20016,
            params=params,
            **kw,
        )
