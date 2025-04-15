# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cloudx.cloudx_builder import CloudxBuilder
    from .config.config_builder import ConfigBuilder
    from .cor.cor_builder import CorBuilder
    from .cortex.cortex_builder import CortexBuilder
    from .device.device_builder import DeviceBuilder
    from .feature.feature_builder import FeatureBuilder
    from .lock.lock_builder import LockBuilder
    from .policy.policy_builder import PolicyBuilder
    from .security.security_builder import SecurityBuilder


class TemplateBuilder:
    """
    Builds and executes requests for operations under /template
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def cloudx(self) -> CloudxBuilder:
        """
        The cloudx property
        """
        from .cloudx.cloudx_builder import CloudxBuilder

        return CloudxBuilder(self._request_adapter)

    @property
    def config(self) -> ConfigBuilder:
        """
        The config property
        """
        from .config.config_builder import ConfigBuilder

        return ConfigBuilder(self._request_adapter)

    @property
    def cor(self) -> CorBuilder:
        """
        The cor property
        """
        from .cor.cor_builder import CorBuilder

        return CorBuilder(self._request_adapter)

    @property
    def cortex(self) -> CortexBuilder:
        """
        The cortex property
        """
        from .cortex.cortex_builder import CortexBuilder

        return CortexBuilder(self._request_adapter)

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def feature(self) -> FeatureBuilder:
        """
        The feature property
        """
        from .feature.feature_builder import FeatureBuilder

        return FeatureBuilder(self._request_adapter)

    @property
    def lock(self) -> LockBuilder:
        """
        The lock property
        """
        from .lock.lock_builder import LockBuilder

        return LockBuilder(self._request_adapter)

    @property
    def policy(self) -> PolicyBuilder:
        """
        The policy property
        """
        from .policy.policy_builder import PolicyBuilder

        return PolicyBuilder(self._request_adapter)

    @property
    def security(self) -> SecurityBuilder:
        """
        The security property
        """
        from .security.security_builder import SecurityBuilder

        return SecurityBuilder(self._request_adapter)
