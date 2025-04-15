# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CloudxBuilder:
    """
    Builds and executes requests for operations under /settings/configuration/cloudx
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Retrieve cloudx configuration value
        GET /dataservice/settings/configuration/cloudx

        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getCloudxConfiguration")
        return self._request_adapter.request(
            "GET", "/dataservice/settings/configuration/cloudx", **kw
        )

    def put(self, payload: str, **kw) -> Any:
        """
        Update cloudx configuration setting
        PUT /dataservice/settings/configuration/cloudx

        :param payload: Payload
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "editCloudxConfiguration")
        return self._request_adapter.request(
            "PUT", "/dataservice/settings/configuration/cloudx", payload=payload, **kw
        )

    def post(self, payload: str, **kw) -> str:
        """
        Add new cloudx configuration
        POST /dataservice/settings/configuration/cloudx

        :param payload: Payload
        :returns: str
        """
        logging.warning("Operation: %s is deprecated", "newCloudxConfiguration")
        return self._request_adapter.request(
            "POST",
            "/dataservice/settings/configuration/cloudx",
            return_type=str,
            payload=payload,
            **kw,
        )
