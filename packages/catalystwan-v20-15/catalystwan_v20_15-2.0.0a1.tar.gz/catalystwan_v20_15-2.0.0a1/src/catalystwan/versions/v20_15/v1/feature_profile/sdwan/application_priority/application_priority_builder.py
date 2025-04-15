# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cloud_probe.cloud_probe_builder import CloudProbeBuilder
    from .qos_policy.qos_policy_builder import QosPolicyBuilder
    from .traffic_policy.traffic_policy_builder import TrafficPolicyBuilder


class ApplicationPriorityBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/application-priority
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def cloud_probe(self) -> CloudProbeBuilder:
        """
        The cloud-probe property
        """
        from .cloud_probe.cloud_probe_builder import CloudProbeBuilder

        return CloudProbeBuilder(self._request_adapter)

    @property
    def qos_policy(self) -> QosPolicyBuilder:
        """
        The qos-policy property
        """
        from .qos_policy.qos_policy_builder import QosPolicyBuilder

        return QosPolicyBuilder(self._request_adapter)

    @property
    def traffic_policy(self) -> TrafficPolicyBuilder:
        """
        The traffic-policy property
        """
        from .traffic_policy.traffic_policy_builder import TrafficPolicyBuilder

        return TrafficPolicyBuilder(self._request_adapter)
