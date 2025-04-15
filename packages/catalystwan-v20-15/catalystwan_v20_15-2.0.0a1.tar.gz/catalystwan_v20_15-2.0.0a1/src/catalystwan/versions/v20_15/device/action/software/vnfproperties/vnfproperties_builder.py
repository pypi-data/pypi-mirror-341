# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetVnfProperties


class VnfpropertiesBuilder:
    """
    Builds and executes requests for operations under /device/action/software/vnfproperties
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, version_id: str, **kw) -> GetVnfProperties:
        """
        Get VNF Properties
        GET /dataservice/device/action/software/vnfproperties/{versionId}

        :param version_id: Version id
        :returns: GetVnfProperties
        """
        params = {
            "versionId": version_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/action/software/vnfproperties/{versionId}",
            return_type=GetVnfProperties,
            params=params,
            **kw,
        )
