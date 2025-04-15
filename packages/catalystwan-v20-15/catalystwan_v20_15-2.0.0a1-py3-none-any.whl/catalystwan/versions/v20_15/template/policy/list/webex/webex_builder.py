# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .update.update_builder import UpdateBuilder


class WebexBuilder:
    """
    Builds and executes requests for operations under /template/policy/list/webex
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> List[Any]:
        """
        TEMP-Create Webex policy lists
        POST /dataservice/template/policy/list/webex

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/policy/list/webex", return_type=List[Any], **kw
        )

    @property
    def update(self) -> UpdateBuilder:
        """
        The update property
        """
        from .update.update_builder import UpdateBuilder

        return UpdateBuilder(self._request_adapter)
