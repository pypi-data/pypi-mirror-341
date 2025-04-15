# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class AssociationBuilder:
    """
    Builds and executes requests for operations under /v1/smart-licensing/association
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, template_id: Optional[str] = None, **kw) -> Any:
        """
        Get the devices associated with a template
        GET /dataservice/v1/smart-licensing/association

        :param template_id: template Id
        :returns: Any
        """
        params = {
            "templateId": template_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/v1/smart-licensing/association", params=params, **kw
        )
