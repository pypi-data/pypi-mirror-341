# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import BatchFlow


class BatchBuilder:
    """
    Builds and executes requests for operations under /jobs/batch
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: BatchFlow, **kw) -> str:
        """
        Batch processing multiple REST API calls
        POST /dataservice/jobs/batch

        :param payload: Payload for executing multiple APIs
        :returns: str
        """
        return self._request_adapter.request(
            "POST", "/dataservice/jobs/batch", return_type=str, payload=payload, **kw
        )
