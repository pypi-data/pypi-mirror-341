# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class MigrationBuilder:
    """
    Builds and executes requests for operations under /template/device/migration
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, has_aaa: Optional[bool] = None, **kw) -> List[Any]:
        """
        Generate a list of templates which require migration


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/template/device/migration

        :param has_aaa: Return only those uses AAA
        :returns: List[Any]
        """
        params = {
            "hasAAA": has_aaa,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/template/device/migration",
            return_type=List[Any],
            params=params,
            **kw,
        )

    def post(
        self,
        id: List[str],
        prefix: Optional[str] = "cisco",
        include_all: Optional[bool] = True,
        **kw,
    ) -> Any:
        """
        Migrate the device templates given the template Ids
        POST /dataservice/template/device/migration

        :param id: Template Id
        :param prefix: Prefix
        :param include_all: Include all flag
        :returns: Any
        """
        params = {
            "id": id,
            "prefix": prefix,
            "includeAll": include_all,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/template/device/migration", params=params, **kw
        )
