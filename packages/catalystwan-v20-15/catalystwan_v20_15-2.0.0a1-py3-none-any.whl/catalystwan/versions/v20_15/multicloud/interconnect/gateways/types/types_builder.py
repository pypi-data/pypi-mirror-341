# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectTypeParam


class TypesBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/gateways/types
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, interconnect_type: InterconnectTypeParam, **kw) -> List[str]:
        """
        API to retrieve the supported Interconnect Gateway solution types.
        GET /dataservice/multicloud/interconnect/gateways/types

        :param interconnect_type: Interconnect provider type
        :returns: List[str]
        """
        params = {
            "interconnect-type": interconnect_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/gateways/types",
            return_type=List[str],
            params=params,
            **kw,
        )
