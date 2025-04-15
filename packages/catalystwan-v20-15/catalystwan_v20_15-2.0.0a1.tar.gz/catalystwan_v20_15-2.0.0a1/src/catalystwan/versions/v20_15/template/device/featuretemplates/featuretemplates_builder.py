# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class FeaturetemplatesBuilder:
    """
    Builds and executes requests for operations under /template/device/{templateId}/featuretemplates
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, template_id: str, **kw):
        """
        get Associated Feature Templates Details
        GET /dataservice/template/device/{templateId}/featuretemplates

        :param template_id: TemplateId
        :returns: None
        """
        params = {
            "templateId": template_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/device/{templateId}/featuretemplates", params=params, **kw
        )
