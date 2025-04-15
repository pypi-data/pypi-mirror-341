# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetRootCertStatusAll


class StatusBuilder:
    """
    Builds and executes requests for operations under /system/device/rootcertchain/status
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, state: str, **kw) -> GetRootCertStatusAll:
        """
        Get controllers vEdge sync status
        GET /dataservice/system/device/rootcertchain/status

        :param state: state
        :returns: GetRootCertStatusAll
        """
        params = {
            "state": state,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/system/device/rootcertchain/status",
            return_type=GetRootCertStatusAll,
            params=params,
            **kw,
        )
