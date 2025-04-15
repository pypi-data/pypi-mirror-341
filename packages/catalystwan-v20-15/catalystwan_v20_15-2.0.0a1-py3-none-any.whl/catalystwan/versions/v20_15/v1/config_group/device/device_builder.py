# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .associate.associate_builder import AssociateBuilder
    from .deploy.deploy_builder import DeployBuilder
    from .preview.preview_builder import PreviewBuilder
    from .variables.variables_builder import VariablesBuilder


class DeviceBuilder:
    """
    Builds and executes requests for operations under /v1/config-group/{configGroupId}/device
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def associate(self) -> AssociateBuilder:
        """
        The associate property
        """
        from .associate.associate_builder import AssociateBuilder

        return AssociateBuilder(self._request_adapter)

    @property
    def deploy(self) -> DeployBuilder:
        """
        The deploy property
        """
        from .deploy.deploy_builder import DeployBuilder

        return DeployBuilder(self._request_adapter)

    @property
    def preview(self) -> PreviewBuilder:
        """
        The preview property
        """
        from .preview.preview_builder import PreviewBuilder

        return PreviewBuilder(self._request_adapter)

    @property
    def variables(self) -> VariablesBuilder:
        """
        The variables property
        """
        from .variables.variables_builder import VariablesBuilder

        return VariablesBuilder(self._request_adapter)
