# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ExportcsvBuilder:
    """
    Builds and executes requests for operations under /template/device/config/exportcsv
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Export the device template to CSV format for given template id


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/template/device/config/exportcsv

        :param payload: Device template
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/device/config/exportcsv", payload=payload, **kw
        )
