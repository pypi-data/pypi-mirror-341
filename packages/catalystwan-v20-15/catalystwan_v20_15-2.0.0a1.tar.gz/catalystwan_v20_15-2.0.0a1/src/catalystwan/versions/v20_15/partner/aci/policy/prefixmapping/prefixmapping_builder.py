# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class PrefixmappingBuilder:
    """
    Builds and executes requests for operations under /partner/aci/policy/prefixmapping
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, partner_id: str, **kw) -> Any:
        """
        Get prefix mapping
        GET /dataservice/partner/aci/policy/prefixmapping/{partnerId}

        :param partner_id: Partner Id
        :returns: Any
        """
        params = {
            "partnerId": partner_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/partner/aci/policy/prefixmapping/{partnerId}", params=params, **kw
        )

    def post(self, partner_id: str, payload: Any, **kw) -> Any:
        """
        Create data prefix mapping
        POST /dataservice/partner/aci/policy/prefixmapping/{partnerId}

        :param partner_id: Partner Id
        :param payload: Prefix definition
        :returns: Any
        """
        params = {
            "partnerId": partner_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/partner/aci/policy/prefixmapping/{partnerId}",
            params=params,
            payload=payload,
            **kw,
        )
