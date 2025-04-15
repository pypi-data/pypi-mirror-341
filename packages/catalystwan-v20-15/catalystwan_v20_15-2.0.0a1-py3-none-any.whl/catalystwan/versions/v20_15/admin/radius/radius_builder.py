# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Radius


class RadiusBuilder:
    """
    Builds and executes requests for operations under /admin/radius
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Radius:
        """
        Get radius configuration


        Note: In a multitenant vManage system, this API is only available in the Provider and Provider-As-Tenant view.
        GET /dataservice/admin/radius

        :returns: Radius
        """
        return self._request_adapter.request(
            "GET", "/dataservice/admin/radius", return_type=Radius, **kw
        )

    def put(self, payload: Radius, **kw):
        """
        Update radius configuration


        Note: In a multitenant vManage system, this API is only available in the Provider and Provider-As-Tenant view.
        PUT /dataservice/admin/radius

        :param payload: radius
        :returns: None
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/admin/radius", payload=payload, **kw
        )

    def post(self, payload: Radius, **kw):
        """
        Create radius configuration


        Note: In a multitenant vManage system, this API is only available in the Provider and Provider-As-Tenant view.
        POST /dataservice/admin/radius

        :param payload: radius
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/admin/radius", payload=payload, **kw
        )

    def delete(self, **kw) -> Radius:
        """
        Delete radius configuration


        Note: In a multitenant vManage system, this API is only available in the Provider and Provider-As-Tenant view.
        DELETE /dataservice/admin/radius

        :returns: Radius
        """
        return self._request_adapter.request(
            "DELETE", "/dataservice/admin/radius", return_type=Radius, **kw
        )
