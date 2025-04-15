# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional, overload

from catalystwan.abc import RequestAdapterInterface


class SyncstatusBuilder:
    """
    Builds and executes requests for operations under /template/device/syncstatus
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, template_id: str, **kw) -> List[Any]:
        """
        Get out of sync devices


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/template/device/syncstatus/{templateId}

        :param template_id: Template Id
        :returns: List[Any]
        """
        ...

    @overload
    def get(self, **kw) -> List[Any]:
        """
        Get template sync status


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/template/device/syncstatus

        :returns: List[Any]
        """
        ...

    def get(self, template_id: Optional[str] = None, **kw) -> List[Any]:
        # /dataservice/template/device/syncstatus/{templateId}
        if self._request_adapter.param_checker([(template_id, str)], []):
            params = {
                "templateId": template_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/template/device/syncstatus/{templateId}",
                return_type=List[Any],
                params=params,
                **kw,
            )
        # /dataservice/template/device/syncstatus
        if self._request_adapter.param_checker([], [template_id]):
            return self._request_adapter.request(
                "GET", "/dataservice/template/device/syncstatus", return_type=List[Any], **kw
            )
        raise RuntimeError("Provided arguments do not match any signature")
