# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class FeatureBuilder:
    """
    Builds and executes requests for operations under /networkdesign/profile/feature
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Generate device profile template list
        GET /dataservice/networkdesign/profile/feature

        :returns: List[Any]
        """
        logging.warning("Operation: %s is deprecated", "getDeviceProfileFeatureTemplateList")
        return self._request_adapter.request(
            "GET", "/dataservice/networkdesign/profile/feature", return_type=List[Any], **kw
        )
