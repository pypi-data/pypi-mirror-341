# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class TemplateBuilder:
    """
    Builds and executes requests for operations under /networkdesign/global/template
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, template_id: str, **kw) -> Any:
        """
        Get global template
        GET /dataservice/networkdesign/global/template/{templateId}

        :param template_id: Template Id
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getGlobalTemplate")
        params = {
            "templateId": template_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/networkdesign/global/template/{templateId}", params=params, **kw
        )

    def put(self, template_id: str, payload: Any, **kw):
        """
        Edit global template
        PUT /dataservice/networkdesign/global/template/{templateId}

        :param template_id: Template Id
        :param payload: Global template
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "editGlobalTemplate")
        params = {
            "templateId": template_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/networkdesign/global/template/{templateId}",
            params=params,
            payload=payload,
            **kw,
        )
