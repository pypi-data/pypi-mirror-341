# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectWidget


class WidgetBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/widget
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, interconnect_type: str, **kw) -> InterconnectWidget:
        """
        API to retrieve an Interconnect widget for an Interconnect type.
        GET /dataservice/multicloud/interconnect/{interconnect-type}/widget

        :param interconnect_type: Interconnect provider type
        :returns: InterconnectWidget
        """
        ...

    @overload
    def get(self, **kw) -> List[InterconnectWidget]:
        """
        API to retrieve all Interconnect widgets.
        GET /dataservice/multicloud/interconnect/widget

        :returns: List[InterconnectWidget]
        """
        ...

    def get(
        self, interconnect_type: Optional[str] = None, **kw
    ) -> Union[List[InterconnectWidget], InterconnectWidget]:
        # /dataservice/multicloud/interconnect/{interconnect-type}/widget
        if self._request_adapter.param_checker([(interconnect_type, str)], []):
            params = {
                "interconnect-type": interconnect_type,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/multicloud/interconnect/{interconnect-type}/widget",
                return_type=InterconnectWidget,
                params=params,
                **kw,
            )
        # /dataservice/multicloud/interconnect/widget
        if self._request_adapter.param_checker([], [interconnect_type]):
            return self._request_adapter.request(
                "GET",
                "/dataservice/multicloud/interconnect/widget",
                return_type=List[InterconnectWidget],
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
