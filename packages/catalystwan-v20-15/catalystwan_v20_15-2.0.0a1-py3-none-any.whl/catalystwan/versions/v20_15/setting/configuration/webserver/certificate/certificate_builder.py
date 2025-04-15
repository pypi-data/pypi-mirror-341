# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .getcertificate.getcertificate_builder import GetcertificateBuilder


class CertificateBuilder:
    """
    Builds and executes requests for operations under /setting/configuration/webserver/certificate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> str:
        """
        Retrieves Certificate Signing Request information
        GET /dataservice/setting/configuration/webserver/certificate

        :returns: str
        """
        return self._request_adapter.request(
            "GET", "/dataservice/setting/configuration/webserver/certificate", return_type=str, **kw
        )

    def put(self, payload: Any, **kw) -> str:
        """
        Import a signed web server certificate
        PUT /dataservice/setting/configuration/webserver/certificate

        :param payload: Web Server Certificate configuration
        :returns: str
        """
        return self._request_adapter.request(
            "PUT",
            "/dataservice/setting/configuration/webserver/certificate",
            return_type=str,
            payload=payload,
            **kw,
        )

    def post(self, payload: Any, **kw) -> str:
        """
        Generate Certificate Signing Request
        POST /dataservice/setting/configuration/webserver/certificate

        :param payload: Web Server Certificate configuration
        :returns: str
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/setting/configuration/webserver/certificate",
            return_type=str,
            payload=payload,
            **kw,
        )

    @property
    def getcertificate(self) -> GetcertificateBuilder:
        """
        The getcertificate property
        """
        from .getcertificate.getcertificate_builder import GetcertificateBuilder

        return GetcertificateBuilder(self._request_adapter)
