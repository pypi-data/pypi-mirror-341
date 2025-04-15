# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AuditFix, CloudTypeParam, Taskid


class AuditBuilder:
    """
    Builds and executes requests for operations under /multicloud/audit
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, cloud_type: CloudTypeParam, cloud_region: Optional[str] = None, **kw):
        """
        Call an audit with dry run
        GET /dataservice/multicloud/audit

        :param cloud_type: Cloud type
        :param cloud_region: Cloud region
        :returns: None
        """
        params = {
            "cloudType": cloud_type,
            "cloudRegion": cloud_region,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/audit", params=params, **kw
        )

    def post(self, payload: AuditFix, **kw) -> Taskid:
        """
        Call an audit
        POST /dataservice/multicloud/audit

        :param payload: Audit
        :returns: Taskid
        """
        return self._request_adapter.request(
            "POST", "/dataservice/multicloud/audit", return_type=Taskid, payload=payload, **kw
        )
