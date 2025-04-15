# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class ResetCredentialsBuilder:
    """
    Builds and executes requests for operations under /aas/reset-credentials
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, cred_type: str, **kw):
        """
        SDWAN as a Platform - Manage Credentials
        POST /dataservice/aas/reset-credentials/{credType}

        :param cred_type: Cred type
        :returns: None
        """
        params = {
            "credType": cred_type,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/aas/reset-credentials/{credType}", params=params, **kw
        )
