# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import TypeParam


class CliBuilder:
    """
    Builds and executes requests for operations under /template/config/device/mode/cli
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, type_: TypeParam, **kw) -> List[Any]:
        """
        Generates a JSON object that contains a list of valid devices in CLI mode
        GET /dataservice/template/config/device/mode/cli

        :param type_: Device type
        :returns: List[Any]
        """
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/template/config/device/mode/cli",
            return_type=List[Any],
            params=params,
            **kw,
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Given a JSON list of devices not managed by any third member partners, push to devices from a CLI template
        POST /dataservice/template/config/device/mode/cli

        :param payload: Device list
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/config/device/mode/cli", payload=payload, **kw
        )
