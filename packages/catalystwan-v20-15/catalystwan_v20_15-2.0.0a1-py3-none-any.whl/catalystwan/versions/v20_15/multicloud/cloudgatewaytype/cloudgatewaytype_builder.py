# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CloudTypeParam


class CloudgatewaytypeBuilder:
    """
    Builds and executes requests for operations under /multicloud/cloudgatewaytype
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, cloud_type: Optional[CloudTypeParam] = None, **kw) -> Any:
        """
        Get cloud gateway types for specified cloudType
        GET /dataservice/multicloud/cloudgatewaytype

        :param cloud_type: Cloud type
        :returns: Any
        """
        params = {
            "cloudType": cloud_type,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/cloudgatewaytype", params=params, **kw
        )
