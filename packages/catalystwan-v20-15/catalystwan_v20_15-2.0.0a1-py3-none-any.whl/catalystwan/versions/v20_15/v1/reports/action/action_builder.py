# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ActionParam, UpdateReportTemplateResponse


class ActionBuilder:
    """
    Builds and executes requests for operations under /v1/reports/{reportId}/action
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, report_id: str, action: ActionParam, **kw) -> UpdateReportTemplateResponse:
        """
        User operations for specific report template, which includes activate,deactivate and run immediately
        PUT /dataservice/v1/reports/{reportId}/action/{action}

        :param report_id: Report id
        :param action: Action
        :returns: UpdateReportTemplateResponse
        """
        params = {
            "reportId": report_id,
            "action": action,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/reports/{reportId}/action/{action}",
            return_type=UpdateReportTemplateResponse,
            params=params,
            **kw,
        )
