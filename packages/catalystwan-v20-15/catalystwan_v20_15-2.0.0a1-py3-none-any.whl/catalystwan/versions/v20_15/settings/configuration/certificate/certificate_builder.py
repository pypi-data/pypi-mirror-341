# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CertificateBuilder:
    """
    Builds and executes requests for operations under /settings/configuration/certificate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, type_: str, **kw) -> str:
        """
        Retrieve certificate configuration value by type
        GET /dataservice/settings/configuration/certificate/{type}

        :param type_: Type of the certificate configuration
        :returns: str
        """
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/settings/configuration/certificate/{type}",
            return_type=str,
            params=params,
            **kw,
        )

    def put(self, type_: str, payload: Any, **kw) -> str:
        """
        Update certificate configuration
        PUT /dataservice/settings/configuration/certificate/{type}

        :param type_: Type of the certificate configuration
        :param payload: Certificate configuration
        :returns: str
        """
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/settings/configuration/certificate/{type}",
            return_type=str,
            params=params,
            payload=payload,
            **kw,
        )

    def post(self, type_: str, payload: Any, **kw) -> str:
        """
        Add new certificate configuration
        POST /dataservice/settings/configuration/certificate/{type}

        :param type_: Type of the certificate configuration
        :param payload: Certificate configuration
        :returns: str
        """
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/settings/configuration/certificate/{type}",
            return_type=str,
            params=params,
            payload=payload,
            **kw,
        )
