# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class RevokeBuilder:
    """
    Builds and executes requests for operations under /featurecertificate/revoke
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, payload: Any, **kw) -> Any:
        """
        Revoke feature cert from cEdge device


        Note: In a multitenant vManage system, this API is only available in the Provider and Provider-As-Tenant view.
        PUT /dataservice/featurecertificate/revoke

        :param payload: Revoking feature cert request for cEdge
        :returns: Any
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/featurecertificate/revoke", payload=payload, **kw
        )
