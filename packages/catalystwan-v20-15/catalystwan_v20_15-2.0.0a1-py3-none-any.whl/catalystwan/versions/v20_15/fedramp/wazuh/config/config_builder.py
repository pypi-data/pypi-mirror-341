# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ConfigBuilder:
    """
    Builds and executes requests for operations under /fedramp/wazuh/config
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Configure Wazuh agent
        POST /dataservice/fedramp/wazuh/config

        :param payload: Wazhuh configuration
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/fedramp/wazuh/config", payload=payload, **kw
        )
