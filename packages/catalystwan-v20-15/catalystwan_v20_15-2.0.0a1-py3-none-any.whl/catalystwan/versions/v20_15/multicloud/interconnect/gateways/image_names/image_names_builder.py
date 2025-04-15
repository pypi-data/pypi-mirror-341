# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse2005, InterconnectTypeParam


class ImageNamesBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/gateways/image-names
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, interconnect_type: InterconnectTypeParam, **kw) -> InlineResponse2005:
        """
        API to retrieve Interconnect Gateway software image versions supported by an Interconnect Provider.
        GET /dataservice/multicloud/interconnect/gateways/image-names

        :param interconnect_type: Interconnect provider type
        :returns: InlineResponse2005
        """
        params = {
            "interconnect-type": interconnect_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/gateways/image-names",
            return_type=InlineResponse2005,
            params=params,
            **kw,
        )
