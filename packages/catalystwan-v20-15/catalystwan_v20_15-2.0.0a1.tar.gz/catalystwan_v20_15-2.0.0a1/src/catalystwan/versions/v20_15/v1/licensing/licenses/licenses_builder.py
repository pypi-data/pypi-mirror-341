# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import LicensesRequest, LicensesResponse


class LicensesBuilder:
    """
    Builds and executes requests for operations under /v1/licensing/licenses
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: LicensesRequest, **kw) -> LicensesResponse:
        """
        Get applicable licenses based on platform class
        POST /dataservice/v1/licensing/licenses

        :param payload: List of device UUIDs and filters
        :returns: LicensesResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/licensing/licenses",
            return_type=LicensesResponse,
            payload=payload,
            **kw,
        )
