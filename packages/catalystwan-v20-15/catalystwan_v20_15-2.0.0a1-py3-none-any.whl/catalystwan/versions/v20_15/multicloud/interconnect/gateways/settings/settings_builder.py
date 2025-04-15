# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectGatewaySettings


class SettingsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/gateways/{interconnect-gateway-name}/settings
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, interconnect_gateway_name: str, interconnect_account_id: str, **kw
    ) -> InterconnectGatewaySettings:
        """
        API to retrieve the custom settings specified for an Interconnect Gateway
        GET /dataservice/multicloud/interconnect/gateways/{interconnect-gateway-name}/settings

        :param interconnect_gateway_name: Interconnect gateway name
        :param interconnect_account_id: Interconnect Account Id
        :returns: InterconnectGatewaySettings
        """
        params = {
            "interconnect-gateway-name": interconnect_gateway_name,
            "interconnect-account-id": interconnect_account_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/gateways/{interconnect-gateway-name}/settings",
            return_type=InterconnectGatewaySettings,
            params=params,
            **kw,
        )
