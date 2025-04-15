# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectGlobalSettings, InterconnectTypeParam


class GlobalBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/settings/global
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, interconnect_type: InterconnectTypeParam, **kw) -> InterconnectGlobalSettings:
        """
        API to retrieve global settings for an Interconnect provider type.
        GET /dataservice/multicloud/interconnect/settings/global

        :param interconnect_type: Interconnect provider type
        :returns: InterconnectGlobalSettings
        """
        params = {
            "interconnect-type": interconnect_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/settings/global",
            return_type=InterconnectGlobalSettings,
            params=params,
            **kw,
        )

    def put(self, payload: InterconnectGlobalSettings, **kw):
        """
        API to update global settings for an Interconnect provider.
        PUT /dataservice/multicloud/interconnect/settings/global

        :param payload: Request Payload for Multicloud Interconnect Global Settings
        :returns: None
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/multicloud/interconnect/settings/global", payload=payload, **kw
        )

    def post(self, payload: InterconnectGlobalSettings, **kw):
        """
        API to add global settings for an Interconnect provider.
        POST /dataservice/multicloud/interconnect/settings/global

        :param payload: Request Payload for Multicloud Interconnect Global Settings
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/multicloud/interconnect/settings/global", payload=payload, **kw
        )
