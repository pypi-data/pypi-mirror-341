# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .app_fwd_cflowd_flows.app_fwd_cflowd_flows_builder import AppFwdCflowdFlowsBuilder
    from .app_fwd_cflowd_v6_flows.app_fwd_cflowd_v6_flows_builder import AppFwdCflowdV6FlowsBuilder


class CedgecflowdBuilder:
    """
    Builds and executes requests for operations under /device/cedgecflowd
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def app_fwd_cflowd_flows(self) -> AppFwdCflowdFlowsBuilder:
        """
        The app-fwd-cflowd-flows property
        """
        from .app_fwd_cflowd_flows.app_fwd_cflowd_flows_builder import AppFwdCflowdFlowsBuilder

        return AppFwdCflowdFlowsBuilder(self._request_adapter)

    @property
    def app_fwd_cflowd_v6_flows(self) -> AppFwdCflowdV6FlowsBuilder:
        """
        The app-fwd-cflowd-v6-flows property
        """
        from .app_fwd_cflowd_v6_flows.app_fwd_cflowd_v6_flows_builder import (
            AppFwdCflowdV6FlowsBuilder,
        )

        return AppFwdCflowdV6FlowsBuilder(self._request_adapter)
