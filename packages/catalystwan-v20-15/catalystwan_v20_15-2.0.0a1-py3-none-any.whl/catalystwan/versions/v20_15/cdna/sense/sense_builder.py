# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DnaSenseResponse


class SenseBuilder:
    """
    Builds and executes requests for operations under /cdna/sense
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, tag: str, **kw) -> DnaSenseResponse:
        """
        Get Sense Service
        GET /dataservice/cdna/sense/{tag}

        :param tag: Tag
        :returns: DnaSenseResponse
        """
        params = {
            "tag": tag,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/cdna/sense/{tag}",
            return_type=DnaSenseResponse,
            params=params,
            **kw,
        )
