# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface


class TemplateBuilder:
    """
    Builds and executes requests for operations under /networkdesign/profile/template
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, template_id: str, payload: Any, **kw):
        """
        Edit device profile template
        PUT /dataservice/networkdesign/profile/template/{templateId}

        :param template_id: Template Id
        :param payload: Global template
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "editDeviceProfileTemplate")
        params = {
            "templateId": template_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/networkdesign/profile/template/{templateId}",
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(self, template_id: str, **kw) -> Any:
        """
        Get device profile template
        GET /dataservice/networkdesign/profile/template/{templateId}

        :param template_id: Template Id
        :returns: Any
        """
        ...

    @overload
    def get(self, **kw) -> List[Any]:
        """
        Generate profile template list
        GET /dataservice/networkdesign/profile/template

        :returns: List[Any]
        """
        ...

    def get(self, template_id: Optional[str] = None, **kw) -> Union[List[Any], Any]:
        # /dataservice/networkdesign/profile/template/{templateId}
        if self._request_adapter.param_checker([(template_id, str)], []):
            logging.warning("Operation: %s is deprecated", "getDeviceProfileTemplate")
            params = {
                "templateId": template_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/networkdesign/profile/template/{templateId}",
                params=params,
                **kw,
            )
        # /dataservice/networkdesign/profile/template
        if self._request_adapter.param_checker([], [template_id]):
            logging.warning("Operation: %s is deprecated", "generateProfileTemplateList")
            return self._request_adapter.request(
                "GET", "/dataservice/networkdesign/profile/template", return_type=List[Any], **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")
