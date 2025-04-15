# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class AvailableBuilder:
    """
    Builds and executes requests for operations under /template/device/config/available
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, master_template_id: str, **kw) -> List[Any]:
        """
        Get possible device list by master template Id


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/template/device/config/available/{masterTemplateId}

        :param master_template_id: Template Id
        :returns: List[Any]
        """
        params = {
            "masterTemplateId": master_template_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/template/device/config/available/{masterTemplateId}",
            return_type=List[Any],
            params=params,
            **kw,
        )
