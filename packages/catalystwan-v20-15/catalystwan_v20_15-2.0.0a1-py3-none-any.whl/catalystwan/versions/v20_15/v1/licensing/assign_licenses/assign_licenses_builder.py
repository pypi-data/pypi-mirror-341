# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AssignLicensesRequest


class AssignLicensesBuilder:
    """
    Builds and executes requests for operations under /v1/licensing/assign-licenses
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: AssignLicensesRequest, **kw):
        """
        Assign licenses to devices
        POST /dataservice/v1/licensing/assign-licenses

        :param payload: Payload
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/v1/licensing/assign-licenses", payload=payload, **kw
        )
