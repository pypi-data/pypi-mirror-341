# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class ResourceGroupBuilder:
    """
    Builds and executes requests for operations under /template/feature/resource-group
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, template_id: str, resource_group_name: str, **kw):
        """
        Change template resource group
        POST /dataservice/template/feature/resource-group/{resourceGroupName}/{templateId}

        :param template_id: Template Id
        :param resource_group_name: Resrouce group name
        :returns: None
        """
        params = {
            "templateId": template_id,
            "resourceGroupName": resource_group_name,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/template/feature/resource-group/{resourceGroupName}/{templateId}",
            params=params,
            **kw,
        )
