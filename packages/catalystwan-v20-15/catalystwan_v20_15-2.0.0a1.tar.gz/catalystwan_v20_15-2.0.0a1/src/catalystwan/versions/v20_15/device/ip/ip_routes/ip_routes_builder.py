# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class IpRoutesBuilder:
    """
    Builds and executes requests for operations under /device/ip/ipRoutes
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        routing_instance_name: Optional[str] = None,
        address_family: Optional[str] = None,
        outgoing_interface: Optional[str] = None,
        source_protocol: Optional[str] = None,
        next_hop_address: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get ietf routing list from device
        GET /dataservice/device/ip/ipRoutes

        :param routing_instance_name: VPN Id
        :param address_family: Address family
        :param outgoing_interface: Outgoing Interface
        :param source_protocol: Source Protocol
        :param next_hop_address: Next Hop Address
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "routing-instance-name": routing_instance_name,
            "address-family": address_family,
            "outgoing-interface": outgoing_interface,
            "source-protocol": source_protocol,
            "next-hop-address": next_hop_address,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/ip/ipRoutes", params=params, **kw
        )
