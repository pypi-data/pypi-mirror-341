# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ActivateBody, ActivateResponse


class ActivateBuilder:
    """
    Builds and executes requests for operations under /ise/pxgrid/activate
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: ActivateBody, **kw) -> ActivateResponse:
        """
        Activate pxGrid account
        POST /dataservice/ise/pxgrid/activate

        :param payload: description for pxgrid node
        :returns: ActivateResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/ise/pxgrid/activate",
            return_type=ActivateResponse,
            payload=payload,
            **kw,
        )
