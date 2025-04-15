# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Aaa


class AaaBuilder:
    """
    Builds and executes requests for operations under /admin/aaa
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Aaa:
        """
        Get aaa configuration


        Note: In a multitenant vManage system, this API is only available in the Provider and Provider-As-Tenant view.
        GET /dataservice/admin/aaa

        :returns: Aaa
        """
        return self._request_adapter.request("GET", "/dataservice/admin/aaa", return_type=Aaa, **kw)

    def put(self, payload: Aaa, **kw):
        """
        Update aaa configuration


        Note: In a multitenant vManage system, this API is only available in the Provider and Provider-As-Tenant view.
        PUT /dataservice/admin/aaa

        :param payload: aaa
        :returns: None
        """
        return self._request_adapter.request("PUT", "/dataservice/admin/aaa", payload=payload, **kw)

    def post(self, payload: Aaa, **kw):
        """
        Create aaa configuration


        Note: In a multitenant vManage system, this API is only available in the Provider and Provider-As-Tenant view.
        POST /dataservice/admin/aaa

        :param payload: aaa
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/admin/aaa", payload=payload, **kw
        )

    def delete(self, **kw):
        """
        Delete aaa configuration


        Note: In a multitenant vManage system, this API is only available in the Provider and Provider-As-Tenant view.
        DELETE /dataservice/admin/aaa

        :returns: None
        """
        return self._request_adapter.request("DELETE", "/dataservice/admin/aaa", **kw)
