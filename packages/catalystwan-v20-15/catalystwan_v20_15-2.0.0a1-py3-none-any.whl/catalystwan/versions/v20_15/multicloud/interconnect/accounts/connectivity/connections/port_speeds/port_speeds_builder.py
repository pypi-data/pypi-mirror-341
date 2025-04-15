# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse2007


class PortSpeedsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/accounts/{interconnect-account-id}/connectivity/connections/{connection-type}/port-speeds
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        interconnect_type: str,
        interconnect_account_id: str,
        connection_type: str,
        cloud_type: Optional[str] = None,
        cloud_account_id: Optional[str] = None,
        connect_type: Optional[str] = None,
        connect_subtype: Optional[str] = None,
        connectivity_gateway_name: Optional[str] = None,
        partner_port: Optional[str] = None,
        **kw,
    ) -> InlineResponse2007:
        """
        API to retrieve supported port speeds for an Interconnect connectivity.
        GET /dataservice/multicloud/interconnect/{interconnect-type}/accounts/{interconnect-account-id}/connectivity/connections/{connection-type}/port-speeds

        :param interconnect_type: Interconnect provider Type
        :param interconnect_account_id: Interconnect provider account id
        :param connection_type: Interconnect connectivity type
        :param cloud_type: Cloud provider type
        :param cloud_account_id: Cloud account id
        :param connect_type: Interconnect connection connect type
        :param connect_subtype: Interconnect connection connect sub-type
        :param connectivity_gateway_name: Cloud connectivity gateway name
        :param partner_port: Interconnect cloud onRamp partner port location name
        :returns: InlineResponse2007
        """
        params = {
            "interconnect-type": interconnect_type,
            "interconnect-account-id": interconnect_account_id,
            "connection-type": connection_type,
            "cloud-type": cloud_type,
            "cloud-account-id": cloud_account_id,
            "connect-type": connect_type,
            "connect-subtype": connect_subtype,
            "connectivity-gateway-name": connectivity_gateway_name,
            "partner-port": partner_port,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/{interconnect-type}/accounts/{interconnect-account-id}/connectivity/connections/{connection-type}/port-speeds",
            return_type=InlineResponse2007,
            params=params,
            **kw,
        )
